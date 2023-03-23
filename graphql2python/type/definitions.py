from enum import Enum
from typing import List, Optional

from graphql import (
    GraphQLEnumType,
    GraphQLEnumValue,
    GraphQLField,
    GraphQLInterfaceType,
    GraphQLObjectType,
    GraphQLScalarType,
    GraphQLUnionType
)
from pydantic import BaseModel
from pydantic import Field as PydanticField

__all__ = [
    "GraphQL2PythonFieldSequenceItemType",
    "GraphQL2PythonScalarType",
    "GraphQL2PythonField",
    "GraphQL2PythonObject",
    "GraphQL2PythonInterfaceType",
    "GraphQL2PythonObjectType",
    "GraphQL2PythonEnumValue",
    "GraphQL2PythonEnumType",
    "GraphQL2PythonUnionType",
]


class GraphQL2PythonFieldSequenceItemType(str, Enum):
    """Supported types for field sequence."""

    # special token for sequence generation
    N = "N"
    # is list object
    L = "L"
    # is optional list object
    OL = "OL"
    # is object
    S = "S"
    # is optional object
    OS = "OS"


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


class GraphQL2PythonField(_GraphQL2PythonType):
    """A field type for graphql2python."""

    graphql_core: GraphQLField = PydanticField(
        description="This field in `graphql.GraphQLField` format."
    )
    description: Optional[str] = PydanticField(
        default=None, description="The same is `graphql.GraphQLField.description`."
    )
    deprecation_reason: Optional[str] = PydanticField(
        default=None, description="The same is `graphql.GraphQLField.deprecation_reason`."
    )
    name: str = PydanticField(description="A field name.")
    alias: Optional[str] = PydanticField(
        default=None, description="An alias for name of this field. Set by user."
    )
    public_name: Optional[str] = PydanticField(
        default=None, description="The public name of the field. Set by user."
    )
    field_object_name: str = PydanticField(
        description="A name of graphql output type in the field. `See graphql.GraphQLOutputType.name`."
    )
    field_object_alias: Optional[str] = PydanticField(
        default=None, description="An alias for name of a graphql output type in the field. Set by user."
    )
    field_sequence: List[GraphQL2PythonFieldSequenceItemType] = PydanticField(
        description="Split this field by special graphql2python tokens."
    )


class GraphQL2PythonObject(_GraphQL2PythonType):
    """An abstract class for GraphQL object: a type with fields."""

    name: str = PydanticField(description="The same is `graphql.GraphQLObjectType.name`.")
    description: Optional[str] = PydanticField(
        default=None, description="The same is `graphql.GraphQLObjectType.description`."
    )
    alias: Optional[str] = PydanticField(
        default=None, description="An alias for name of this object. Set by user."
    )
    fields: List[GraphQL2PythonField] = PydanticField(
        description="All fields for this object."
    )


class GraphQL2PythonInterfaceType(GraphQL2PythonObject):
    """An interface type for graphql2python."""

    graphql_core: GraphQLInterfaceType = PydanticField(
        description="This interface in `graphql.GraphQLInterfaceType` format."
    )
    interfaces: List[str] = PydanticField(
        description="Name of interfaces. See `graphql.GraphQLInterfaceType.interfaces`."
    )
    fields_from_interfaces: List[str] = PydanticField(
        description="Name of fields from each interface from `graphql.GraphQLInterfaceType.interfaces`."
    )


class GraphQL2PythonObjectType(GraphQL2PythonObject):
    """An object type for graphql2python."""

    graphql_core: GraphQLObjectType = PydanticField(
        description="This object in `graphql.GraphQLObjectType` format."
    )
    interfaces: List[str] = PydanticField(
        description="Name of interfaces. See `graphql.GraphQLObjectType.interfaces`."
    )
    fields_from_interfaces: List[str] = PydanticField(
        description="name of fields from each interface from `graphql.GraphQLObjectType.interfaces`."
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
