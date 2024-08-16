import re
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Optional, Tuple

import git
from git import GitCommandError
from packaging.version import InvalidVersion
from packaging.version import parse as parse_version

from ..repo import Repo
from . import MessageManager


class RepoManager:
    def __init__(
        self,
        repos_data: Dict,
        all_versions: bool,
        exclude: Tuple,
        keep: Tuple,
        bleeding_edge: Tuple,
    ) -> None:
        self._all_versions: bool = all_versions
        self._exclude: Tuple = exclude
        self._keep: Tuple = keep
        self._bleeding_edge: Tuple = bleeding_edge
        self._repos_data: Dict = repos_data
        self._repos_tags_and_hashes: List[Dict] = self._get_repos_tags_and_hashes()
        self._repos_latest_hashes: List = self._get_repos_latest_hash()
        self._repos_list: List[Repo] = self._get_repos_list()

    @property
    def repos_data(self) -> Dict:
        return self._repos_data

    @staticmethod
    def _get_repo_fixed_tags_and_hashes(tag_hash: Dict) -> Dict:
        # Due to various prefixes that devs choose for tags, strip them down to semantic version numbers only.
        # Store it inside the dict ("ver1.2.3": "1.2.3") and parse the value to get the correct sort.
        # Remove invalid suffixes ("-test", "-split", ...)
        # Return the original value (key) once everything is parsed/sorted.
        fixed_tags: Dict = {}
        for tag in tag_hash.keys():
            for prefix in re.findall("([a-zA-Z ]*)\\d*.*", tag):
                prefix = prefix.strip()
                try:
                    version: str = tag[len(prefix) :]
                    parse_version(version)
                    fixed_tags[tag] = version
                except InvalidVersion:
                    continue
        fixed_tags = {
            k: v
            for k, v in sorted(
                fixed_tags.items(),
                key=lambda item: parse_version(item[1]),
                reverse=True,
            )
        }
        return {k: tag_hash[k] for k in fixed_tags.keys()}

    def _get_repo_tags_and_hashes(self, repo: Dict) -> Dict:
        url: str = repo["repo"]
        if self._is_repo_excluded(url.split("/")[-1]):
            return {}
        try:
            remote_tags: List = (
                git.cmd.Git()
                .ls_remote("--exit-code", "--tags", url, sort="v:refname")
                .split("\n")
            )
            tag_hash: Dict = {}
            for tag in remote_tags:
                commit_hash, parsed_tag = re.split(r"\t+", tag)
                parsed_tag = parsed_tag.replace("refs/tags/", "").replace("^{}", "")
                tag_hash[parsed_tag] = commit_hash
            return tag_hash
        except GitCommandError as ex:
            if ex.status == 2:
                message = f"No tags found for repo: {url}"
            else:
                message = f"Failed to list tags for repo: {url}"
            raise Exception(message)

    def _get_repo_latest_hash(self, repo: Dict) -> Optional[str]:
        url: str = repo["repo"]
        if self._is_repo_excluded(url.split("/")[-1]):
            return None
        try:
            return (
                git.cmd.Git().ls_remote("--exit-code", repo["repo"], "HEAD").split()[0]
            )
        except Exception:
            return None

    def _get_repos_tags_and_hashes(self) -> List[Dict]:
        with ThreadPoolExecutor(max_workers=10) as pool:
            tasks: List = []
            for repo in self._repos_data:
                tasks.append(pool.submit(self._get_repo_tags_and_hashes, repo))
        for i, _ in enumerate(tasks):
            try:
                tasks[i] = self._get_repo_fixed_tags_and_hashes(tasks[i].result())
            except Exception:
                tasks[i] = {}
        return tasks

    def _get_repos_latest_hash(self) -> List[Optional[str]]:
        with ThreadPoolExecutor(max_workers=10) as pool:
            tasks: List = []
            for repo in self._repos_data:
                tasks.append(pool.submit(self._get_repo_latest_hash, repo))
        return tasks

    def _get_repos_list(self) -> List[Repo]:
        repo_list: List[Repo] = []
        for i, repo in enumerate(self._repos_data):
            repo_list.append(
                Repo(
                    repo=repo,
                    tags_and_hashes=self._repos_tags_and_hashes[i],
                    latest_hash=self._repos_latest_hashes[i].result(),
                    all_versions=self._all_versions,
                    bleeding_edge=self._is_repo_bleeding_edge(
                        repo["repo"].split("/")[-1]
                    ),
                )
            )
        return repo_list

    def _is_repo_excluded(self, repo_name: str) -> bool:
        return repo_name in self._exclude or self._exclude == ("*",)

    def _is_repo_kept(self, repo_name: str) -> bool:
        return repo_name in self._keep or self._keep == ("*",)

    def _is_repo_bleeding_edge(self, repo_name: str) -> bool:
        return repo_name in self._bleeding_edge or self._bleeding_edge == ("*",)

    def get_updates(self, messages: MessageManager) -> None:
        for i, repo in enumerate(self._repos_list):
            if repo.is_local:
                continue
            if not repo.has_tags_and_hashes and not self._is_repo_excluded(repo.name):
                messages.add_warning_message(repo.name, "0 tags/hashes fetched")
                continue
            if self._is_repo_excluded(repo.name):
                messages.add_excluded_message(repo.name, repo.current_version)
                continue
            if self._is_repo_kept(repo.name):
                messages.add_kept_message(
                    repo.name, repo.current_version, repo.latest_version
                )
                continue
            if repo.current_version != repo.latest_version:
                messages.add_to_update_message(
                    repo.name, repo.current_version, repo.latest_version
                )
                self._repos_data[i]["rev"] = repo.latest_version
                continue
            messages.add_no_update_message(repo.name, repo.current_version)
