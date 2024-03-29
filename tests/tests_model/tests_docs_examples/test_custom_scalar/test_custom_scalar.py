import os
from pathlib import Path

from graphql2python.model.config import GraphQL2PythonModelConfig, GraphQL2PythonModelOptions
from graphql2python.model.generate import Generator


def test_custom_scalar():
    schema_path = Path(os.path.join(os.path.dirname(__file__), "input.graphql"))
    output_path = Path(os.path.join(os.path.dirname(__file__), "output.py"))

    config = GraphQL2PythonModelConfig(
        schema=schema_path, output=output_path, options=GraphQL2PythonModelOptions(scalar_pytypes={"Date": "date"})
    )

    generator = Generator(config)
    generator.generate()

    with output_path.open("r", encoding="utf-8") as f:
        output_file_text = f.read()

    assert (
        output_file_text
        == '''"""Auto-generated by graphql2python."""

# pylint: disable-all
# mypy: ignore-errors

import enum
import typing as _t
from datetime import date, datetime

from pydantic import BaseModel, Field

__all__ = [
    "GraphQLBaseModel",
    # scalars
    "Boolean",
    "Date",
    "Float",
    "ID",
    "String",
    # enums
    # unions
    # interfaces
    # objects
    "Starship",
]


class GraphQLBaseModel(BaseModel):
    """Base Model for GraphQL object."""

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            # custom output conversion for datetime
            datetime: lambda dt: dt.isoformat()
        }
        smart_union = True


# The `Boolean` scalar type represents `true` or `false`.
Boolean = str


# A Scalar type
# See https://graphql.org/learn/schema/#scalar-types
Date = date


# The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE
# 754](https://en.wikipedia.org/wiki/IEEE_floating_point).
Float = str


# The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID
# type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an
# input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.
ID = str


# The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most
# often used by GraphQL to represent free-form human-readable text.
String = str


class Starship(GraphQLBaseModel):
    """
    An Object type
    See https://graphql.org/learn/schema/#object-types-and-fields
    """
    id: 'ID'
    name: 'String'
    length: _t.Optional['Float'] = Field(default=None)
    typename__: _t.Literal["Starship"] = Field(default="Starship", alias="__typename")


Starship.update_forward_refs()
'''
    )
