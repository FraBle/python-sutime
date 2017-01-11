import os
import pytest
import aniso8601
from datetime import date, time, timedelta
from dateutil import parser
from sutime import SUTime


@pytest.fixture(scope='module')
def sutime():
    return SUTime(jars=os.path.join(*[os.path.dirname(__file__), os.pardir, os.pardir, 'jars']))


@pytest.fixture(scope='module')
def sutime_with_mark_time_ranges():
    return SUTime(jars=os.path.join(*[os.path.dirname(__file__), os.pardir, os.pardir, 'jars']), mark_time_ranges=True)


@pytest.fixture
def input_duration():
    return 'I need a desk for tomorrow from 2pm for 2 hours'


@pytest.fixture
def input_duration_range():
    return 'I need a desk for tomorrow from 2pm to 3pm'


@pytest.fixture
def input_christmas_eve():
    return 'christmas eve'


@pytest.fixture
def input_sunday_night():
    return 'Mary had spent Sunday night with us.'


@pytest.fixture
def input_today():
    return 'I have written a test today.'


@pytest.fixture(scope='module')
def tomorrow():
    return date.today() + timedelta(days=1)


@pytest.fixture(scope='module')
def two_pm():
    return time(hour=14)


@pytest.fixture(scope='module')
def three_pm():
    return time(hour=15)


@pytest.fixture(scope='module')
def reference_date():
    return date(2017, 1, 9)


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


def test_parse_duration_range_with_mark_time_ranges(sutime_with_mark_time_ranges, input_duration_range, tomorrow, two_pm, three_pm):
    result = sutime_with_mark_time_ranges.parse(input_duration_range)

    assert len(result) == 2

    assert result[0][u'type'] == u'DATE'
    assert parser.parse(result[0][u'value']).date() == tomorrow

    assert result[1][u'type'] == u'DURATION'

    begin = result[1][u'value'][u'begin']
    assert parser.parse(begin).time() == two_pm

    end = result[1][u'value'][u'end']
    assert parser.parse(end).time() == three_pm


def test_parse_christmas(sutime_with_mark_time_ranges, input_christmas_eve):
    result = sutime_with_mark_time_ranges.parse(input_christmas_eve)

    assert len(result) == 1

    assert result[0][u'type'] == u'SET'
    assert result[0][u'value'] == u'XXXX-12-24'


def test_sunday_night(sutime_with_mark_time_ranges, input_sunday_night):
    result = sutime_with_mark_time_ranges.parse(input_sunday_night)
    assert len(result) == 1


def test_reference_date(sutime, input_today, reference_date):
    result = sutime.parse(input_today, reference_date.isoformat())

    assert len(result) == 1

    assert result[0][u'type'] == u'DATE'
    assert result[0][u'value'] == reference_date.isoformat()
