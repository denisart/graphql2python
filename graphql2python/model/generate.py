from enum import Enum
from typing import Dict, List, Set

from graphql import GraphQLNamedType, GraphQLSchema, build_schema, lexicographic_sort_schema
from graphql.type.introspection import TypeKind, TypeResolvers

from graphql2python.model.config import GraphQL2PythonModelConfig
from graphql2python.model.render import DataModelRender
from graphql2python.utils.graphlib import TopologicalSorter

__all__ = [
    "Generator",
]


resolver = TypeResolvers()


class SupportTypes(Enum):
    # pylint: disable=invalid-name
    GraphQLScalarType = "GraphQLScalarType"
    GraphQLObjectType = "GraphQLObjectType"
    GraphQLInterfaceType = "GraphQLInterfaceType"
    GraphQLUnionType = "GraphQLUnionType"
    GraphQLEnumType = "GraphQLEnumType"
    GraphQLInputObjectType = "GraphQLInputObjectType"


TYPES_MAPPER: Dict[TypeKind, SupportTypes] = {
    TypeKind.SCALAR: SupportTypes.GraphQLScalarType,
    TypeKind.OBJECT: SupportTypes.GraphQLObjectType,
    TypeKind.INTERFACE: SupportTypes.GraphQLInterfaceType,
    TypeKind.UNION: SupportTypes.GraphQLUnionType,
    TypeKind.ENUM: SupportTypes.GraphQLEnumType,
    TypeKind.INPUT_OBJECT: SupportTypes.GraphQLInputObjectType,
}


class GraphQLSchemaTypeMap:
    # pylint: disable=too-few-public-methods

    # GraphQL type --> list of object names
    type_map: Dict[SupportTypes, List[str]]

    # object name --> GraphQL object
    types: Dict[str, GraphQLNamedType]

    def build(self, schema: GraphQLSchema):
        self.type_map: Dict[SupportTypes, List[str]] = {
            SupportTypes.GraphQLUnionType: [],
            SupportTypes.GraphQLScalarType: [],
            SupportTypes.GraphQLObjectType: [],
            SupportTypes.GraphQLEnumType: [],
            SupportTypes.GraphQLInterfaceType: [],
            SupportTypes.GraphQLInputObjectType: [],
        }
        self.types: Dict[str, GraphQLNamedType] = {}

        for object_name, type_ in schema.type_map.items():
            if object_name.startswith("__"):
                continue

            if object_name in ["Query", "Mutation"]:
                continue

            resolved_type = resolver.kind(type_, None)

            self.type_map[TYPES_MAPPER[resolved_type]].append(object_name)
            self.types[object_name] = type_

        graph: Dict[str, Set[str]] = {}

        for object_name in self.type_map[SupportTypes.GraphQLInterfaceType]:
            graph[object_name] = {
                inter.name
                for inter in schema.get_type(object_name).interfaces  # type: ignore
            }

        t_sort = TopologicalSorter(graph)
        self.type_map[SupportTypes.GraphQLInterfaceType] = list(t_sort.static_order())


