import pytest
from graphql import GraphQLObjectType, GraphQLUnionType

from graphql2python.model.render import DataModelRender

render = DataModelRender()


@pytest.mark.parametrize(
    "obj, result",
    [
        (
            GraphQLUnionType(
                'MyUnion',
                types=[GraphQLObjectType('MyObject1', {}), GraphQLObjectType('MyObject2', {})]
            ),
            """# A Union type
# See https://graphql.org/learn/schema/#union-types
MyUnion = Union[
    'MyObject1',
    'MyObject2',
]"""
        ),
        (
            GraphQLUnionType(
                'MyUnion',
                types=[GraphQLObjectType('MyObject1', {}), GraphQLObjectType('MyObject2', {})],
                description='my description'
            ),
            "# my description\nMyUnion = Union[\n    'MyObject1',\n    'MyObject2',\n]"
        ),
        (
            GraphQLUnionType(
                'MyUnion',
                types=[GraphQLObjectType('MyObject1', {})],
                description='my description'
            ),
            "# my description\nMyUnion = TypeVar('MyUnion', bound='MyObject1')"
        ),
    ]
)
def test_render_union(obj: GraphQLUnionType, result: str):
    """Tests for a union render with some options."""
    assert render.render_union(obj) == result
