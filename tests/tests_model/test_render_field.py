import pytest
from graphql import (GraphQLEnumType, GraphQLField, GraphQLInterfaceType, GraphQLList, GraphQLNonNull,
                     GraphQLObjectType, GraphQLScalarType, GraphQLUnionType)

from graphql2python.model.render import DataModelRender

render = DataModelRender()


@pytest.mark.parametrize(
    'field_name, field, result',
    [
        (
            'f', GraphQLField(type_=GraphQLScalarType('S')),
            "    f: Optional['S'] = Field(default=None)"
        ),
        (
            'f', GraphQLField(type_=GraphQLNonNull(GraphQLScalarType('S'))),
            "    f: 'S'"
        ),
        (
            'f', GraphQLField(type_=GraphQLList(GraphQLScalarType('S'))),
            "    f: Optional[List[Optional['S']]] = Field(default_factory=list)"
        ),
        (
            'f', GraphQLField(type_=GraphQLNonNull(GraphQLList(GraphQLScalarType('S')))),
            "    f: List[Optional['S']]"
        ),
        (
            'f', GraphQLField(type_=GraphQLList(GraphQLNonNull(GraphQLScalarType('S')))),
            "    f: Optional[List['S']] = Field(default_factory=list)"
        ),
        (
            'f', GraphQLField(type_=GraphQLNonNull(GraphQLList(GraphQLNonNull(GraphQLScalarType('S'))))),
            "    f: List['S']"
        ),
        (
            'f', GraphQLField(type_=GraphQLList(GraphQLList(GraphQLScalarType('S')))),
            "    f: Optional[List[Optional[List[Optional['S']]]]] = Field(default_factory=list)"
        ),
    ]
)
def test_render_field_scalar(field_name: str, field: GraphQLField, result: str):
    """Test of field render with a scalar."""
    assert render.render_field(field_name, field) == result


@pytest.mark.parametrize(
    'field_name, field, result',
    [
        (
            'f', GraphQLField(type_=GraphQLEnumType('S', {})),  # type: ignore
            "    f: Optional['S'] = Field(default=None)"
        ),
        (
            'f', GraphQLField(type_=GraphQLNonNull(GraphQLEnumType('S', {}))),  # type: ignore
            "    f: 'S'"
        ),
        (
            'f', GraphQLField(type_=GraphQLList(GraphQLEnumType('S', {}))),  # type: ignore
            "    f: Optional[List[Optional['S']]] = Field(default_factory=list)"
        ),
        (
            'f', GraphQLField(type_=GraphQLNonNull(GraphQLList(GraphQLEnumType('S', {})))),  # type: ignore
            "    f: List[Optional['S']]"
        ),
        (
            'f', GraphQLField(type_=GraphQLList(GraphQLNonNull(GraphQLEnumType('S', {})))),  # type: ignore
            "    f: Optional[List['S']] = Field(default_factory=list)"
        ),
        (
            'f',
            GraphQLField(type_=GraphQLNonNull(GraphQLList(GraphQLNonNull(GraphQLEnumType('S', {}))))),  # type: ignore
            "    f: List['S']"
        ),
        (
            'f', GraphQLField(type_=GraphQLList(GraphQLList(GraphQLEnumType('S', {})))),  # type: ignore
            "    f: Optional[List[Optional[List[Optional['S']]]]] = Field(default_factory=list)"
        ),
    ]
)
def test_render_field_enum(field_name: str, field: GraphQLField, result: str):
    """Test of field render with an enum."""
    assert render.render_field(field_name, field) == result


@pytest.mark.parametrize(
    'field_name, field, result',
    [
        (
            'f', GraphQLField(type_=GraphQLUnionType('S', [])),
            "    f: Optional['S'] = Field(default=None)"
        ),
        (
            'f', GraphQLField(type_=GraphQLNonNull(GraphQLUnionType('S', []))),
            "    f: 'S'"
        ),
        (
            'f', GraphQLField(type_=GraphQLList(GraphQLUnionType('S', []))),
            "    f: Optional[List[Optional['S']]] = Field(default_factory=list)"
        ),
        (
            'f', GraphQLField(type_=GraphQLNonNull(GraphQLList(GraphQLUnionType('S', [])))),
            "    f: List[Optional['S']]"
        ),
        (
            'f', GraphQLField(type_=GraphQLList(GraphQLNonNull(GraphQLUnionType('S', [])))),
            "    f: Optional[List['S']] = Field(default_factory=list)"
        ),
        (
            'f', GraphQLField(type_=GraphQLNonNull(GraphQLList(GraphQLNonNull(GraphQLUnionType('S', []))))),
            "    f: List['S']"
        ),
        (
            'f', GraphQLField(type_=GraphQLList(GraphQLList(GraphQLUnionType('S', [])))),
            "    f: Optional[List[Optional[List[Optional['S']]]]] = Field(default_factory=list)"
        ),
    ]
)
def test_render_field_union(field_name: str, field: GraphQLField, result: str):
    """Test of field render with a union."""
    assert render.render_field(field_name, field) == result


