from pathlib import Path

import pytest
from jinja2 import Template

from graphql2python.template import TemplatesManager
from graphql2python.template.template import TEMPLATES_PYDANTIC


def test_invalid_template_name():
    manager = TemplatesManager()

    with pytest.raises(ValueError):
        _ = manager.get_template("unsupported-template-name")


def test_exist_default_templates():
    for template_name in TemplatesManager.supported_templates:
        template_file = TEMPLATES_PYDANTIC / Path(template_name)
        assert template_file.is_file()


def test_get_default_templates():
    for template_name in TemplatesManager.supported_templates:
        manager = TemplatesManager()
        tpl = manager.get_template(template_name)

        assert isinstance(tpl, Template)
