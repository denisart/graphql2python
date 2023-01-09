from pathlib import Path

from graphql2python.template import TemplatesManager


def test_custom_template():
    custom_template_dir = Path(__file__).parent / Path("custom_templates/")

    manager = TemplatesManager(custom_template_dir=custom_template_dir)

    assert manager.render_comment(
        lines=["My long", "comment"],
        extra_template_data={"deprecation_reason": "Will be removed"}
    ) == """# comment line: My long
# comment line: comment
# @deprecation_reason: Will be removed"""