@pytest.mark.parametrize(
    'field_name, field, result',
    [
        (
            'f',
            GraphQLField(type_=GraphQLUnionType('S', [GraphQLObjectType('F', ())])),  # type: ignore
            "    f: Optional['S'] = Field(default=None)"
        ),
        (
            'f',
            GraphQLField(type_=GraphQLNonNull(GraphQLUnionType('S', [GraphQLObjectType('F', ())]))),  # type: ignore
            "    f: 'S'"
        ),
        (
            'f',
            GraphQLField(type_=GraphQLList(GraphQLUnionType('S', [GraphQLObjectType('F', ())]))),  # type: ignore
            "    f: Optional[List[Optional['S']]] = Field(default_factory=list)"
        ),
        (
            'f',
            GraphQLField(
                type_=GraphQLNonNull(GraphQLList(GraphQLUnionType('S', [GraphQLObjectType('F', ())])))),  # type: ignore
            "    f: List[Optional['S']]"
        ),
        (
            'f',
            GraphQLField(
                type_=GraphQLList(
                    GraphQLNonNull(GraphQLUnionType('S', [GraphQLObjectType('F', ())]))  # type: ignore
                )
            ),
            "    f: Optional[List['S']] = Field(default_factory=list)"
        ),
        (
            'f',
            GraphQLField(
                type_=GraphQLNonNull(
                    GraphQLList(GraphQLNonNull(GraphQLUnionType('S', [GraphQLObjectType('F', ())])))  # type: ignore
                )
            ),
            "    f: List['S']"
        ),
        (
            'f',
            GraphQLField(
                type_=GraphQLList(
                    GraphQLList(GraphQLUnionType('S', [GraphQLObjectType('F', ())]))  # type: ignore
                )
            ),
            "    f: Optional[List[Optional[List[Optional['S']]]]] = Field(default_factory=list)"
        ),
    ]
)
def test_render_field_union_one(field_name: str, field: GraphQLField, result: str):
    """Test of field render with a union."""
    assert render.render_field(field_name, field) == result


@pytest.mark.parametrize(
    'field_name, field, result',
    [
        (
            'f', GraphQLField(type_=GraphQLInterfaceType('S', {})),
            "    f: Optional['S'] = Field(default=None)"
        ),
        (
            'f', GraphQLField(type_=GraphQLNonNull(GraphQLInterfaceType('S', {}))),
            "    f: 'S'"
        ),
        (
            'f', GraphQLField(type_=GraphQLList(GraphQLInterfaceType('S', {}))),
            "    f: Optional[List[Optional['S']]] = Field(default_factory=list)"
        ),
        (
            'f', GraphQLField(type_=GraphQLNonNull(GraphQLList(GraphQLInterfaceType('S', {})))),
            "    f: List[Optional['S']]"
        ),
        (
            'f', GraphQLField(type_=GraphQLList(GraphQLNonNull(GraphQLInterfaceType('S', {})))),
            "    f: Optional[List['S']] = Field(default_factory=list)"
        ),
        (
            'f', GraphQLField(type_=GraphQLNonNull(GraphQLList(GraphQLNonNull(GraphQLInterfaceType('S', {}))))),
            "    f: List['S']"
        ),
        (
            'f', GraphQLField(type_=GraphQLList(GraphQLList(GraphQLInterfaceType('S', {})))),
            "    f: Optional[List[Optional[List[Optional['S']]]]] = Field(default_factory=list)"
        ),
    ]
)
def test_render_field_interface(field_name: str, field: GraphQLField, result: str):
    """Test of field render with an interface."""
    assert render.render_field(field_name, field) == result


