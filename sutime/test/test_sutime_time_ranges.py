import os
from datetime import date

import pytest
from dateutil import parser
from sutime import SUTime


@pytest.fixture(scope='module')
def sutime_with_mark_time_ranges():
    return SUTime(
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

    assert result[0]['type'] == 'DATE'
    assert parser.parse(result[0]['value']).date() == tomorrow

    assert result[1]['type'] == 'DURATION'

    begin = result[1]['value']['begin']
    assert parser.parse(begin).time() == two_pm

    end = result[1]['value']['end']
    assert parser.parse(end).time() == three_pm


def test_parse_christmas(sutime_with_mark_time_ranges, input_christmas_eve):
    result = sutime_with_mark_time_ranges.parse(input_christmas_eve)

    assert len(result) == 1
    assert result[0]['type'] == 'DATE'

    # SUTime 4.x returns a date for `christmas eve`, which depends on today's
    # date. If we're in the first half after christmas last year, it defaults
    # to last year, otherwise this year.
    today = date.today()
    current_year = today.year if today >= date(
        today.year, 6, 25) else today.year - 1
    assert result[0]['value'] == '{0}-12-24'.format(current_year)


def test_sunday_night(sutime_with_mark_time_ranges, input_sunday_night):
    result = sutime_with_mark_time_ranges.parse(input_sunday_night)
    assert len(result) == 1
