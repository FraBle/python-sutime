#! /bin/bash -x

# We have to run tests separately as the JVM can only be started once per test
python setup.py test --addopts "--capture=no -vv --color=auto sutime/test/test_sutime.py" 2>&1 | tee ./test-reports/test_sutime.txt
python setup.py test --addopts "--capture=no -vv --color=auto sutime/test/test_sutime_time_ranges.py" 2>&1 | tee ./test-reports/test_sutime_time_ranges.txt
python setup.py test --addopts "--capture=no -vv --color=auto sutime/test/test_sutime_spanish.py" 2>&1 | tee ./test-reports/test_sutime_spanish.txt
python setup.py test --addopts "--capture=no -vv --color=auto sutime/test/test_sutime_jvm_flags.py" 2>&1 | tee ./test-reports/test_sutime_jvm_flags.txt
