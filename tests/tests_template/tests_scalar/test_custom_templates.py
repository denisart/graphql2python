from pathlib import Path
from graphql2python.template import TemplatesManager
from graphql import GraphQLScalarType


def test_custom_templates():
    custom_dir = Path(__file__).parent / Path("data/custom_templates")
    manager = TemplatesManager(custom_template_dir=custom_dir)

    assert manager.render_scalar(
        scalar_object=GraphQLScalarType("ID", description="123"),
        pytype="str",
        extra_template_data={"scalar_docs_url": "https://graphql.org/learn/schema/#scalar-types"}
    ) == """# A Scalar type. See https://graphql.org/learn/schema/#scalar-types
ID = str"""
