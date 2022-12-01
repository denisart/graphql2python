from pydantic import BaseModel, Field

__all__ = [
    "GraphQL2PythonModelOptions",
    "GraphQL2PythonModelConfig",
]


class GraphQL2PythonModelOptions(BaseModel):
    """Data-model render options."""

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

    schema: str = Field(description="A path to the target GraphQL schema file.")
    output: str = Field(description="A path to an output python file.")
    options: GraphQL2PythonModelOptions = Field(
        description="Data-model render options.", default=GraphQL2PythonModelOptions()
    )
