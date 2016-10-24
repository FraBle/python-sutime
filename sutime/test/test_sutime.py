import os
import pytest
import aniso8601
from datetime import datetime, timedelta
from dateutil import parser
from sutime import SUTime


@pytest.fixture(scope='module')
def sutime():
    return SUTime(jars=os.path.join(*[os.path.dirname(__file__), os.pardir, os.pardir, 'jars']))


@pytest.fixture(scope='module')
def sutime_with_mark_time_ranges():
    return SUTime(jars=os.path.join(*[os.path.dirname(__file__), os.pardir, os.pardir, 'jars']), mark_time_ranges=True)


@pytest.fixture
def test_input_duration():
    return 'I need a desk for tomorrow from 2pm for 2 hours'


@pytest.fixture
def test_input_duration_range():
    return 'I need a desk for tomorrow from 2pm to 3pm'


@pytest.fixture(scope='module')
def tomorrow():
    return datetime.now().date() + timedelta(days=1)


@pytest.fixture(scope='module')
def two_pm():
    return datetime.now().replace(
        hour=14, minute=0, second=0, microsecond=0).time()


@pytest.fixture(scope='module')
def three_pm():
    return datetime.now().replace(
        hour=15, minute=0, second=0, microsecond=0).time()


def test_parse_duration(sutime, test_input_duration, tomorrow, two_pm):
    result = sutime.parse(test_input_duration)

    assert len(result) == 3

    assert result[0][u'type'] == u'DATE'
    assert parser.parse(result[0][u'value']).date() == tomorrow

    assert result[1][u'type'] == u'TIME'
    assert parser.parse(result[1][u'value']).time() == two_pm

    assert result[2][u'type'] == u'DURATION'
    assert aniso8601.parse_duration(result[2][u'value']) == timedelta(hours=2)


def test_parse_duration_range(sutime, test_input_duration_range, tomorrow, two_pm, three_pm):
    result = sutime.parse(test_input_duration_range)

    assert len(result) == 3

    assert result[0][u'type'] == u'DATE'
    assert parser.parse(result[0][u'value']).date() == tomorrow

    assert result[1][u'type'] == u'TIME'
    assert parser.parse(result[1][u'value']).time() == two_pm

    assert result[2][u'type'] == u'TIME'
    assert parser.parse(result[2][u'value']).time() == three_pm


def test_parse_duration_range_with_mark_time_ranges(sutime_with_mark_time_ranges, test_input_duration_range, tomorrow, two_pm, three_pm):
    result = sutime_with_mark_time_ranges.parse(test_input_duration_range)

    assert len(result) == 2

    assert result[0][u'type'] == u'DATE'
    assert parser.parse(result[0][u'value']).date() == tomorrow

    assert result[1][u'type'] == u'DURATION'

    begin = result[1][u'value'][u'begin']
    assert parser.parse(begin).time() == two_pm

    end = result[1][u'value'][u'end']
    assert parser.parse(end).time() == three_pm


def test_parse_christmas(sutime_with_mark_time_ranges):
    result = sutime_with_mark_time_ranges.parse('christmas eve')

    assert len(result) == 1

    assert result[0][u'type'] == u'SET'
    assert result[0][u'value'] == u'XXXX-12-24'


def test_sunday_night(sutime_with_mark_time_ranges):
    result = sutime_with_mark_time_ranges.parse(
        'Mary had spent Sunday night with us.')
    assert len(result) == 1
