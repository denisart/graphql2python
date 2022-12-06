import os
from pathlib import Path
from typing import Optional

import click
import yaml

from graphql2python.model.config import GraphQL2PythonModelConfig
from graphql2python.model.generate import Generator


class YamlLoadError(Exception):
    """An exception for load error of yaml file."""


def load_yaml(filename: str, encoding: Optional[str] = None):
    """Load some yaml file."""

    try:
        with open(filename, 'r', encoding=encoding) as fh:
            return yaml.safe_load(fh)

    except (OSError, yaml.YAMLError, UnicodeDecodeError) as error:
        if encoding is None:
            # try with default encoding UTF-8
            return load_yaml(filename, encoding='utf-8')

        raise YamlLoadError(f'Load Yaml failed: {error}') from error


@click.group()
def model_cli():
    """CLI for graphql2python.model."""


@model_cli.command()
@click.option(
    "-c",
    "--config",
    help="GraphQL2Python model config.",
)
def generate(config: str):
    """Generate pydantic data-model."""

    cwd_path = Path(os.getcwd())
    config_path = (cwd_path / Path(config)).resolve()

    with config_path.open("r", encoding="utf-8") as fh:
        yaml_config = yaml.safe_load(fh)

    if ("schema" not in yaml_config) or ("output" not in yaml_config):
        raise ValueError("Missing config fields: schema or output.")

    yaml_config["schema"] = (cwd_path / Path(yaml_config["schema"])).resolve()
    yaml_config["output"] = (cwd_path / Path(yaml_config["output"])).resolve()

    config = GraphQL2PythonModelConfig.parse_obj(yaml_config)

    generator = Generator(config)
    generator.generate()


graphql2python = cli = click.CommandCollection(sources=[model_cli])


if __name__ == "__main__":
    graphql2python()
