import pytest

from graphql2python.template import TemplatesManager


def test_empty_lines():
    manager = TemplatesManager()
    assert manager.render_comment(lines=[]) == "# ..."


def test_simple_comment():
    manager = TemplatesManager()
    assert manager.render_comment(lines=["my comment"]) == "# my comment"


def test_simple_comment_with_indent():
    manager = TemplatesManager()
    assert manager.render_comment(lines=["my comment"], indent=4) == "    # my comment"


@pytest.mark.parametrize(
    "indent, result",
    [
        (0, "# my comment"),
        (1, " # my comment"),
        (2, "  # my comment"),
        (3, "   # my comment"),
        (4, "    # my comment"),
        (5, "     # my comment"),
    ]
)
def test_indent(indent: int, result: str):
    manager = TemplatesManager()
    assert manager.render_comment(lines=["my comment"], indent=indent) == result


def test_multi_line_comment():
    manager = TemplatesManager()
    assert manager.render_comment(
        lines=["my long", "comment", "long long", "comment"]
    ) == """# my long
# comment
# long long
# comment"""


def test_multi_line_comment_with_indent():
    manager = TemplatesManager()
    assert manager.render_comment(lines=["my long", "comment"], indent=4) == "    # my long\n    # comment"
