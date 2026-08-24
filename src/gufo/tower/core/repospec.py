# ----------------------------------------------------------------------
# RepoSpec
# ----------------------------------------------------------------------
# Copyright (C) 2015-2026 Gufo Labs
# See LICENSE for details
# ----------------------------------------------------------------------

# Python modules
from dataclasses import dataclass


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
    revision: str | None = None

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
