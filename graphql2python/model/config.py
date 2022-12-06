from pathlib import Path
from typing import Dict, Optional

from pydantic import BaseModel, Field, validator

__all__ = [
    "FieldSetting",
    "GraphQL2PythonModelOptions",
    "GraphQL2PythonModelConfig",
]


class FieldSetting(BaseModel):
    alias: Optional[str] = Field(default=None)
    new_name: Optional[str] = Field(default=None)


class GraphQL2PythonModelOptions(BaseModel):
    """Data-model render options."""

    scalar_pytypes: Dict[str, str] = Field(
        description="Python types for custom GraphQL scalars.",
        default_factory=dict
    )
    fields_setting: Dict[str, Dict[str, FieldSetting]] = Field(
        description="Settings for interfaces or objects fields.",
        default_factory=dict
    )
    max_line_len: int = Field(default=120, description="Maximum of line length of output python file.")
    name_suffix: str = Field(default="_", description="A suffix for invalid field name (as python object name).")
    each_field_optional: bool = Field(
        default=False,
        description="Each fields of interfaces and objects are optional."
    )
    add_from_dict: bool = Field(default=False, description="add from_dict method to the general class.")
    add_to_dict: bool = Field(default=False, description="add to_dict method to the general class.")


class GraphQL2PythonModelConfig(BaseModel):
    """GraphQL2Python config for pydantic data-model generation."""

    graphql_schema: Path = Field(description="A path to the target GraphQL schema file.", alias="schema")
    output: Path = Field(description="A path to an output python file.")
    options: GraphQL2PythonModelOptions = Field(
        description="Data-model render options.", default=GraphQL2PythonModelOptions()
    )

    @validator("graphql_schema")
    def validation_graphql_schema_file(cls, schema_path: Path):
        if not schema_path.exists():
            raise ValueError(f"The file {schema_path} is not exist.")

        if not schema_path.is_file():
            raise ValueError("The input schema is not file.")

        if schema_path.suffix != ".graphql":
            raise ValueError("The input file must have the suffix is .graphql")

        return schema_path

    @validator("output")
    def validation_output_py_file(cls, output_path: Path):
        if output_path.suffix != ".py":
            raise ValueError("The output file must have the suffix is .py")

        return output_path
