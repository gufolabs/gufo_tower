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

# Third paryy modules
import pytest

# Gufo Tower modules
from gufo.tower.core.pull import pull

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
    pull(REPO_URL, str(repo))
    assert (repo / ".git").is_dir()


def test_pull_clone_path(workdir: Path) -> None:
    """Test cloning into a new directory."""
    repo = workdir / "repo"
    pull(REPO_URL, repo)
    assert (repo / ".git").is_dir()


def test_pull_update(workdir: Path) -> None:
    """Test updating an existing repository."""
    repo = workdir / "repo"
    pull(REPO_URL, repo)
    pull(REPO_URL, repo)
    assert (repo / ".git").is_dir()


def test_pull_replace_directory(workdir: Path) -> None:
    """Test replacing an existing non-git directory."""
    repo = workdir / "repo"
    repo.mkdir()
    (repo / "junk.txt").write_text("junk")
    pull(REPO_URL, repo)
    assert (repo / ".git").is_dir()
    assert not (repo / "junk.txt").exists()


def test_pull_invalid_repo(workdir: Path) -> None:
    """Test pulling from invalid repo."""
    repo_path = workdir / "repo"
    with pytest.raises(RuntimeError):
        pull(f"{REPO_URL}@invalid", repo_path)


def test_pull_missing_remote_branch(workdir: Path) -> None:
    """Test missing remote branch."""
    repo_path = workdir / "repo"
    with pytest.raises(RuntimeError):
        pull(INVALID_REPO_URL, repo_path)


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
    expected_version: str | None,
) -> None:
    """Test pulling different repository revisions."""
    repo = workdir / "repo"
    pull(f"{REPO_URL}@{revision}", repo)
    assert (repo / "README.md").is_file()
    version_file = repo / "version.txt"
    if expected_version is None:
        assert not version_file.exists()
    else:
        assert version_file.is_file()
        assert version_file.read_text().strip() == expected_version
