from enum import Enum
from typing import List, Optional

from graphql import (GraphQLEnumType, GraphQLEnumValue, GraphQLField, GraphQLInputObjectType, GraphQLInterfaceType,
                     GraphQLObjectType, GraphQLScalarType, GraphQLUnionType)
from pydantic import BaseModel, Field

__all__ = [
    "GraphQL2PythonFieldSequenceItemType",
    "GraphQL2PythonType",
    "GraphQL2PythonScalarType",
    "GraphQL2PythonField",
    "GraphQL2PythonInterfaceType",
    "GraphQL2PythonObjectType",
    "GraphQL2PythonInputObjectType",
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


class GraphQL2PythonType(BaseModel):
    """Base class for all graphql2python types"""

    class Config:
        arbitrary_types_allowed = True
        smart_union = True


class GraphQL2PythonScalarType(GraphQL2PythonType):
    """A scalar type for graphql2python."""

    # this scalar in graphql.GraphQLScalarType format
    graphql_core: GraphQLScalarType
    # the same is graphql.GraphQLScalarType.name
    name: str
    # a string with python type name for this scalar. Set by user
    pytype: str
    # an alias for name of this scalar. Set by user
    alias: Optional[str] = Field(default=None)
    # the same is graphql.GraphQLScalarType.description
    description: Optional[str] = Field(default=None)


class GraphQL2PythonField(GraphQL2PythonType):
    """A field type for graphql2python."""

    # this field in graphql.GraphQLField format
    graphql_core: GraphQLField
    # a field name
    name: str
    # an alias for name of this field. Set by user
    alias: Optional[str] = Field(default=None)
    # the public name of the field. Set by user
    public_name: Optional[str] = Field(default=None)
    # a name of graphql output type in the field. See graphql.GraphQLOutputType.name
    field_object: str
    # an alias for name of a graphql output type in the field. Set by user
    field_object_alias: Optional[str] = Field(default=None)
    # split this field by special graphql2python tokens
    field_sequence: List[GraphQL2PythonFieldSequenceItemType]
    # the same is graphql.GraphQLField.description
    description: Optional[str] = Field(default=None)
    # the same is graphql.GraphQLField.deprecation_reason
    deprecation_reason: Optional[str] = Field(default=None)


class GraphQL2PythonInterfaceType(GraphQL2PythonType):
    """An interface type for graphql2python."""

    # this interface in graphql.GraphQLInterfaceType format
    graphql_core: GraphQLInterfaceType
    # the same is graphql.GraphQLInterfaceType.name
    name: str
    # an alias for name of this interface. Set by user
    alias: Optional[str] = Field(default=None)
    # the same is graphql.GraphQLInterfaceType.description
    description: Optional[str] = Field(default=None)
    # name of interfaces. See graphql.GraphQLInterfaceType.interfaces
    interfaces: List[str]
    # name of fields from each interface from graphql.GraphQLInterfaceType.interfaces
    fields_from_interfaces: List[str]
    # all fields for this interface
    fields: List[GraphQL2PythonField]


class GraphQL2PythonObjectType(GraphQL2PythonType):
    """An object type for graphql2python."""

    # this object in graphql.GraphQLObjectType format
    graphql_core: GraphQLObjectType
    # the same is graphql.GraphQLObjectType.name
    name: str
    # an alias for name of this object. Set by user
    alias: Optional[str] = Field(default=None)
    # the same is graphql.GraphQLObjectType.description
    description: Optional[str] = Field(default=None)
    # name of interfaces. See graphql.GraphQLObjectType.interfaces
    interfaces: List[str]
    # name of fields from each interface from graphql.GraphQLObjectType.interfaces
    fields_from_interfaces: List[str]
    # all fields for this object
    fields: List[GraphQL2PythonField]


class GraphQL2PythonInputObjectType(GraphQL2PythonType):
    """An input object type for graphql2python."""

    # this input object in graphql.GraphQLInputObjectType format
    graphql_core: GraphQLInputObjectType
    # the same is graphql.GraphQLInputObjectType.name
    name: str
    # an alias for name of this input object. Set by user
    alias: Optional[str] = Field(default=None)
    # the same is graphql.GraphQLInputObjectType.description
    description: Optional[str] = Field(default=None)
    # all fields for this input object
    fields: List[GraphQL2PythonField]


class GraphQL2PythonEnumValue(GraphQL2PythonType):
    """An enum value for graphql2python."""

    # this enum value in graphql.GraphQLEnumValue format
    graphql_core: GraphQLEnumValue
    # an enum value name. Set from graphql.GraphQLEnumType
    name: str
    # the same is graphql.GraphQLEnumValue.description
    description: Optional[str] = Field(default=None)
    # the same is graphql.GraphQLEnumValue.deprecation_reason
    deprecation_reason: Optional[str] = Field(default=None)


class GraphQL2PythonEnumType(GraphQL2PythonType):
    """An enum type for graphql2python."""

    # this enum in graphql.GraphQLEnumType format
    graphql_core: GraphQLEnumType
    # the same is graphql.GraphQLEnumType.name
    name: str
    # enum values. Created from graphql.GraphQLEnumType.values
    values: List[GraphQL2PythonEnumValue]
    # an alias for name of this enum. Set by user
    alias: Optional[str] = Field(default=None)
    # the same is graphql.GraphQLEnumType.description
    description: Optional[str] = Field(default=None)


class GraphQL2PythonUnionType(GraphQL2PythonType):
    """A union type for graphql2python."""

    # this union in graphql.GraphQLUnionType format
    graphql_core: GraphQLUnionType
    # the same is graphql.GraphQLUnionType.name
    name: str
    # name of union types. Created from graphql.GraphQLUnionType.types
    types: List[str]
    # an alias for name of this union. Set by user
    alias: Optional[str] = Field(default=None)
    # the same is graphql.GraphQLUnionType.description
    description: Optional[str] = Field(default=None)
