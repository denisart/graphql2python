import os
from pathlib import Path

import pytest

from graphql2python.model.config import GraphQL2PythonModelConfig

static_folder = Path(os.path.join(os.path.dirname(__file__), "static/"))


@pytest.mark.parametrize(
    "input_file",
    (
        static_folder,
        static_folder / "schema.txt",
        static_folder / "un_exist_schema.graphql",
    )
)
def test_schema_validation_raises(input_file: str):
    with pytest.raises(ValueError):
        GraphQL2PythonModelConfig(
            schema=input_file,
            output=static_folder / "output_file.py"
        )


def test_schema_validation_correct():
    config = GraphQL2PythonModelConfig(
        schema=Path(static_folder / "example.graphql"),
        output=static_folder / "output_file.py"
    )

    assert isinstance(config.graphql_schema, Path)
