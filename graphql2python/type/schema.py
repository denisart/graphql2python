from typing import Dict, List, Optional, Tuple

from graphql import (GraphQLEnumType, GraphQLEnumValue, GraphQLField, GraphQLInputObjectType, GraphQLInterfaceType,
                     GraphQLObjectType, GraphQLScalarType, GraphQLSchema, GraphQLUnionType, is_enum_type,
                     is_input_object_type, is_interface_type, is_list_type, is_non_null_type, is_object_type,
                     is_scalar_type, is_union_type)

from .definition import (GraphQL2PythonEnumType, GraphQL2PythonEnumValue, GraphQL2PythonField,
                         GraphQL2PythonFieldSequenceItemType, GraphQL2PythonInputObjectType,
                         GraphQL2PythonInterfaceType, GraphQL2PythonObjectType, GraphQL2PythonScalarType,
                         GraphQL2PythonType, GraphQL2PythonUnionType)

__all__ = [
    "GraphQL2PythonSchema",
]


class GraphQL2PythonSchema:
    """A graphql schema for graphql2python. It is a special format for
     convenient render of result.

    Args:
        schema: target GraphQL schema in graphql-core format.
        aliases: aliases for GraphQL objects in the following format:
            Dict[object_name, alias].
        fields_aliases: aliases for fields of GraphQL objects in the
            following format:
            Dict[object_name, Dict[fields_name, {"alias": "...", "public_name": "..."}]].
        scalar_definitions: scalar definitions for result file:
            Dict[scalar_name, python_type]. Default it is DEFAULT_SCALAR_DEFINITION.
        force_optional: each field will be optional.

    """

    DEFAULT_SCALAR_DEFINITION = "str"

    def __init__(
        self,
        schema: GraphQLSchema,
        aliases: Dict[str, str],
        fields_aliases: Dict[str, Dict[str, Dict[str, str]]],
        scalar_definitions: Dict[str, str],
        force_optional: bool,
    ):
        """Initialization of graphql2python schema."""

        # a graphql schema in graphql.GraphQLSchema format
        self.schema = schema
        # mapper from name to a GraphQL2PythonType object
        self.type_map: Dict[str, GraphQL2PythonType] = {}

        self.aliases = aliases
        self.fields_aliases = fields_aliases
        self.scalar_definitions = scalar_definitions

        self.force_optional = force_optional

        self.graphql_scalar_types: List[GraphQL2PythonScalarType] = []
        self.graphql_interface_types: List[GraphQL2PythonInterfaceType] = []
        self.graphql_object_types: List[GraphQL2PythonObjectType] = []
        self.graphql_input_object_types: List[GraphQL2PythonInputObjectType] = []
        self.graphql_enum_types: List[GraphQL2PythonEnumType] = []
        self.graphql_union_types: List[GraphQL2PythonUnionType] = []

    @staticmethod
    def _graphql2python_enum_value_type(
        enum_value_type: GraphQLEnumValue,
        enum_value_name: str
    ) -> GraphQL2PythonEnumValue:
        return GraphQL2PythonEnumValue(
            graphql_core=enum_value_type,
            name=enum_value_name,
            description=enum_value_type.description,
            deprecation_reason=enum_value_type.deprecation_reason
        )

    def _field_processing(self, field_object: GraphQLField) -> Tuple[
        List[GraphQL2PythonFieldSequenceItemType],
        str
    ]:
        obj = field_object.type

        # transitions:
        # None --> OS, OL
        # L --> OL, OS
        # OL --> OL, OS
        # N --> S, L
        # S -- is final
        # OS -- is final
        #

        # previous token
        prev_token: Optional[GraphQL2PythonFieldSequenceItemType] = None
        # result list with tokens
        result_list: List[GraphQL2PythonFieldSequenceItemType] = []

        while is_list_type(obj) or is_non_null_type(obj):

            if is_list_type(obj):
                if (
                    (prev_token is None) or
                    (prev_token in [GraphQL2PythonFieldSequenceItemType.L, GraphQL2PythonFieldSequenceItemType.OL])
                ):
                    result_list.append(GraphQL2PythonFieldSequenceItemType.OL)
                    prev_token = GraphQL2PythonFieldSequenceItemType.OL
                else:
                    result_list.append(GraphQL2PythonFieldSequenceItemType.L)
                    prev_token = GraphQL2PythonFieldSequenceItemType.L

            elif is_non_null_type(obj):
                prev_token = GraphQL2PythonFieldSequenceItemType.N

            obj = obj.of_type  # type: ignore

        if (
            (prev_token is None) or
            (prev_token in [GraphQL2PythonFieldSequenceItemType.L, GraphQL2PythonFieldSequenceItemType.OL])
        ):
            result_list.append(GraphQL2PythonFieldSequenceItemType.OS)
        else:
            result_list.append(GraphQL2PythonFieldSequenceItemType.S)

        # check that the field is optional
        if self.force_optional:
            if result_list[0] == GraphQL2PythonFieldSequenceItemType.S:
                result_list[0] = GraphQL2PythonFieldSequenceItemType.OS
            elif result_list[0] == GraphQL2PythonFieldSequenceItemType.L:
                result_list[0] = GraphQL2PythonFieldSequenceItemType.OL

        return result_list, obj.name

    def _graphql2python_scalar_type(self, scalar_type: GraphQLScalarType) -> GraphQL2PythonScalarType:
        return GraphQL2PythonScalarType(
            graphql_core=scalar_type,
            name=scalar_type.name,
            pytype=self.scalar_definitions.get(scalar_type.name, self.DEFAULT_SCALAR_DEFINITION),
            alias=self.aliases.get(scalar_type.name, None),
            description=scalar_type.description,
        )

    def _graphql2python_enum_type(self, enum_type: GraphQLEnumType) -> GraphQL2PythonEnumType:
        return GraphQL2PythonEnumType(
            graphql_core=enum_type,
            name=enum_type.name,
            values=[
                self._graphql2python_enum_value_type(value_type, value_name)
                for value_name, value_type in enum_type.values.items()
            ],
            alias=self.aliases.get(enum_type.name, None),
            description=enum_type.description
        )

    def _graphql2python_union_type(self, union_type: GraphQLUnionType) -> GraphQL2PythonUnionType:
        return GraphQL2PythonUnionType(
            graphql_core=union_type,
            name=union_type.name,
            types=[object_type.name for object_type in union_type.types],
            alias=self.aliases.get(union_type.name, None),
            description=union_type.description
        )

    def _field_info(self, field_name: str, parent_object_name: str) -> Tuple[Optional[str], Optional[str]]:
        field_alias = None
        public_name = None

        if (
            (self.fields_aliases.get(parent_object_name, None) is not None) and
            (field_name in self.fields_aliases.get(parent_object_name, None))
        ):
            setting = self.fields_aliases[parent_object_name][field_name]

            field_alias = setting.get("alias", None)
            public_name = setting.get("public_name", None)

        return field_alias, public_name

    def _graphql2python_field_type(
        self,
        field_type: GraphQLField,
        field_name: str,
        parent_object_name: str,
    ) -> GraphQL2PythonField:
        field_alias, public_name = self._field_info(field_name, parent_object_name)
        field_sequence, field_object_name = self._field_processing(field_type)

        return GraphQL2PythonField(
            graphql_core=field_type,
            name=field_name,
            alias=field_alias,
            public_name=public_name,
            field_object=field_object_name,
            field_object_alias=self.aliases.get(field_object_name, None),
            field_sequence=field_sequence,
            description=field_type.description,
            deprecation_reason=field_type.deprecation_reason,
        )

    def _graphql2python_interface_type(
        self,
        interface_type: GraphQLInterfaceType,
    ) -> GraphQL2PythonInterfaceType:
        fields_from_interfaces = []
        for i in interface_type.interfaces:
            fields_from_interfaces = fields_from_interfaces + [key for key, _ in i.fields.items()]

        return GraphQL2PythonInterfaceType(
            graphql_core=interface_type,
            name=interface_type.name,
            alias=self.aliases.get(interface_type.name, None),
            description=interface_type.description,
            interfaces=[i.name for i in interface_type.interfaces],
            fields_from_interfaces=fields_from_interfaces,
            fields=[
                self._graphql2python_field_type(f_type, f_name, interface_type.name)
                for f_name, f_type in interface_type.fields.items()
            ]
        )

    def _graphql2python_object_type(
        self,
        object_type: GraphQLObjectType,
    ) -> GraphQL2PythonObjectType:
        fields_from_interfaces = []
        for i in object_type.interfaces:
            fields_from_interfaces = fields_from_interfaces + [key for key, _ in i.fields.items()]

        return GraphQL2PythonObjectType(
            graphql_core=object_type,
            name=object_type.name,
            alias=self.aliases.get(object_type.name, None),
            description=object_type.description,
            interfaces=[i.name for i in object_type.interfaces],
            fields_from_interfaces=fields_from_interfaces,
            fields=[
                self._graphql2python_field_type(f_type, f_name, object_type.name)
                for f_name, f_type in object_type.fields.items()
            ]
        )

    def _graphql2python_input_object_type(
        self,
        input_object_type: GraphQLInputObjectType
    ) -> GraphQL2PythonInputObjectType:
        # return GraphQL2PythonInputObjectType(
        #     graphql_core=input_object_type,
        #     name=input_object_type.name,
        #     alias=self.aliases.get(input_object_type.name, None),
        #     description=input_object_type.description,
        #     fields=[
        #         self._graphql2python_field_type(f_type, f_name, input_object_type.name)
        #         for f_name, f_type in input_object_type.fields.items()
        #     ]
        # )
        pass

    def build(self):
        for object_name, type_ in self.schema.type_map.items():
            if object_name.startswith("__"):
                continue

            if object_name in ["Query", "Mutation"]:
                continue

            graphql2python_type_ = None

            if is_scalar_type(type_):
                graphql2python_type_ = self._graphql2python_scalar_type(type_)  # type: ignore
                self.graphql_scalar_types.append(graphql2python_type_)

            if is_enum_type(type_):
                graphql2python_type_ = self._graphql2python_enum_type(type_)  # type: ignore
                self.graphql_enum_types.append(graphql2python_type_)

            if is_union_type(type_):
                graphql2python_type_ = self._graphql2python_union_type(type_)  # type: ignore
                self.graphql_union_types.append(graphql2python_type_)

            if is_interface_type(type_):
                graphql2python_type_ = self._graphql2python_interface_type(type_)  # type: ignore
                self.graphql_interface_types.append(graphql2python_type_)

            if is_object_type(type_):
                graphql2python_type_ = self._graphql2python_object_type(type_)  # type: ignore
                self.graphql_object_types.append(graphql2python_type_)

            if is_input_object_type(type_):
                graphql2python_type_ = self._graphql2python_input_object_type(type_)  # type: ignore
                self.graphql_input_object_types.append(graphql2python_type_)

            if graphql2python_type_ is not None:
                self.type_map[type_.name] = graphql2python_type_
