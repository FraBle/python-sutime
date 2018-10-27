#! /bin/bash -x

# We have to run tests separately as the JVM can only be started once per test
python setup.py test --addopts sutime/test/test_sutime.py
python setup.py test --addopts sutime/test/test_sutime_time_ranges.py
python setup.py test --addopts sutime/test/test_sutime_jvm_flags.py
