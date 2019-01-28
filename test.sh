#! /bin/bash -x

set -o pipefail

# We have to run tests separately as the JVM can only be started once per test
python3 setup.py test --addopts "--capture=no -vv --color=auto sutime/test/test_sutime.py" 2>&1 | tee ./test-reports/test_sutime.txt
python3 setup.py test --addopts "--capture=no -vv --color=auto sutime/test/test_sutime_time_ranges.py" 2>&1 | tee ./test-reports/test_sutime_time_ranges.txt || exit $?
python3 setup.py test --addopts "--capture=no -vv --color=auto sutime/test/test_sutime_spanish.py" 2>&1 | tee ./test-reports/test_sutime_spanish.txt || exit $?
python3 setup.py test --addopts "--capture=no -vv --color=auto sutime/test/test_sutime_jvm_flags.py" 2>&1 | tee ./test-reports/test_sutime_jvm_flags.txt || exit $?
