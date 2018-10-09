#! /bin/bash -x

# We have to run tests separately as the JVM can only be started once per test
pytest sutime/test/test_sutime.py
pytest sutime/test/test_sutime_time_ranges.py
