import pytest
from graphql import GraphQLEnumType, GraphQLEnumValue

from graphql2python.model.render import DataModelRender

render = DataModelRender()


@pytest.mark.parametrize(
    "obj, result",
    [
        (
            GraphQLEnumType('MyEnum', {'f1': 'f1', 'f2': 'f2'}),
            '''class MyEnum(enum.Enum):
    """
    An Enum type
    See https://graphql.org/learn/schema/#enumeration-types
    """
    f1 = "f1"
    f2 = "f2"''',
        ),
        (
            GraphQLEnumType(
                "MyEnum",
                {"f1": GraphQLEnumValue(description="field description", deprecation_reason="my reason")},
                description='my description',
            ),
            '''class MyEnum(enum.Enum):
    """
    my description
    """
    # field description
    f1 = "f1"  # deprecation_reason: my reason''',
        ),
    ],
)
def test_render_enum(obj: GraphQLEnumType, result: str):
    """Tests for an enum render with some options."""
    assert render.render_enum(obj) == result
