import os

import pytest
from sutime import SUTime


@pytest.fixture(scope="module")
def sutime_spanish():
    return SUTime(
        jars=os.path.join(
            *[os.path.dirname(__file__), os.pardir, os.pardir, "jars"]
        ),
        language="spanish",
    )


def test_spanish(sutime_spanish, input_spanish, reference_date):
    result = sutime_spanish.parse(input_spanish, reference_date.isoformat())

    assert len(result) == 1

    assert result[0]["type"] == "DATE"
    assert result[0]["value"] == reference_date.isoformat()
