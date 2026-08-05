# ----------------------------------------------------------------------
# Pull repo
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import datetime
import logging
import shutil
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

# Third-party modules
from dulwich import porcelain
from dulwich.repo import Repo
from gufo.err import err

# Gufo Tower modules
from ..models.db import db
from ..models.environment import Environment
from ..models.pulllog import PullLog
from ..models.role import Role
from .base import API, api

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


class PullAPI(API):
    name = "pull"
    executor = ThreadPoolExecutor(2)

    @api
    def is_pulled(self, env_id):
        """Check repo is pulled and ready to deploy.

        Args:
            env_id
        """
        try:
            env = Environment.get(Environment.id == int(env_id))
        except Environment.DoesNotExist:
            return False
        return (env.playbook_path / "site.yml").is_file()

    @api
    def start_job(self, env_id):
        try:
            env = Environment.get(Environment.id == int(env_id))
        except Environment.DoesNotExist:
            return {"success": False}
        with db.atomic():
            job = PullLog(
                start_ts=datetime.datetime.now(),
                environment=env,
                user=self.handler.current_user.name,
                repo=env.playbook_link,
            )
            job.save()
            self.executor.submit(self.pull_job, job)
            return {"success": True, "job": job.id}

    @api
    def get_job_status(self, env_id, job_id):
        with db.atomic():
            try:
                env = Environment.get(Environment.id == int(env_id))
            except Environment.DoesNotExist:
                return {"success": False}
            try:
                job = PullLog.get(
                    PullLog.id == int(job_id), PullLog.environment == env
                )
            except PullLog.DoesNotExist:
                return {"success": False}
        r = {
            "success": True,
            "complete": job.complete_ts is not None,
        }
        if r["complete"]:
            r["status"] = job.status
        return r

    def pull_job(self, job: PullLog) -> None:
        env = job.environment
        status = True
        log = "success"
        try:
            self.pull(env.playbook_link, env.repo_path)
            # Detect playbooks root
            repo_playbooks_path = env.repo_path / "ansible"
            if not repo_playbooks_path.is_dir():
                # Playbooks on repo root
                repo_playbooks_path = env.repo_path
            # Clear old playbooks
            shutil.rmtree(env.playbook_path, ignore_errors=True)
            # Extract new from repo to playbooks
            shutil.move(repo_playbooks_path, env.playbook_path)
            # Pull all enabled roles
            for role in Role.select().where(
                Role.environment == env, Role.is_enabled == True
            ):
                self.pull(role.link, role.role_path)
        except BaseException as e:
            logger.error("Failed to pull: %s", e)
            err.process()
            status = False
            log = f"Failed: {e}"
        with db.atomic():
            job.complete_ts = datetime.datetime.now()
            job.status = status
            job.log = log
            job.save()

    @staticmethod
    def pull(link: str, path: Union[str, Path]) -> None:
        """Clone or update a git repository.

        Args:
            link: Repository URL.
            path: Local repository path.

        Raises:
            RuntimeError: on invalid repo or missed tag.
        """
        spec = RepoSpec.from_url(link)
        path = Path(path)

        logger.debug(
            "Pull repo: %s, revision: %s, path: %s",
            spec.url,
            spec.revision,
            path,
        )

        try:
            # Ensure repo is exists
            path.mkdir(parents=True, exist_ok=True)
            # Pull
            if (path / ".git").is_dir():
                repo = Repo(path)
                porcelain.fetch(repo)
            else:
                shutil.rmtree(path, ignore_errors=True)
                porcelain.clone(
                    source=spec.url,
                    target=path,
                )
                repo = Repo(path)
        except BaseException as e:
            err.process()
            msg = f"failed to fetch repo: {e}"
            raise RuntimeError(msg) from e
        if spec.revision is not None:
            try:
                porcelain.checkout(repo, spec.revision)
            except KeyError as e:
                msg = f"Invalid tag: {spec.revision}"
                raise RuntimeError(msg) from e


@dataclass
class RepoSpec:
    """Normalized Git repository specification.

    The parser accepts repository specifications in either native Git form
    or the `pip`-style notation:

    * `https://github.com/org/repo.git`
    * `https://github.com/org/repo.git@stable`
    * `git+https://github.com/org/repo.git@stable`
    * `git+ssh://git@github.com/org/repo.git@main`
    * `git@github.com:org/repo.git`
    * `git@github.com:org/repo.git@v1.2.3`

    The optional `git+` prefix is stripped from the URL. If a revision is
    present, it is returned separately.
    """

    url: str
    revision: Optional[str] = None

    @classmethod
    def from_url(cls, url: str) -> "RepoSpec":
        """Parse a repository specification.

        Args:
            url: Repository specification. May optionally start with
                `git+` and/or end with `@<revision>`.

        Returns:
            Parsed repository specification with a normalized repository URL
            and an optional revision.
        """
        if url.startswith("git+"):
            url = url[4:]
        head, sep, tail = url.rpartition("@")
        if not sep:
            return cls(url=url)
        # '@' belongs to the revision only when it is the last separator.
        # Examples:
        #
        #   https://host/repo.git@main      -> revision
        #   git@github.com:org/repo.git     -> SSH user
        #
        if "/" in tail or ":" in tail:
            return cls(url=url)
        return cls(url=head, revision=tail)
