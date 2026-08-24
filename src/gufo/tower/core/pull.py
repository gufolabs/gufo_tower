# ----------------------------------------------------------------------
# Repo pulling utilities
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import logging
import shutil
from pathlib import Path

# Third-party modules
from dulwich import porcelain
from dulwich.repo import Repo
from gufo.err import err

# Gufo Tower modules
from ..models.environment import Environment
from ..models.role import Role
from .repospec import RepoSpec

logger = logging.getLogger(__name__)


def pull(link: str, path: str | Path) -> None:
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
            porcelain.fetch(repo, spec.url)
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
            porcelain.checkout(repo, spec.revision, force=True)
        except KeyError as e:
            msg = f"Invalid tag: {spec.revision}"
            raise RuntimeError(msg) from e


def prepare_env(env: Environment) -> None:
    pull(env.playbook_link, env.repo_path)
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
        pull(role.link, role.role_path)
