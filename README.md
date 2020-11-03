# sutime
*Python wrapper for Stanford CoreNLP's [SUTime](http://nlp.stanford.edu/software/sutime.shtml) Java library.*

## Build Status

#### Travis CI Builds
[![Travis CI](https://travis-ci.com/FraBle/python-sutime.svg?branch=master)](https://travis-ci.com/FraBle/python-sutime)
>>>>>>> c66aec1... Switch to Poetry and wemake-python-styleguide

#### PyPI
[![PyPI Version](https://img.shields.io/pypi/v/sutime.svg)](https://pypi.org/project/sutime/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/sutime.svg)](https://pypi.org/project/sutime/)

#### Code Quality
[![Codacy Grade](https://img.shields.io/codacy/grade/05d69a800b2c4854bc1f98d9281b35a8.svg)](https://app.codacy.com/project/FraBle/python-sutime/dashboard)
[![Scrutinizer](https://img.shields.io/scrutinizer/g/FraBle/python-sutime.svg)](https://scrutinizer-ci.com/g/FraBle/python-sutime/)
[![Coverity Scan](https://img.shields.io/coverity/scan/22017.svg)](https://scan.coverity.com/projects/python-sutime)
[![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability/FraBle/python-sutime.svg)](https://codeclimate.com/github/FraBle/python-sutime/maintainability)

## Installation

```bash
>> # Ideally, create a virtual environment before installing any dependencies
>> pip install sutime
>> # Install Java dependencies
>> mvn dependency:copy-dependencies -DoutputDirectory=./jars -f $(python3 -c 'import importlib; import pathlib; print(pathlib.Path(importlib.util.find_spec("sutime").origin).parent / "pom.xml")')
```

Append `-P spanish` to the `mvn` command to include the Spanish language model.

## Supported Languages

SUTime currently supports only English, British and Spanish ([Source](https://github.com/stanfordnlp/CoreNLP/tree/master/src/edu/stanford/nlp/time/rules)).
This Python wrapper is prepared to support the other CoreNLP languages (e.g. German) as well as soon as they get added to SUTime.
The following command can be used to download the language models for `arabic`, `chinese`, `english`, `french`, `german`, and `spanish`:

```bash
>> mvn dependency:copy-dependencies -DoutputDirectory=./jars -f $(python -c 'import importlib; import pathlib; print(pathlib.Path(importlib.util.find_spec("sutime").origin).parent / "pom.xml")') -P <language>
```

*However, SUTime only supports a subset (default model and `spanish`) of CoreNLP's languages and the other language models will get ignored.*

## Example

```python
import json
from sutime import SUTime

if __name__ == '__main__':
    test_case = 'I need a desk for tomorrow from 2pm to 3pm'
    sutime = SUTime(mark_time_ranges=True, include_range=True)
    print(json.dumps(sutime.parse(test_case), sort_keys=True, indent=4))
```

Result:

```json
[
    {
        "end": 26,
        "start": 18,
        "text": "tomorrow",
        "timex-value": "2020-11-03",
        "type": "DATE",
        "value": "2020-11-03"
    },
    {
        "end": 42,
        "start": 27,
        "text": "from 2pm to 3pm",
        "type": "DURATION",
        "value": {
            "begin": "T14:00",
            "end": "T15:00"
        }
    }
]
```

Other examples can be found in the [test](https://github.com/FraBle/python-sutime/blob/master/sutime/test) directory.

## Functions

```python
SUTime(
    jars: Optional[str] = None,
    jvm_started: Optional[bool] = False,
    mark_time_ranges: Optional[bool] = False,
    include_range: Optional[bool] = False,
    jvm_flags: Optional[List[str]] = None,
    language: Optional[str] = 'english',
):
    """
    Args:
        jars (Optional[str]): Path to previously downloaded SUTime Java
            dependencies. Defaults to False.
        jvm_started (Optional[bool]): Flag to indicate that JVM has been
            already started (with all Java dependencies loaded). Defaults
            to False.
        mark_time_ranges (Optional[bool]): SUTime flag for
            sutime.markTimeRanges. Defaults to False.
            "Whether or not to recognize time ranges such as 'July to
            August'"
        include_range (Optional[bool]): SUTime flag for
            sutime.includeRange. Defaults to False.
            "Whether or not to add range info to the TIMEX3 object"
        jvm_flags (Optional[List[str]]): List of flags passed to JVM. For
            example, this may be used to specify the maximum heap size
            using '-Xmx'. Has no effect if `jvm_started` is set to True.
            Defaults to None.
        language (Optional[str]): Selected language. Currently supported
            are: english (/en), british, spanish (/es). Defaults to
            `english`.
    """

sutime.parse(input_str: str, reference_date: Optional[str] = '') -> List[Dict]:
    """Parse datetime information out of string input.

    It invokes the SUTimeWrapper.annotate() function in Java.

    Args:
        input_str (str): The input as string that has to be parsed.
        reference_date (Optional[str]): Optional reference data for SUTime.
            Defaults to `''`.

    Returns:
        A list of dicts with the result from the `SUTimeWrapper.annotate()`
        call.

    Raises:
        RuntimeError: An error occurs when CoreNLP is not loaded.
    """
```

## Credit

-   [The team behind Stanford CoreNLP](http://stanfordnlp.github.io/CoreNLP/) for their awesome work and tools for the NLP community
-   [Luis Nell (Github: originell) and team](https://github.com/originell/jpype/) for maintaining JPype as interface between Python and Java

## Contributions

-   [René Springer](https://github.com/r-springer): Support for reference date
-   [Constantine Lignos](https://github.com/ConstantineLignos): Support for JVM flags, adoption of CircleCI 2.0, fix for mutable default argument, fix for test execution
-   [Cole Robertson](https://github.com/cbjrobertson): Updated instructions, JAR requirements, and SUTime JAR imports
-   [Ludovico Pestarino](https://github.com/arkeane): Modified json.loads for compatibility with json data (string handling)

## License

-   GPLv3+ (check the LICENSE file)
