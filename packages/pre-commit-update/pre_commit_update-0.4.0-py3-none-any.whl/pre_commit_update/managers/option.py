from typing import List, Set, Tuple

from . import MessageManager


class OptionManager:
    def __init__(
        self,
        warnings: bool,
        all_versions: bool,
        exclude: Tuple,
        keep: Tuple,
        bleeding_edge: Tuple,
        repo_trims: Set,
    ) -> None:
        self._warnings: bool = warnings
        self._all_versions: bool = all_versions
        self._exclude: List = list(sorted(exclude))
        self._keep: List = list(sorted(keep))
        self._bleeding_edge: List = list(sorted(bleeding_edge))
        self._repo_trims: Set = repo_trims

    @property
    def exclude(self) -> Tuple:
        return tuple(self._exclude)

    @property
    def keep(self) -> Tuple:
        return tuple(self._keep)

    @property
    def bleeding_edge(self) -> Tuple:
        return tuple(self._bleeding_edge)

    @staticmethod
    def _remove_list_element(lst: List, element: str) -> None:
        if element in lst:
            lst.remove(element)

    def _validate_invalid_repo_trims(self, message_manager: MessageManager) -> None:
        all_option_trims: Set = set(self._exclude + self._keep + self._bleeding_edge)
        for trim in all_option_trims - self._repo_trims:
            if trim == "*":
                continue
            self._remove_list_element(self._exclude, trim)
            self._remove_list_element(self._keep, trim)
            self._remove_list_element(self._bleeding_edge, trim)
            message_manager.add_warning_message(trim, "invalid repo trim (ignored)")

    def _validate_wildcards(self, message_manager: MessageManager) -> None:
        if "*" in self._exclude:
            for trim in [t for t in self._exclude if t != "*"]:
                message_manager.add_warning_message(
                    trim,
                    "--exclude option obsolete (--exclude *)",
                )
            self._exclude = ["*"]
            for trim in self._keep:
                message_manager.add_warning_message(
                    trim,
                    "--keep option ignored (--exclude *)",
                )
            self._keep = []
            for trim in self._bleeding_edge:
                message_manager.add_warning_message(
                    trim,
                    "--bleeding-edge option ignored (--exclude *)",
                )
            self._bleeding_edge = []
            return
        if "*" in self._keep:
            for trim in [t for t in self._keep if t != "*"]:
                message_manager.add_warning_message(
                    trim,
                    "--keep option obsolete (--keep *)",
                )
            self._keep = ["*"]
            for trim in self._exclude:
                message_manager.add_warning_message(
                    trim,
                    "--exclude option ignored (--keep *)",
                )
            self._exclude = []
            for trim in self._bleeding_edge:
                message_manager.add_warning_message(
                    trim,
                    "--bleeding-edge option ignored (--keep *)",
                )
            self._bleeding_edge = []
            return
        if "*" in self._bleeding_edge:
            for trim in [t for t in self._bleeding_edge if t != "*"]:
                message_manager.add_warning_message(
                    trim,
                    "--bleeding-edge option obsolete (--bleeding-edge *)",
                )
            self._bleeding_edge = ["*"]
            for trim in self._exclude:
                message_manager.add_warning_message(
                    trim,
                    "--exclude option ignored (--bleeding-edge *)",
                )
            self._exclude = []
            for trim in self._keep:
                message_manager.add_warning_message(
                    trim,
                    "--keep option ignored (--bleeding-edge *)",
                )
            self._keep = []
            return

    def _validate_repeating_repo_trims(self, message_manager: MessageManager) -> None:
        for trim in self._exclude:
            if trim == "*":
                self._remove_list_element(self._keep, "*")
                self._remove_list_element(self._bleeding_edge, "*")
                continue
            match: List = []
            if trim in self._keep:
                self._remove_list_element(self._keep, trim)
                match.append("--keep")
            if trim in self._bleeding_edge:
                self._remove_list_element(self._bleeding_edge, trim)
                match.append("--bleeding-edge")
            if not match:
                continue
            message_manager.add_warning_message(
                trim,
                f"{', '.join(match)} option{'s' if len(match) == 2 else ''} ignored (--exclude)",
            )
        for trim in self._keep:
            if trim == "*":
                self._remove_list_element(self._bleeding_edge, "*")
                continue
            if trim in self._bleeding_edge:
                self._remove_list_element(self._bleeding_edge, trim)
                message_manager.add_warning_message(
                    trim,
                    "--bleeding-edge option ignored (--keep)",
                )

    def _validate_bleeding_edge(self, message_manager: MessageManager) -> None:
        if self._all_versions:
            return
        for trim in [t for t in self._bleeding_edge if t != "*"]:
            message_manager.add_warning_message(
                trim, "--all-versions option ignored (--bleeding-edge)"
            )

    def validate(self, message_manager: MessageManager) -> None:
        self._validate_invalid_repo_trims(message_manager)
        self._validate_repeating_repo_trims(message_manager)
        self._validate_wildcards(message_manager)
        self._validate_bleeding_edge(message_manager)
