# sutime
*Python wrapper for Stanford CoreNLP's [SUTime](http://nlp.stanford.edu/software/sutime.shtml) Java library.*

## Build Status

#### CircleCI Builds
[![CircleCI](https://img.shields.io/circleci/project/github/FraBle/python-sutime.svg)](https://circleci.com/gh/FraBle/python-sutime)

#### PyPI
[![PyPI Version](https://img.shields.io/pypi/v/sutime.svg)](https://pypi.org/project/sutime/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/sutime.svg)](https://pypi.org/project/sutime/)

#### Code Quality
[![Codacy Grade](https://img.shields.io/codacy/grade/05d69a800b2c4854bc1f98d9281b35a8.svg)](https://app.codacy.com/project/FraBle/python-sutime/dashboard)
[![Scrutinizer](https://img.shields.io/scrutinizer/g/FraBle/python-sutime.svg)](https://scrutinizer-ci.com/g/FraBle/python-sutime/)
[![Coverity Scan](https://img.shields.io/coverity/scan/17101.svg)](https://scan.coverity.com/projects/frable-python-sutime)
[![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability/FraBle/python-sutime.svg)](https://codeclimate.com/github/FraBle/python-sutime/maintainability)

## Installation

```bash
>> pip install sutime
>> # use package pom.xml to install all Java dependencies via Maven into ./jars
>> mvn dependency:copy-dependencies -DoutputDirectory=./jars
```

Run the following command to add the Spanish language model:
```bash
>> mvn dependency:copy-dependencies -DoutputDirectory=./jars -P spanish
```

## Supported Languages
SUTime currently supports only English, British and Spanish ([Source](https://github.com/stanfordnlp/CoreNLP/tree/master/src/edu/stanford/nlp/time/rules)).
This Python wrapper is prepared to support the other CoreNLP languages (e.g. German) as well as soon as they get added to SUTime.
The following command can be used to download the language models for `arabic`, `chinese`, `english`, `french`, `german`, and `spanish`:
```bash
>> mvn dependency:copy-dependencies -DoutputDirectory=./jars -P <language>
```
_However, SUTime only supports a subset (default model and `spanish`) of CoreNLP's languages and the other language models will get ignored._

## Example

```python
import json
import os
from sutime import SUTime

if __name__ == '__main__':
    test_case = u'I need a desk for tomorrow from 2pm to 3pm'

    jar_files = os.path.join(os.path.dirname(__file__), 'jars')
    sutime = SUTime(jars=jar_files, mark_time_ranges=True)

    print(json.dumps(sutime.parse(test_case), sort_keys=True, indent=4))
```

Result:

```json
[
    {
        "end": 26,
        "start": 18,
        "text": "tomorrow",
        "type": "DATE",
        "value": "2016-10-14"
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
SUTime(jars=None, jvm_started=False, mark_time_ranges=False, include_range=False,
       jvm_flags=None, language='english')
    """
    jars: List of paths to the SUTime Java dependencies.
    jvm_started: Optional attribute to specify if the JVM has already been
        started (with all Java dependencies loaded).
    mark_time_ranges: Optional attribute to specify CoreNLP property
        sutime.markTimeRanges. Default is False.
        "Tells sutime to mark phrases such as 'From January to March'
        instead of marking 'January' and 'March' separately"
    include_range: Optional attribute to specify CoreNLP property
        sutime.includeRange. Default is False.
        "Tells sutime to mark phrases such as 'From January to March'
        instead of marking 'January' and 'March' separately"
    jvm_flags: Optional attribute to specify an iterable of string flags
        to be provided to the JVM at startup. For example, this may be
        used to specify the maximum heap size using '-Xmx'. Has no effect
        if jvm_started is set to True. Default is None.
    language: Optional attribute to select language. The following options
        are supported: english (/en), british, spanish (/es). Default is
        english.
    """

sutime.parse(input_str, reference_date=''):
    """Parses datetime information out of string input.

    It invokes the SUTimeWrapper.annotate() function in Java.

    Args:
        input_str: The input as string that has to be parsed.
        reference_date: Optional reference data for SUTime.

    Returns:
        A list of dicts with the result from the SUTimeWrapper.annotate()
            call.
    """
```

## Credit

-   [The team behind Stanford CoreNLP](http://stanfordnlp.github.io/CoreNLP/) for their awesome work and tools for the NLP community
-   [Luis Nell (Github: originell) and team](https://github.com/originell/jpype/) for maintaining JPype as interface between Python and Java

## Contributions

-   [René Springer](https://github.com/r-springer): Support for reference date
-   [Constantine Lignos](https://github.com/ConstantineLignos): Support for JVM flags, adoption of CircleCI 2.0, fix for mutable default argument, fix for test execution

## License

-   GPLv3+ (check the LICENSE file)
