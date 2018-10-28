import os

import pytest
from dateutil import parser
from sutime import SUTime


@pytest.fixture(scope="module")
def sutime_with_mark_time_ranges():
    return SUTime(
        jars=os.path.join(
            *[os.path.dirname(__file__), os.pardir, os.pardir, "jars"]
        ),
        mark_time_ranges=True,
    )


def test_parse_duration_range_with_mark_time_ranges(
    sutime_with_mark_time_ranges,
    input_duration_range,
    tomorrow,
    two_pm,
    three_pm,
):
    result = sutime_with_mark_time_ranges.parse(input_duration_range)

    assert len(result) == 2

    assert result[0]["type"] == "DATE"
    assert parser.parse(result[0]["value"]).date() == tomorrow

    assert result[1]["type"] == "DURATION"

    begin = result[1]["value"]["begin"]
    assert parser.parse(begin).time() == two_pm

    end = result[1]["value"]["end"]
    assert parser.parse(end).time() == three_pm


def test_parse_christmas(sutime_with_mark_time_ranges, input_christmas_eve):
    result = sutime_with_mark_time_ranges.parse(input_christmas_eve)

    assert len(result) == 1

    assert result[0]["type"] == "SET"
    assert result[0]["value"] == "XXXX-12-24"


def test_sunday_night(sutime_with_mark_time_ranges, input_sunday_night):
    result = sutime_with_mark_time_ranges.parse(input_sunday_night)
    assert len(result) == 1
