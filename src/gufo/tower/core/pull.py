# ----------------------------------------------------------------------
# Repo pulling utilities
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import logging
import re
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

SHA_RE = re.compile(r"^[0-9a-fA-F]{7,64}$")


def resolve_refspecs(url: str, revision: str | None) -> str | None:
    """Resolve a revision to remote Git refspecs.

    Args:
        url: Repository URL.
        revision: Branch, tag, or commit to fetch.

    Returns:
        List of Git refspecs, or None if no revision is specified.

    Raises:
        KeyError: if revision is invalid or not found.
    """
    if revision is None:
        return None
    refs = porcelain.ls_remote(url).refs
    branch = f"refs/heads/{revision}".encode()
    if branch in refs:
        return f"{branch.decode()}:{branch.decode()}"
    tag = f"refs/tags/{revision}".encode()
    if tag in refs:
        return f"{tag.decode()}:{tag.decode()}"
    if SHA_RE.fullmatch(revision):
        return revision
    raise KeyError(revision)


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
        # Check repo
        repo = Repo(path) if (path / ".git").is_dir() else None
        if (
            repo is None
            or repo.get_config().get(("remote", "origin"), "url")
            != spec.url.encode()
        ):
            shutil.rmtree(path, ignore_errors=True)
            porcelain.clone(
                source=spec.url,
                target=path,
                depth=1,
                branch=spec.revision,
            )
            return
        result = porcelain.fetch(
            repo,
            spec.url,
            depth=1,
            force=True,
        )
        if spec.revision is not None:
            refspec = resolve_refspecs(spec.url, spec.revision)
            if refspec is None:
                raise KeyError(spec.revision)
            source, _ = refspec.split(":", 1)
            revision = result.refs[source.encode()]
            porcelain.checkout(repo, revision, force=True)
    except KeyError as e:
        msg = f"Invalid revision: {spec.revision}"
        raise RuntimeError(msg) from e
    except BaseException as e:
        err.process()
        msg = f"failed to fetch repo: {e}"
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
    shutil.copytree(repo_playbooks_path, env.playbook_path, dirs_exist_ok=True)
    # Pull all enabled roles
    for role in Role.select().where(Role.environment == env, Role.is_enabled):
        pull(role.link, role.role_path)
