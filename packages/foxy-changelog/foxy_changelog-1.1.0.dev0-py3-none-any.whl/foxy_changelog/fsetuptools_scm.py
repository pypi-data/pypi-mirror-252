from __future__ import annotations

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from setuptools_scm.version import ScmVersion


def simplified_semver_version_foxy(version: ScmVersion) -> str:
    return "1.2.0"
