from typing import Optional, List

from graphql import (
    GraphQLScalarType,
    GraphQLEnumType,
    GraphQLEnumValue,
    GraphQLUnionType,
)
from pydantic import BaseModel, Field as PydanticField

__all__ = [
    "GraphQL2PythonScalarType",
    "GraphQL2PythonEnumValue",
    "GraphQL2PythonEnumType",
    "GraphQL2PythonUnionType",
]


class _GraphQL2PythonType(BaseModel):
    """A base class for all graphql2python types."""

    class Config:
        arbitrary_types_allowed = True
        smart_union = True


#
# GraphQL schema types
#
class GraphQL2PythonScalarType(_GraphQL2PythonType):
    """A scalar type for graphql2python."""

    graphql_core: GraphQLScalarType = PydanticField(
        description="This scalar in `graphql.GraphQLScalarType` format."
    )
    name: str = PydanticField(
        description="The same is `graphql.GraphQLScalarType.name`."
    )
    description: Optional[str] = PydanticField(
        default=None, description="The same is `graphql.GraphQLScalarType.description`."
    )
    pytype: str = PydanticField(
        description="A string with python type name for this scalar. Set by user."
    )
    alias: Optional[str] = PydanticField(
        default=None, description="An alias for name of this scalar. Set by user."
    )


class GraphQL2PythonEnumValue(_GraphQL2PythonType):
    """An enum value for graphql2python."""

    graphql_core: GraphQLEnumValue = PydanticField(
        description="This enum value in `graphql.GraphQLEnumValue` format."
    )
    name: str = PydanticField(description="An enum value name. Set from `graphql.GraphQLEnumType`.")
    description: Optional[str] = PydanticField(
        default=None, description="The same is `graphql.GraphQLEnumValue.description`."
    )
    deprecation_reason: Optional[str] = PydanticField(
        default=None, description="The same is `graphql.GraphQLEnumValue.deprecation_reason`."
    )


class GraphQL2PythonEnumType(_GraphQL2PythonType):
    """An enum type for graphql2python."""

    graphql_core: GraphQLEnumType = PydanticField(description="This enum in `graphql.GraphQLEnumType` format.")
    name: str = PydanticField(description="The same is `graphql.GraphQLEnumType.name`.")
    values: List[GraphQL2PythonEnumValue] = PydanticField(
        description="Enum values. Created from `graphql.GraphQLEnumType.values`."
    )
    alias: Optional[str] = PydanticField(
        default=None, description="An alias for name of this enum. Set by user."
    )
    description: Optional[str] = PydanticField(
        default=None, description="The same is `graphql.GraphQLEnumType.description`."
    )


class GraphQL2PythonUnionType(_GraphQL2PythonType):
    """A union type for graphql2python."""

    graphql_core: GraphQLUnionType = PydanticField(
        description="This union in `graphql.GraphQLUnionType` format."
    )
    name: str = PydanticField(
        description="The same is `graphql.GraphQLUnionType.name`."
    )
    description: Optional[str] = PydanticField(
        default=None, description="The same is `graphql.GraphQLUnionType.description`."
    )
    types: List[str] = PydanticField(
        description="A name of union types. Created from `graphql.GraphQLUnionType.types`."
    )
    alias: Optional[str] = PydanticField(
        default=None, description="An alias for name of this union. Set by user."
    )
