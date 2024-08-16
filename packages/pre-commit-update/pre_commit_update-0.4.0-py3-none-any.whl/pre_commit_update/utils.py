import os
from typing import Dict

import click
import tomli


class RepoType(click.types.StringParamType):
    name = "repo_url_trim"


def get_color(text: str, color: str) -> str:
    return click.style(str(text), fg=color)


def get_passed_params(ctx: click.Context) -> Dict:
    return {
        k: v
        for k, v in ctx.params.items()
        if ctx.get_parameter_source(k) == click.core.ParameterSource.COMMANDLINE
    }


def get_toml_config(defaults: Dict) -> Dict:
    try:
        with open(os.path.join(os.getcwd(), "pyproject.toml"), "rb") as f:
            toml_dict: Dict = tomli.load(f)
        return {**defaults, **toml_dict["tool"]["pre-commit-update"]}
    except (FileNotFoundError, KeyError):
        return defaults


def get_dict_diffs(d1: Dict, d2: Dict) -> Dict:
    return {k: d2[k] for k in d2 if d2[k] != d1[k]}
