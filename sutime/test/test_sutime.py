import os
from datetime import timedelta

import aniso8601
import pytest
from dateutil import parser

from sutime import SUTime


@pytest.fixture(scope="module")
def sutime():
    return SUTime(
        jars=os.path.join(
            *[os.path.dirname(__file__), os.pardir, os.pardir, "jars"]
        )
    )


def test_parse_duration(sutime, input_duration, tomorrow, two_pm):
    result = sutime.parse(input_duration)

    assert len(result) == 3

    assert result[0]["type"] == "DATE"
    assert parser.parse(result[0]["value"]).date() == tomorrow

    assert result[1]["type"] == "TIME"
    assert parser.parse(result[1]["value"]).time() == two_pm

    assert result[2]["type"] == "DURATION"
    assert aniso8601.parse_duration(result[2]["value"]) == timedelta(hours=2)


def test_parse_duration_range(
    sutime, input_duration_range, tomorrow, two_pm, three_pm
):
    result = sutime.parse(input_duration_range)

    assert len(result) == 3

    assert result[0]["type"] == "DATE"
    assert parser.parse(result[0]["value"]).date() == tomorrow

    assert result[1]["type"] == "TIME"
    assert parser.parse(result[1]["value"]).time() == two_pm

    assert result[2]["type"] == "TIME"
    assert parser.parse(result[2]["value"]).time() == three_pm


def test_reference_date(sutime, input_today, reference_date):
    result = sutime.parse(input_today, reference_date.isoformat())

    assert len(result) == 1

    assert result[0]["type"] == "DATE"
    assert result[0]["value"] == reference_date.isoformat()


def test_last_quarter(
    sutime, input_last_quarter, last_quarter, reference_date
):
    result = sutime.parse(input_last_quarter, reference_date.isoformat())

    assert len(result) == 1

    assert result[0]["type"] == "DATE"
    assert result[0]["value"] == str(
        (reference_date - timedelta(weeks=2)).year)
    assert result[0]["timex-value"] == last_quarter
