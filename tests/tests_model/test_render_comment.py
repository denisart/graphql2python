from typing import List

import pytest

from graphql2python.model.render import DataModelRender

render = DataModelRender()


@pytest.mark.parametrize("lines, result", [([], "# ..."), (["a", "b"], "# a\n# b"), (["a", "b\nc"], "# a\n# b\n# c")])
def test_render_comment_lines(lines: List[str], result: str):
    assert render.render_comment(lines, 0, 120) == result


def test_render_comment_lines_long_line():
    """Test for comment render with long line."""

    lines = ["aaaaaaaa", "aaa aaa aaa aaaaaaaa a aaa a aaaa a"]

    result = """# aaaaaaaa
# aaa aaa
# aaa
# aaaaaaaa
# a aaa a
# aaaa a"""

    assert render.render_comment(lines, 0, 10) == result


def test_render_comment_lines_long_line_ident():
    """Test for comment render with long line and with non-zero indent."""

    lines = ["aaaaaaaa", "aaa aaa aaa aaaaaaaa a aaa a aaaa a"]

    result = """    # aaaaaaaa
    # aaa
    # aaa
    # aaa
    # aaaaaaaa
    # a
    # aaa
    # a
    # aaaa
    # a"""

    assert render.render_comment(lines, 4, 10) == result
