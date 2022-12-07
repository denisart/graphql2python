import os
from keyword import iskeyword
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from graphql import (GraphQLEnumType, GraphQLField, GraphQLInterfaceType, GraphQLObjectType, GraphQLScalarType,
                     GraphQLUnionType, is_list_type, is_non_null_type)
from jinja2 import Environment, FileSystemLoader, Template

from graphql2python.model.config import FieldSetting

__all__ = [
    "DataModelRender",
]


# templates setting for render of classes
TEMPLATES_FOLDER = Path(os.path.join(os.path.dirname(__file__), "templates/"))

template_env = Environment(loader=FileSystemLoader(searchpath=TEMPLATES_FOLDER))


class DataModelRender:
    """Render templates for GraphQL types.

    Args:
        max_line_len: maximum of line length.
        name_suffix: a suffix for invalid field name (as python object).
        each_field_optional: each field is optional.

    """

    _template_comment: Template = template_env.get_template("comment.jinja2")
    _template_docstring: Template = template_env.get_template("docstring.jinja2")
    _template_scalar: Template = template_env.get_template("scalar.jinja2")
    _template_enum: Template = template_env.get_template("enum.jinja2")
    _template_union: Template = template_env.get_template("union.jinja2")
    _template_interface: Template = template_env.get_template("interface.jinja2")
    _template_object: Template = template_env.get_template("object.jinja2")

    SCALAR_DEFAULT_DESCRIPTION = "A Scalar type\nSee https://graphql.org/learn/schema/#scalar-types"
    ENUM_DEFAULT_DESCRIPTION = "An Enum type\nSee https://graphql.org/learn/schema/#enumeration-types"
    UNION_DEFAULT_DESCRIPTION = "A Union type\nSee https://graphql.org/learn/schema/#union-types"
    INTERFACE_DEFAULT_DESCRIPTION = "An Interface type\nSee https://graphql.org/learn/schema/#interfaces"
    OBJECT_DEFAULT_DESCRIPTION = "An Object type\nSee https://graphql.org/learn/schema/#object-types-and-fields"

    def __init__(
        self,
        max_line_len: int = 120,
        name_suffix: str = "_",
        each_field_optional: bool = False,
    ):
        self.max_line_len = max_line_len
        self.name_suffix = name_suffix
        self.each_field_optional = each_field_optional

    @staticmethod
    def _line_shift(text: str, indent: int = 4) -> str:
        return ("\n" + " " * indent).join(text.split("\n"))

    @staticmethod
    def render_general_class(add_from_dict: bool, add_to_dict: bool) -> str:
        """Render the general class for each datamodel class.

        Args:
            add_from_dict: add from_dict method to the general class.
            add_to_dict: add to_dict method to the general class.

        """

        general_class = '''class GraphQLBaseModel(BaseModel):
    """Base Model for GraphQL object."""

    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            # custom output conversion for datetime
            datetime: lambda dt: dt.isoformat()
        }
        smart_union = True'''

        if add_from_dict:
            general_class += '''\n\n    @classmethod
    def from_dict(cls, obj: _t.Any):
        """Special wrapper over .parse_obj method."""
        return cls.parse_obj(obj)'''

        if add_to_dict:
            general_class += '''\n\n    def to_dict(self):
        """Special wrapper over .dict method."""
        return self.dict(by_alias=True)'''

        return general_class

    @staticmethod
    def processing_of_line(line: str, indent: int = 0, max_line_len: int = 120) -> List[str]:
        """Splitting a long string by space token.

        Args:
            line: some line.
            indent: the len of indent for each line.
            max_line_len: maximum of line length.

        """

        line_processed = []
        line_split = line.split(" ")

        temp = line_split[0]

        for word_id in range(1, len(line_split)):
            word = line_split[word_id]

            if len(temp) > (max_line_len - 2 - indent):
                line_processed.append(temp)
                temp = word

            else:
                if len(temp + word) + 1 <= (max_line_len - 2 - indent):
                    temp = " ".join([temp, word])
                else:
                    line_processed.append(temp)
                    temp = word

        line_processed.append(temp)

        return line_processed

    def render_comment(self, lines: List[str], indent: int = 0, max_line_len: int = 120) -> str:
        """Render multiline comment with `comment.jinja2` template.

        Args:
            lines: comment lines.
            indent: the len of indent for each line.
            max_line_len: the max of line length.

        """

        if len(lines) == 0:
            lines.append("...")

        processed_lines: List[str] = []

        for line in lines:
            separated_lines = line.split("\n")

            for line_from_separated_lines in separated_lines:
                processed_lines += self.processing_of_line(line_from_separated_lines, indent, max_line_len)

        return self._template_comment.render(indent=" " * indent, lines=processed_lines)[:-1]

    def render_docstring(self, lines: List[str], indent: int = 0, max_line_len: int = 120) -> str:
        """Render multiline docstring with `docstring.jinja2` template.

        Args:
            lines: comment lines.
            indent: the len of indent for each line.
            max_line_len: the max of line length.

        """

        if len(lines) == 0:
            lines.append("...")

        processed_lines: List[str] = []

        for line in lines:
            separated_lines = line.split("\n")

            for line_from_separated_lines in separated_lines:
                processed_lines += self.processing_of_line(line_from_separated_lines, indent - 2, max_line_len)

        return self._template_docstring.render(indent=" " * indent, lines=processed_lines)

    def render_scalar(self, obj: GraphQLScalarType, pytype: str) -> str:
        """Render scalar with `scalar.jinja2` template.

        Args:
            obj: scalar object for render.
            pytype: python type name for this scalar.

        """

        name = obj.name
        description = self.render_comment(
            (obj.description or self.SCALAR_DEFAULT_DESCRIPTION).split("\n"),
            max_line_len=self.max_line_len
        )

        return self._template_scalar.render(description=description, name=name, pytype=pytype)

    def render_enum(self, obj: GraphQLEnumType) -> str:
        """Render enum with `enum.jinja2` template.

        Args:
            obj: enum object for render.

        """

        name = obj.name
        docstring = self.render_docstring(
            (obj.description or self.ENUM_DEFAULT_DESCRIPTION).split("\n"),
            indent=4,
            max_line_len=self.max_line_len
        )

        #
        # for render of values with template
        # v_name, v, desc, dpr --> value_name, value, description, deprecation_reason
        #
        values: List[Tuple[str, str, Optional[str], Optional[str]]] = []

        for value_name, value in obj.values.items():  # type: ignore
            name_suffix = ""

            # for invalid name of python token
            if iskeyword(value_name):
                name_suffix = self.name_suffix

            v_name = name_suffix + value_name

            value_from_value = value.value or value_name
            if isinstance(value_from_value, (int, float)):
                v = str(value_from_value)  # pylint: disable=invalid-name
            else:
                v = f'"{str(value_from_value)}"'  # pylint: disable=invalid-name

            v_description = None
            if value.description is not None:
                v_description = self.render_comment(value.description.split("\n"))

            v_deprecated = None
            if value.deprecation_reason is not None:
                v_deprecated = value.deprecation_reason

            values.append((v_name, v, v_description, v_deprecated))

        return self._template_enum.render(docstring=docstring, name=name, values=values)

    def render_union(self, obj: GraphQLUnionType) -> str:
        """Render union with `union.jinja2` template.

        Args:
            obj: union object for render.

        """

        name = obj.name
        description = self.render_comment(
            (obj.description or self.UNION_DEFAULT_DESCRIPTION).split('\n'),
            max_line_len=self.max_line_len
        )
        types = [type_.name for type_ in obj.types]  # type: ignore

        return self._template_union.render(description=description, name=name, types=types)

    def render_field_type(self, field: GraphQLField, alias: Optional[str] = None) -> str:
        """Render a type of some GraphQL field."""

        # pylint: disable=too-many-statements,too-many-branches

        obj = field.type
        result = ""

        #
        # tokens:
        # None -- is start
        # L -- is list
        # OL -- is not optional (non null) list
        # N -- is not optional (non null)
        # S -- is scalar or other object
        # OS -- is not optional (non null) scalar or other object
        #
        # transitions:
        # None --> OS, OL
        # L --> OL, OS
        # OL --> OL, OS
        # N --> S, L
        # S -- is final
        # OS -- is final
        #

        # previous token
        prev_token: Optional[str] = None
        # result list with tokens
        res_list: List[str] = []

        while is_list_type(obj) or is_non_null_type(obj):

            if is_list_type(obj):
                if (prev_token is None) or (prev_token in ["L", "OL"]):
                    res_list.append("OL")
                    prev_token = "OL"
                else:
                    res_list.append("L")
                    prev_token = "L"

            elif is_non_null_type(obj):
                prev_token = "N"

            obj = obj.of_type  # type: ignore

        final_name = obj.name  # type: ignore

        if (prev_token is None) or (prev_token in ["L", "OL"]):
            res_list.append("OS")
        else:
            res_list.append("S")

        # check that the field is optional
        if self.each_field_optional:
            if res_list[0] == "S":
                res_list[0] = "OS"

            elif res_list[0] == "L":
                res_list[0] = "OL"

        alias_field = ""
        if alias is not None:
            alias_field = f", alias='{alias}'"

        if len(res_list) == 1:
            is_optional = res_list[0] == "OS"

            def_value = ""
            if is_optional:
                def_value = "default=None"

            field_options = ""
            if is_optional or alias:
                if def_value == "":
                    def_value = "..."

                field_options = f' = Field({def_value}{alias_field})'

            if res_list[0] == 'OS':
                result += f"_t.Optional['{final_name}']"
            elif res_list[0] == 'S':
                result += f"'{final_name}'"
            else:
                raise ValueError

            result += field_options

        else:
            is_optional = res_list[0] == 'OL'

            def_value = ''
            if is_optional:
                def_value = 'default_factory=list'

            field_options = ''
            if is_optional or alias:
                if def_value == '':
                    def_value = '...'

                field_options = f' = Field({def_value}{alias_field})'

            end_brace = 0
            for key_id in range(len(res_list) - 1):
                if res_list[key_id] == 'OL':
                    result += '_t.Optional[_t.List['
                    end_brace += 2

                else:
                    result += '_t.List['
                    end_brace += 1

            if res_list[-1] == 'OS':
                result += f"_t.Optional['{final_name}']"
            else:
                result += f"'{final_name}'"

            result += ']' * end_brace

            result += field_options

        return result

    def render_field(
        self,
        field_name: str,
        field: GraphQLField,
        alias: Optional[str] = None,
        new_name: Optional[str] = None,
    ) -> str:
        """Render a GraphQL field.

        Args:
            field_name: field name.
            field: field object for render.
            alias: pydantic alias for field.
            new_name: new field name.

        """

        if new_name is not None:
            field_name = new_name

        name_suffix = ""

        # for invalid name of python token
        if iskeyword(field_name):
            name_suffix = self.name_suffix

        result = ""

        if field.description is not None:
            result += self.render_comment(
                field.description.split('\n'),
                indent=4,
                max_line_len=self.max_line_len
            ) + "\n"

        result += f"    {field_name}{name_suffix}: "

        result += self.render_field_type(field, alias)

        if field.deprecation_reason is not None:
            result += f'  # deprecation_reason: {field.deprecation_reason}'

        return result

    def render_interface(self, obj: GraphQLInterfaceType, field_aliases: Dict[str, FieldSetting]) -> str:
        """Render an interface with `interface.jinja2` template.

        Args:
            obj: interface object for render.
            field_aliases: aliases for the interface field.

        """

        docstring = self.render_docstring(
            indent=4,
            lines=[obj.description or self.INTERFACE_DEFAULT_DESCRIPTION],
            max_line_len=self.max_line_len
        )

        interfaces = [
            int_name.name
            for int_name in obj.interfaces  # type: ignore
        ]

        parents = set()

        for interface in obj.interfaces:  # type: ignore
            for f_name, _ in interface.fields.items():
                parents.add(f_name)

        fields_optional = []
        fields_required = []

        for f_name, f in obj.fields.items():  # pylint: disable=invalid-name
            if f_name in parents:
                continue

            if is_non_null_type(f.type):
                if self.each_field_optional:
                    fields_optional.append(f_name)
                else:
                    fields_required.append(f_name)
            else:
                fields_optional.append(f_name)

        field_names = fields_required + fields_optional

        fields = []
        for f_name in field_names:  # type: ignore
            alias = None
            new_name = None

            if f_name in field_aliases:
                alias = field_aliases[f_name].alias
                new_name = field_aliases[f_name].new_name

            fields.append(
                self.render_field(
                    f_name,
                    obj.fields[f_name],  # type: ignore
                    alias=alias,
                    new_name=new_name,
                )
            )

        return self._template_interface.render(
                docstring=docstring,
                name=obj.name,
                interfaces=interfaces,
                fields=fields,
        )

    def render_object(self, obj: GraphQLObjectType, field_aliases: Dict[str, FieldSetting]) -> str:
        """Render an object with `object.jinja2` template.

        Args:
            obj: object for render.
            field_aliases: aliases for the interface field in
                the following format:
                    Dict[
                        object_name,
                        {
                            field_name: {
                                "alias": Optional[str],
                                "new_name": Optional[str],
                            }
                        }
                    ]

        """

        docstring = self.render_docstring(
            indent=4,
            lines=[obj.description or self.OBJECT_DEFAULT_DESCRIPTION],
            max_line_len=self.max_line_len
        )

        interfaces = [
            int_name.name
            for int_name in obj.interfaces  # type: ignore
        ]

        parents = set()
        for interface in obj.interfaces:  # type: ignore
            for f_name, _ in interface.fields.items():
                parents.add(f_name)

        fields_optional = []
        fields_required = []

        for f_name, f in obj.fields.items():  # pylint: disable=invalid-name
            if f_name in parents:
                continue

            if is_non_null_type(f.type):
                if self.each_field_optional:
                    fields_optional.append(f_name)
                else:
                    fields_required.append(f_name)
            else:
                fields_optional.append(f_name)

        field_names = fields_required + fields_optional

        fields = []
        for f_name in field_names:
            alias = None
            new_name = None

            if f_name in field_aliases:
                alias = field_aliases[f_name].alias
                new_name = field_aliases[f_name].new_name

            fields.append(
                self.render_field(
                    f_name,
                    obj.fields[f_name],  # type: ignore
                    alias,
                    new_name,
                )
            )

        return self._template_object.render(
            docstring=docstring,
            name=obj.name,
            interfaces=interfaces,
            fields=fields,
        )
