from graphql import GraphQLField, GraphQLInterfaceType, GraphQLNonNull, GraphQLScalarType

from graphql2python.model.config import FieldSetting
from graphql2python.model.render import DataModelRender

render = DataModelRender()


def test_render_interface_simple():
    """Test for render of simple GraphQL interface with aliases."""

    field_aliases = {
        'f1': FieldSetting(alias='f1_alias'),
        'f3': FieldSetting(new_name='f3_new')
    }

    obj = GraphQLInterfaceType(
        'I',
        fields={
            'f1': GraphQLField(GraphQLScalarType('String')),
            'f2': GraphQLField(GraphQLScalarType('String')),
            'f3': GraphQLField(GraphQLScalarType('String')),
            'from': GraphQLField(GraphQLScalarType('String')),
        },
        description='my description',
    )

    result = '''class I(GraphQLBaseModel):
    """
    my description
    """
    f1: Optional['String'] = Field(default=None, alias='f1_alias')
    f2: Optional['String'] = Field(default=None)
    f3_new: Optional['String'] = Field(default=None)
    from_: Optional['String'] = Field(default=None)'''

    assert render.render_interface(obj, field_aliases) == result


def test_render_interface_not_all_optional():
    """Test for render of simple GraphQL interface with optional_fields=False."""

    field_aliases = {
        'f1': FieldSetting(alias='f1_alias'),
        'f3': FieldSetting(new_name='f3_new')
    }

    obj = GraphQLInterfaceType(
        'I',
        fields={
            'f1': GraphQLField(GraphQLScalarType('String')),
            'f2': GraphQLField(GraphQLNonNull(GraphQLScalarType('String'))),
            'f3': GraphQLField(GraphQLScalarType('String')),
            'from': GraphQLField(GraphQLScalarType('String')),
        },
        description='my description',
    )

    result = '''class I(GraphQLBaseModel):
    """
    my description
    """
    f2: 'String'
    f1: Optional['String'] = Field(default=None, alias='f1_alias')
    f3_new: Optional['String'] = Field(default=None)
    from_: Optional['String'] = Field(default=None)'''

    assert render.render_interface(obj, field_aliases) == result


def test_render_interface_all_optional():
    """Test for render of simple GraphQL interface with optional_fields=True."""

    field_aliases = {
        'f1': FieldSetting(alias='f1_alias'),
        'f3': FieldSetting(new_name='f3_new'),
    }

    obj = GraphQLInterfaceType(
        'I',
        fields={
            'f1': GraphQLField(GraphQLScalarType('String')),
            'f2': GraphQLField(GraphQLNonNull(GraphQLScalarType('String'))),
            'f3': GraphQLField(GraphQLScalarType('String')),
            'from': GraphQLField(GraphQLScalarType('String')),
        },
        description='my description',
    )

    result = '''class I(GraphQLBaseModel):
    """
    my description
    """
    f1: Optional['String'] = Field(default=None, alias='f1_alias')
    f2: Optional['String'] = Field(default=None)
    f3_new: Optional['String'] = Field(default=None)
    from_: Optional['String'] = Field(default=None)'''

    render_optional = DataModelRender(each_field_optional=True)
    assert render_optional.render_interface(obj, field_aliases) == result


def test_render_interface_inherit():
    """Test of an interface render with inherit."""

    obj = GraphQLInterfaceType(
        'I',
        fields={
            'f1': GraphQLField(GraphQLScalarType('String')),
        },
        interfaces=[
            GraphQLInterfaceType('I1', {}),
            GraphQLInterfaceType('I2', {}),
            GraphQLInterfaceType('I3', {})
        ]
    )

    result = '''class I(
    I1,
    I2,
    I3,
):
    """
    An Interface type
    See https://graphql.org/learn/schema/#interfaces
    """
    f1: Optional['String'] = Field(default=None)'''

    assert render.render_interface(obj, {}) == result