@pytest.mark.parametrize(
    'field_name, field, result',
    [
        (
            'f', GraphQLField(type_=GraphQLObjectType('S', {})),
            "    f: Optional['S'] = Field(default=None)"
        ),
        (
            'f', GraphQLField(type_=GraphQLNonNull(GraphQLObjectType('S', {}))),
            "    f: 'S'"
        ),
        (
            'f', GraphQLField(type_=GraphQLList(GraphQLObjectType('S', {}))),
            "    f: Optional[List[Optional['S']]] = Field(default_factory=list)"
        ),
        (
            'f', GraphQLField(type_=GraphQLNonNull(GraphQLList(GraphQLObjectType('S', {})))),
            "    f: List[Optional['S']]"
        ),
        (
            'f', GraphQLField(type_=GraphQLList(GraphQLNonNull(GraphQLObjectType('S', {})))),
            "    f: Optional[List['S']] = Field(default_factory=list)"
        ),
        (
            'f', GraphQLField(type_=GraphQLNonNull(GraphQLList(GraphQLNonNull(GraphQLObjectType('S', {}))))),
            "    f: List['S']"
        ),
        (
            'f', GraphQLField(type_=GraphQLList(GraphQLList(GraphQLObjectType('S', {})))),
            "    f: Optional[List[Optional[List[Optional['S']]]]] = Field(default_factory=list)"
        ),
    ]
)
def test_render_field_object(field_name: str, field: GraphQLField, result: str):
    """Test of field render with an object."""
    assert render.render_field(field_name, field) == result


def test_render_field_new_name():
    """Test of render a field with new name."""

    f_name = 'f'
    field = GraphQLField(type_=GraphQLScalarType('S'))

    result = "    new_f: Optional['S'] = Field(default=None)"

    assert render.render_field(f_name, field, new_name='new_f') == result


def test_render_field_suffix():
    """Test of render a field with invalid name."""

    f_name = 'from'
    field = GraphQLField(type_=GraphQLScalarType('S'))

    result = "    from_: Optional['S'] = Field(default=None)"

    assert render.render_field(f_name, field) == result


def test_render_field_deprecated():
    """Test of render a field with deprecated reason."""

    f_name = 'f'
    field = GraphQLField(type_=GraphQLScalarType('S'), deprecation_reason='my reason')

    result = "    f: Optional['S'] = Field(default=None)  # deprecation_reason: my reason"

    assert render.render_field(f_name, field) == result


def test_render_field_description():
    """Test of render a field with description."""

    f_name = 'f'
    field = GraphQLField(type_=GraphQLScalarType('S'), description='my description')

    result = "    # my description\n    f: Optional['S'] = Field(default=None)"

    assert render.render_field(f_name, field) == result


@pytest.mark.parametrize(
    'field_name, field, result',
    [
        (
            'f', GraphQLField(type_=GraphQLScalarType('S')),
            "    f: Optional['S'] = Field(default=None, alias='alias_f')"
        ),
        (
            'f', GraphQLField(type_=GraphQLNonNull(GraphQLScalarType('S'))),
            "    f: 'S' = Field(..., alias='alias_f')"
        ),
        (
            'f', GraphQLField(type_=GraphQLList(GraphQLScalarType('S'))),
            "    f: Optional[List[Optional['S']]] = Field(default_factory=list, alias='alias_f')"
        ),
        (
            'f', GraphQLField(type_=GraphQLNonNull(GraphQLList(GraphQLScalarType('S')))),
            "    f: List[Optional['S']] = Field(..., alias='alias_f')"
        ),
        (
            'f', GraphQLField(type_=GraphQLList(GraphQLNonNull(GraphQLScalarType('S')))),
            "    f: Optional[List['S']] = Field(default_factory=list, alias='alias_f')"
        ),
        (
            'f', GraphQLField(type_=GraphQLNonNull(GraphQLList(GraphQLNonNull(GraphQLScalarType('S'))))),
            "    f: List['S'] = Field(..., alias='alias_f')"
        ),
        (
            'f', GraphQLField(type_=GraphQLList(GraphQLList(GraphQLScalarType('S')))),
            "    f: Optional[List[Optional[List[Optional['S']]]]] = Field(default_factory=list, alias='alias_f')"
        ),
    ]
)
def test_render_field_scalar_alias(field_name: str, field: GraphQLField, result: str):
    """Tests for render of a field with alias."""
    assert render.render_field(field_name, field, alias='alias_f') == result
