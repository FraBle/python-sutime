import os
from datetime import timedelta

import aniso8601
import pytest
from dateutil import parser

from sutime import SUTime


@pytest.fixture(scope='module')
def sutime():
    return SUTime(jars=os.path.join(*[os.path.dirname(__file__), os.pardir, os.pardir, 'jars']))


def test_parse_duration(sutime, input_duration, tomorrow, two_pm):
    result = sutime.parse(input_duration)

    assert len(result) == 3

    assert result[0][u'type'] == u'DATE'
    assert parser.parse(result[0][u'value']).date() == tomorrow

    assert result[1][u'type'] == u'TIME'
    assert parser.parse(result[1][u'value']).time() == two_pm

    assert result[2][u'type'] == u'DURATION'
    assert aniso8601.parse_duration(result[2][u'value']) == timedelta(hours=2)


def test_parse_duration_range(sutime, input_duration_range, tomorrow, two_pm, three_pm):
    result = sutime.parse(input_duration_range)

    assert len(result) == 3

    assert result[0][u'type'] == u'DATE'
    assert parser.parse(result[0][u'value']).date() == tomorrow

    assert result[1][u'type'] == u'TIME'
    assert parser.parse(result[1][u'value']).time() == two_pm

    assert result[2][u'type'] == u'TIME'
    assert parser.parse(result[2][u'value']).time() == three_pm


def test_reference_date(sutime, input_today, reference_date):
    result = sutime.parse(input_today, reference_date.isoformat())

    assert len(result) == 1

    assert result[0][u'type'] == u'DATE'
    assert result[0][u'value'] == reference_date.isoformat()
