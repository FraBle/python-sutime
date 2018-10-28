import os

import pytest
from sutime import SUTime


@pytest.fixture(scope="module")
def sutime_with_jvm_flags():
    return SUTime(
        jars=os.path.join(
            *[os.path.dirname(__file__), os.pardir, os.pardir, "jars"]
        ),
        jvm_flags=("-Xms256m",),
    )


def test_jvm_flags(sutime_with_jvm_flags, input_today, reference_date):
    # We can't test the effect of the JVM flags, all we can do is test
    # that basic functionality is ok
    result = sutime_with_jvm_flags.parse(
        input_today, reference_date.isoformat()
    )
    assert len(result) == 1
