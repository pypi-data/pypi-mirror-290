import string
from typing import Dict, Optional

from packaging.version import InvalidVersion
from packaging.version import parse as parse_version


class Repo:
    def __init__(
        self,
        repo: Dict,
        tags_and_hashes: Dict,
        latest_hash: Optional[str] = None,
        all_versions: bool = False,
        bleeding_edge: bool = False,
    ) -> None:
        self._url: str = repo["repo"]
        self._name: str = repo["repo"].split("/")[-1]
        self._tags_and_hashes: Dict = tags_and_hashes
        self._latest_hash: Optional[str] = latest_hash
        self._is_hash: bool = self._is_version_a_hash(repo["rev"])
        self._current_version: str = repo["rev"]
        self._latest_version: str = self._get_latest_version(
            all_versions, bleeding_edge
        )

    @property
    def is_local(self) -> bool:
        return not self._url.startswith("http")

    @property
    def has_tags_and_hashes(self) -> bool:
        return len(self._tags_and_hashes) > 0

    @property
    def name(self) -> str:
        return self._name

    @property
    def current_version(self) -> str:
        return self._current_version

    @property
    def latest_version(self) -> str:
        return self._latest_version

    @staticmethod
    def _is_version_a_hash(version: str) -> bool:
        # The minimum length for an abbreviated hash is 4:
        # <https://git-scm.com/docs/git-config#Documentation/git-config.txt-coreabbrev>.
        if len(version) < 4:
            return False
        else:
            # Credit goes to Levon (https://stackoverflow.com/users/1209279/levon)
            # for this idea: <https://stackoverflow.com/a/11592279/7593853>.
            return all(character in string.hexdigits for character in version)

    def _get_latest_tag(self, all_versions: bool) -> str:
        if not self.has_tags_and_hashes:
            return self._current_version
        if all_versions:
            return next(iter(self._tags_and_hashes))
        for t in self._tags_and_hashes:
            if not any(v in t for v in ("a", "b", "rc")):
                return t
        return next(iter(self._tags_and_hashes))

    def _get_latest_version(self, all_versions: bool, bleeding_edge: bool) -> str:
        latest_tag: str = self._get_latest_tag(all_versions or bleeding_edge)
        latest_tag_hash: Optional[str] = self._tags_and_hashes.get(latest_tag)
        try:
            parse_version(self._current_version)
            if bleeding_edge:
                return (
                    self._latest_hash
                    if self._latest_hash
                    and latest_tag_hash
                    and latest_tag_hash != self._latest_hash
                    else latest_tag
                )
            return latest_tag
        except (InvalidVersion, IndexError):
            pass
        if self._is_hash:
            if bleeding_edge and self._latest_hash:
                return self._latest_hash
            if latest_tag_hash:
                return latest_tag_hash
        return self._current_version
