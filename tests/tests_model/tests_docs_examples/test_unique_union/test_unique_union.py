import os
from pathlib import Path

from graphql2python.model.config import GraphQL2PythonModelConfig
from graphql2python.model.generate import Generator


def test_unique_union():
    schema_path = Path(os.path.join(os.path.dirname(__file__), "input.graphql"))
    output_path = Path(os.path.join(os.path.dirname(__file__), "output.py"))

    config = GraphQL2PythonModelConfig(schema=schema_path, output=output_path)

    generator = Generator(config)
    generator.generate()

    with output_path.open("r", encoding="utf-8") as f:
        output_file_text = f.read()

    assert output_file_text == '''"""Auto-generated by graphql2python."""

# pylint: disable-all
# mypy: ignore-errors

import enum
from datetime import date, datetime
from typing import Any, List, Literal, Optional, TypeVar, Union

from pydantic import BaseModel, Field

__all__ = [
    "GraphQLBaseModel",
    # scalars
    "Boolean",
    "ID",
    "Int",
    "String",
    # enums
    "Episode",
    # unions
    "SearchResult",
    # interfaces
    "Character",
    # objects
    "Human",
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


# The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID
# type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an
# input type, any string (such as `"4"`) or integer (such as `4`) input value will be accepted as an ID.
ID = str


# The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31)
# and 2^31 - 1.
Int = str


# The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most
# often used by GraphQL to represent free-form human-readable text.
String = str


class Episode(enum.Enum):
    """
    An Enum type
    See https://graphql.org/learn/schema/#enumeration-types
    """
    EMPIRE = "EMPIRE"
    JEDI = "JEDI"
    NEWHOPE = "NEWHOPE"


# A Union type
# See https://graphql.org/learn/schema/#union-types
SearchResult = TypeVar('SearchResult', bound='Human')


class Character(GraphQLBaseModel):
    """
    An Interface type
    See https://graphql.org/learn/schema/#interfaces
    """
    appearsIn: List[Optional['Episode']]
    id: 'ID'
    name: 'String'
    friends: Optional[List[Optional['Character']]] = Field(default_factory=list)


class Human(
    Character,
):
    """
    An Object type
    See https://graphql.org/learn/schema/#object-types-and-fields
    """
    totalCredits: Optional['Int'] = Field(default=None)
'''
