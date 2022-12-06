import pytest
from jinja2 import Template

from graphql2python.model.render import template_env


@pytest.mark.parametrize(
    "template_name",
    [
        "comment.jinja2",
        "docstring.jinja2",
        "scalar.jinja2",
        "enum.jinja2",
        "union.jinja2",
        "interface.jinja2",
        "object.jinja2",
    ]
)
def test_exist_templates_for_model(template_name: str):
    tpl = template_env.get_template(template_name)
    assert isinstance(tpl, Template)
