# ----------------------------------------------------------------------
# RepoSpec tests
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Third-party modules
import pytest

# Gufo Tower modules
from gufo.tower.core.repospec import RepoSpec


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
    expected_revision: str | None,
) -> None:
    """Test parsing repository specifications."""
    spec = RepoSpec.from_url(url)
    assert spec.url == expected_url
    assert spec.revision == expected_revision
