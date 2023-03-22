from typing import List

import pytest

from graphql2python.model.render import DataModelRender

render = DataModelRender()


@pytest.mark.parametrize(
    "lines, result", [([], '"""\n...\n"""'), (['a', 'b'], '"""\na\nb\n"""'), (['a', 'b\nc'], '"""\na\nb\nc\n"""')]
)
def test_render_docstring_lines(lines: List[str], result: str):
    """Test for docstring render."""
    assert render.render_docstring(lines, 0, 120) == result


def test_render_docstring_lines_long_line():
    """Test for docstring render with long line."""

    lines = ['aaaaaaaa', 'aaa aaa aaa aaaaaaaa a aaa a aaaa a']

    result = '''"""
aaaaaaaa
aaa aaa
aaa
aaaaaaaa a
aaa a aaaa
a
"""'''

    assert render.render_docstring(lines, 0, 10) == result


def test_render_docstring_lines_long_line_ident():
    """Test for docstring render with long line and with non-zero indent"""

    lines = ['aaaaaaaa', 'aaa aaa aaa aaaaaaaa a aaa a aaaa a']

    result = '''    """
    aaaaaaaa
    aaa
    aaa
    aaa
    aaaaaaaa
    a aaa
    a aaaa
    a
    """'''

    assert render.render_docstring(lines, 4, 10) == result
