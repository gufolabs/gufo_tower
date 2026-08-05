# ----------------------------------------------------------------------
# Pull tests
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
import tempfile
from collections.abc import Iterator
from pathlib import Path
from typing import Optional

# Third paryy modules
import pytest

# Gufo Tower modules
from gufo.tower.api.pull import PullAPI, RepoSpec

REPO_URL = "https://github.com/gufolabs/git_test.git"
INVALID_REPO_URL = "https://github.com/gufolabs/git_test_invalid.git"


@pytest.fixture
def workdir() -> Iterator[Path]:
    """Create temporary working directory."""
    with tempfile.TemporaryDirectory() as td:
        yield Path(td)


def test_pull_clone_str(workdir: Path) -> None:
    """Test cloning into a new directory."""
    repo = workdir / "repo"
    PullAPI.pull(REPO_URL, str(repo))
    assert (repo / ".git").is_dir()


def test_pull_clone_path(workdir: Path) -> None:
    """Test cloning into a new directory."""
    repo = workdir / "repo"
    PullAPI.pull(REPO_URL, repo)
    assert (repo / ".git").is_dir()


def test_pull_update(workdir: Path) -> None:
    """Test updating an existing repository."""
    repo = workdir / "repo"
    PullAPI.pull(REPO_URL, repo)
    PullAPI.pull(REPO_URL, repo)
    assert (repo / ".git").is_dir()


def test_pull_replace_directory(workdir: Path) -> None:
    """Test replacing an existing non-git directory."""
    repo = workdir / "repo"
    repo.mkdir()
    (repo / "junk.txt").write_text("junk")
    PullAPI.pull(REPO_URL, repo)
    assert (repo / ".git").is_dir()
    assert not (repo / "junk.txt").exists()


def test_pull_invalid_repo(workdir: Path) -> None:
    """Test pulling from invalid repo."""
    repo_path = workdir / "repo"
    with pytest.raises(RuntimeError):
        PullAPI.pull(f"{REPO_URL}@invalid", repo_path)


def test_pull_missing_remote_branch(workdir: Path) -> None:
    """Test missing remote branch."""
    repo_path = workdir / "repo"
    with pytest.raises(RuntimeError):
        PullAPI.pull(INVALID_REPO_URL, repo_path)


@pytest.mark.parametrize(
    ("revision", "expected_version"),
    [
        ("start", None),
        ("v1", "1"),
        ("v2", "2"),
        ("v3", "3"),
        ("master", "3"),
    ],
    ids=["start", "v1", "v2", "v3", "master"],
)
def test_pull_revision(
    workdir: Path,
    revision: str,
    expected_version: Optional[str],
) -> None:
    """Test pulling different repository revisions."""
    repo = workdir / "repo"
    PullAPI.pull(f"{REPO_URL}@{revision}", repo)
    assert (repo / "README.md").is_file()
    version_file = repo / "version.txt"
    if expected_version is None:
        assert not version_file.exists()
    else:
        assert version_file.is_file()
        assert version_file.read_text().strip() == expected_version


@pytest.mark.parametrize(
    ("url", "expected_url", "expected_revision"),
    [
        (
            "https://github.com/gufolabs/git-test.git",
            "https://github.com/gufolabs/git-test.git",
            None,
        ),
        (
            "https://github.com/gufolabs/git-test.git@v1",
            "https://github.com/gufolabs/git-test.git",
            "v1",
        ),
        (
            "git+https://github.com/gufolabs/git-test.git",
            "https://github.com/gufolabs/git-test.git",
            None,
        ),
        (
            "git+https://github.com/gufolabs/git-test.git@stable",
            "https://github.com/gufolabs/git-test.git",
            "stable",
        ),
        (
            "ssh://git@github.com/gufolabs/git-test.git",
            "ssh://git@github.com/gufolabs/git-test.git",
            None,
        ),
        (
            "ssh://git@github.com/gufolabs/git-test.git@v2",
            "ssh://git@github.com/gufolabs/git-test.git",
            "v2",
        ),
        (
            "git+ssh://git@github.com/gufolabs/git-test.git",
            "ssh://git@github.com/gufolabs/git-test.git",
            None,
        ),
        (
            "git+ssh://git@github.com/gufolabs/git-test.git@main",
            "ssh://git@github.com/gufolabs/git-test.git",
            "main",
        ),
        (
            "git@github.com:gufolabs/git-test.git",
            "git@github.com:gufolabs/git-test.git",
            None,
        ),
        (
            "git@github.com:gufolabs/git-test.git@v3",
            "git@github.com:gufolabs/git-test.git",
            "v3",
        ),
    ],
    ids=[
        "https",
        "https-tag",
        "git+https",
        "git+https-tag",
        "ssh",
        "ssh-tag",
        "git+ssh",
        "git+ssh-tag",
        "scp",
        "scp-tag",
    ],
)
def test_repo_spec_from_url(
    url: str,
    expected_url: str,
    expected_revision: Optional[str],
) -> None:
    """Test parsing repository specifications."""
    spec = RepoSpec.from_url(url)
    assert spec.url == expected_url
    assert spec.revision == expected_revision
