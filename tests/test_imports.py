import pytest

from graphql2python.imports import (
    Import,
    Imports,
    IMPORT_ANNOTATED,
    IMPORT_ANY,
    IMPORT_LIST,
    IMPORT_UNION,
    IMPORT_OPTIONAL,
    IMPORT_LITERAL,
    IMPORT_ENUM,
    IMPORT_DICT,
    IMPORT_DECIMAL,
    IMPORT_DATE,
    IMPORT_DATETIME,
    IMPORT_TIME,
    IMPORT_UUID,
)


@pytest.mark.parametrize(
    "import_, result",
    [
        (IMPORT_ANNOTATED, "from typing import Annotated"),
        (IMPORT_ANY, "from typing import Any"),
        (IMPORT_LIST, "from typing import List"),
        (IMPORT_UNION, "from typing import Union"),
        (IMPORT_OPTIONAL, "from typing import Optional"),
        (IMPORT_LITERAL, "from typing import Literal"),
        (IMPORT_DICT, "from typing import Dict"),
        (IMPORT_ENUM, "from enum import Enum"),
        (IMPORT_DECIMAL, "from decimal import Decimal"),
        (IMPORT_DATE, "from datetime import date"),
        (IMPORT_DATETIME, "from datetime import datetime"),
        (IMPORT_TIME, "from datetime import time"),
        (IMPORT_UUID, "from uuid import UUID"),
    ]
)
def test_default_import(import_: Import, result: str):
    imports_ = Imports()
    imports_.append(import_)
    assert str(imports_) == result


def test_full():
    imports_ = Imports()

    imports_.append(IMPORT_ANY)
    imports_.append(IMPORT_UNION)
    imports_.append(IMPORT_OPTIONAL)
    imports_.append(IMPORT_DATE)
    imports_.append(IMPORT_DATETIME)
    imports_.append(IMPORT_UUID)

    result = """from typing import Any, Optional, Union
from datetime import date, datetime
from uuid import UUID"""

    assert str(imports_) == result


def test_alias():
    imports_ = Imports()

    imports_.append(Import(from_="typing", import_="Any", alias="MyAny"))
    imports_.append(Import(from_="typing", import_="Optional", alias="MyOptional"))
    imports_.append(Import(from_="datetime", import_="datetime", alias="default_datetime"))

    result = """from typing import Any as MyAny, Optional as MyOptional
from datetime import datetime as default_datetime"""

    assert str(imports_) == result
