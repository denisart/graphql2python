from typing import Optional

import pytest
from graphql import GraphQLScalarType

from graphql2python.template import TemplatesManager


@pytest.mark.parametrize(
    "scalar_object, pytype, alias, result",
    [
        # a scalar
        (GraphQLScalarType("ID"), "str", None, "ID = str"),
        # a scalar with description
        (GraphQLScalarType("ID", description="My scalar"), "str", None, "# My scalar\nID = str"),
        # a scalar with alias
        (GraphQLScalarType("ID"), "str", "MyID", "MyID = str"),
        # a scalar with description and with alias
        (GraphQLScalarType("ID", description="My scalar"), "str", "MyID", "# My scalar\nMyID = str"),
        # full
        (
            GraphQLScalarType("ID", description="It is long description\nfor my scalar"),
            "str", "MyID", "# It is long description\n# for my scalar\nMyID = str"
        ),
    ]
)
def test_scalar_object_pydantic(
    scalar_object: GraphQLScalarType,
    pytype: str,
    alias: Optional[str],
    result: str
):
    manager = TemplatesManager()
    assert manager.render_scalar(
        scalar_object=scalar_object,
        pytype=pytype,
        alias=alias,
    ) == result