class Generator:
    """Generate GraphQL datamodel with pydantic from some GraphQL schema.

    Args:
        config: config for generate.

    """

    # pylint: disable=too-few-public-methods

    schema: GraphQLSchema
    type_map: GraphQLSchemaTypeMap
    config: GraphQL2PythonModelConfig
    render: DataModelRender

    DEFAULT_PYTYPE_FOR_SCALAR: str = "str"

    def __init__(self, config: GraphQL2PythonModelConfig):
        self.config = config

        with config.graphql_schema.open("r", encoding="utf8") as schema_file:
            schema_str = schema_file.read()

        self.schema = build_schema(schema_str)
        self.schema = lexicographic_sort_schema(self.schema)

        self.type_map = GraphQLSchemaTypeMap()
        self.type_map.build(self.schema)

        self.render = DataModelRender(
            max_line_len=config.options.max_line_len,
            name_suffix=config.options.name_suffix,
            each_field_optional=config.options.each_field_optional,
        )

    def _render_all_header(self) -> str:
        """Render of all header for output py file."""

        # GraphQLBaseModel -- an abstract class for some GraphQL object in datamodel
        result = '__all__ = [\n    "GraphQLBaseModel",\n'

        type_headers: Dict[SupportTypes, str] = {
            SupportTypes.GraphQLUnionType: "unions",
            SupportTypes.GraphQLScalarType: "scalars",
            SupportTypes.GraphQLObjectType: "objects",
            SupportTypes.GraphQLEnumType: "enums",
            SupportTypes.GraphQLInterfaceType: "interfaces",
            SupportTypes.GraphQLInputObjectType: "inputs",
        }

        for type_name in [
            SupportTypes.GraphQLScalarType,
            SupportTypes.GraphQLEnumType,
            SupportTypes.GraphQLUnionType,
            SupportTypes.GraphQLInterfaceType,
            SupportTypes.GraphQLObjectType,
            # SupportTypes.GraphQLInputObjectType,
        ]:
            result += f"    # {type_headers[type_name]}\n"

            for obj_name in self.type_map.type_map[type_name]:
                result += f'    "{obj_name}",\n'

        return result + "]"

    def _scalars_str(self) -> str:
        """Render all scalars."""

        scalar_strings: List[str] = []

        for scalar_name in self.type_map.type_map[SupportTypes.GraphQLScalarType]:
            obj = self.type_map.types[scalar_name]

            pytype = self.config.options.scalar_pytypes.get(obj.name, self.DEFAULT_PYTYPE_FOR_SCALAR)  # type: ignore

            scalar_strings.append(self.render.render_scalar(obj, pytype))  # type: ignore

        return "\n\n\n" + "\n\n\n".join(scalar_strings)

    def _enums_str(self) -> str:
        """Render all enums."""

        enum_strings: List[str] = []

        for enum_name in self.type_map.type_map[SupportTypes.GraphQLEnumType]:
            obj = self.type_map.types[enum_name]

            enum_strings.append(self.render.render_enum(obj))  # type: ignore

        if len(enum_strings) == 0:
            return ""

        return "\n\n\n" + "\n\n\n".join(enum_strings)

    def _unions_str(self) -> str:
        """Render all unions."""

        union_strings: List[str] = []

        for union_name in self.type_map.type_map[SupportTypes.GraphQLUnionType]:
            obj = self.type_map.types[union_name]

            union_strings.append(self.render.render_union(obj))  # type: ignore

        if len(union_strings) == 0:
            return ""

        return "\n\n\n" + "\n\n\n".join(union_strings)

    def _interfaces_str(self) -> str:
        """Render all unions."""

        interface_strings: List[str] = []

        for int_name in self.type_map.type_map[SupportTypes.GraphQLInterfaceType]:
            obj = self.type_map.types[int_name]

            field_aliases = self.config.options.fields_setting.get(int_name, {})

            interface_strings.append(self.render.render_interface(obj, field_aliases))  # type: ignore

        if len(interface_strings) == 0:
            return ""

        return "\n\n\n" + "\n\n\n".join(interface_strings)

    def _objects_str(self) -> str:
        """Render all objects."""

        object_strings: List[str] = []

        for obj_name in self.type_map.type_map[SupportTypes.GraphQLObjectType]:
            obj = self.type_map.types[obj_name]

            field_aliases = self.config.options.fields_setting.get(obj_name, {})

            object_strings.append(self.render.render_object(obj, field_aliases))  # type: ignore

        return "\n\n\n" + "\n\n\n".join(object_strings)

    def _update_forward_refs(self) -> str:
        """Render of update_forward_refs for each interface and for each object."""

        result = ""

        for type_name in [
            SupportTypes.GraphQLInterfaceType,
            SupportTypes.GraphQLObjectType,
        ]:
            for o_name in self.type_map.type_map[type_name]:
                result += f"{o_name}.update_forward_refs()\n"

        if result == "":
            return result

        return "\n\n\n" + result

    def generate(self):
        result_str = '"""Auto-generated by graphql2python."""\n\n# pylint: disable-all\n# mypy: ignore-errors\n\n'

        # TODO: add only used imports
        # TODO: add custom imports
        result_str += """import enum
import typing as _t
from datetime import date, datetime

from pydantic import BaseModel, Field"""

        result_str += "\n\n" + self._render_all_header()

        result_str += "\n\n\n" + self.render.render_general_class(
            add_from_dict=self.config.options.add_from_dict,
            add_to_dict=self.config.options.add_to_dict,
        )

        result_str += self._scalars_str()
        result_str += self._enums_str()
        result_str += self._unions_str()
        result_str += self._interfaces_str()
        result_str += self._objects_str()
        result_str += self._update_forward_refs()

        with self.config.output.open("w", encoding="utf-8") as output_file:
            output_file.write(result_str)
