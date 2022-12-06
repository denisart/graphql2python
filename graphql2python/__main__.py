import os
from pathlib import Path

import click
import yaml

from graphql2python.model.config import GraphQL2PythonModelConfig
from graphql2python.model.generate import Generator


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

    with config_path.open("r", encoding="utf-8") as config_file:
        yaml_config = yaml.safe_load(config_file)

    if ("schema" not in yaml_config) or ("output" not in yaml_config):
        raise ValueError("Missing config fields: schema or output.")

    yaml_config["schema"] = (cwd_path / Path(yaml_config["schema"])).resolve()
    yaml_config["output"] = (cwd_path / Path(yaml_config["output"])).resolve()

    graphql2python_config = GraphQL2PythonModelConfig.parse_obj(yaml_config)

    generator = Generator(graphql2python_config)
    generator.generate()


graphql2python = cli = click.CommandCollection(sources=[model_cli])


if __name__ == "__main__":
    graphql2python()
