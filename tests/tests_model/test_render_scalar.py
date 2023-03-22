import pytest
from graphql import GraphQLScalarType

from graphql2python.model.render import DataModelRender

render = DataModelRender()


@pytest.mark.parametrize(
    "obj, pytype, result",
    [
        (
            GraphQLScalarType("ID"),
            "str",
            "# A Scalar type\n# See https://graphql.org/learn/schema/#scalar-types\nID = str",
        ),
        (GraphQLScalarType("ID", description="my description"), "str", "# my description\nID = str"),
    ],
)
def test_render_scalar(obj: GraphQLScalarType, pytype: str, result: str):
    """Tests for scalar render with some options."""
    assert render.render_scalar(obj, pytype) == result
