from graphql import GraphQLField, GraphQLInterfaceType, GraphQLNonNull, GraphQLObjectType, GraphQLScalarType

from graphql2python.model.render import DataModelRender, FieldSetting

render = DataModelRender()


def test_render_object_simple():
    """Test for render of simple GraphQL object with aliases."""

    field_aliases = {
        'f1': FieldSetting(alias='f1_alias'),
        'f3': FieldSetting(new_name='f3_new'),
    }

    obj = GraphQLObjectType(
        'O',
        fields={
            'f1': GraphQLField(GraphQLScalarType('String')),
            'f2': GraphQLField(GraphQLScalarType('String')),
            'f3': GraphQLField(GraphQLScalarType('String')),
            'from': GraphQLField(GraphQLScalarType('String')),
        },
        description='my description',
    )

    result = '''class O(GraphQLBaseModel):
    """
    my description
    """
    f1: _t.Optional['String'] = Field(default=None, alias='f1_alias')
    f2: _t.Optional['String'] = Field(default=None)
    f3_new: _t.Optional['String'] = Field(default=None)
    from_: _t.Optional['String'] = Field(default=None)
    typename__: _t.Literal["O"] = Field(default="O", alias="__typename")'''

    assert render.render_object(obj, field_aliases) == result


def test_render_object_not_all_optional():
    """Test for render of simple GraphQL object with optional_fields=False."""

    field_aliases = {
        'f1': FieldSetting(alias='f1_alias'),
        'f3': FieldSetting(new_name='f3_new'),
    }

    obj = GraphQLObjectType(
        'O',
        fields={
            'f1': GraphQLField(GraphQLScalarType('String')),
            'f2': GraphQLField(GraphQLNonNull(GraphQLScalarType('String'))),
            'f3': GraphQLField(GraphQLScalarType('String')),
            'from': GraphQLField(GraphQLScalarType('String')),
        },
        description='my description',
    )

    result = '''class O(GraphQLBaseModel):
    """
    my description
    """
    f2: 'String'
    f1: _t.Optional['String'] = Field(default=None, alias='f1_alias')
    f3_new: _t.Optional['String'] = Field(default=None)
    from_: _t.Optional['String'] = Field(default=None)
    typename__: _t.Literal["O"] = Field(default="O", alias="__typename")'''

    assert render.render_object(obj, field_aliases) == result


def test_render_object_all_optional():
    """Test for render of simple GraphQL object with optional_fields=True."""

    field_aliases = {
        'f1': FieldSetting(alias='f1_alias'),
        'f3': FieldSetting(new_name='f3_new'),
    }

    obj = GraphQLObjectType(
        'O',
        fields={
            'f1': GraphQLField(GraphQLScalarType('String')),
            'f2': GraphQLField(GraphQLNonNull(GraphQLScalarType('String'))),
            'f3': GraphQLField(GraphQLScalarType('String')),
            'from': GraphQLField(GraphQLScalarType('String')),
        },
        description='my description',
    )

    result = '''class O(GraphQLBaseModel):
    """
    my description
    """
    f1: _t.Optional['String'] = Field(default=None, alias='f1_alias')
    f2: _t.Optional['String'] = Field(default=None)
    f3_new: _t.Optional['String'] = Field(default=None)
    from_: _t.Optional['String'] = Field(default=None)
    typename__: _t.Literal["O"] = Field(default="O", alias="__typename")'''

    render_optional = DataModelRender(each_field_optional=True)
    assert render_optional.render_object(obj, field_aliases) == result


def test_render_object_inherit():
    """Test of an object render with inherit."""

    obj = GraphQLObjectType(
        'O',
        fields={
            'f1': GraphQLField(GraphQLScalarType('String')),
        },
        interfaces=[
            GraphQLInterfaceType('I1', {}),
            GraphQLInterfaceType('I2', {}),
            GraphQLInterfaceType('I3', {})
        ]
    )

    result = '''class O(
    I1,
    I2,
    I3,
):
    """
    An Object type
    See https://graphql.org/learn/schema/#object-types-and-fields
    """
    f1: _t.Optional['String'] = Field(default=None)
    typename__: _t.Literal["O"] = Field(default="O", alias="__typename")'''

    assert render.render_object(obj, {}) == result
