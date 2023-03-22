from typing import List

import pytest

from graphql2python.model.render import DataModelRender

render = DataModelRender()


@pytest.mark.parametrize(
    "line, result",
    [
        ("aa", ["aa"]),
        ("aaaaaaaaaaa", ["aaaaaaaaaaa"]),
        ("aaaaa aaaaa", ["aaaaa", "aaaaa"]),
        ("aaaaa aaaaaa", ["aaaaa", "aaaaaa"]),
        ("aaa aaa aaaaa", ["aaa aaa", "aaaaa"]),
    ],
)
def test_processing_of_line(line: str, result: List[str]):
    assert render.processing_of_line(line, 0, 10) == result


@pytest.mark.parametrize(
    "line, result",
    [
        ("aa", ["aa"]),
        ("aaaaaaaaaaa", ["aaaaaaaaaaa"]),
        ("aaaaa aaaaa", ["aaaaa", "aaaaa"]),
        ("aaaaa aaaaaa", ["aaaaa", "aaaaaa"]),
        ("aaa aaa aaaaa", ["aaa", "aaa", "aaaaa"]),
    ],
)
def test_processing_of_line_indent(line: str, result: List[str]):
    assert render.processing_of_line(line, 4, 10) == result
