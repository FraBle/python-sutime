# sutime
*Python wrapper for Stanford CoreNLP's [SUTime](http://nlp.stanford.edu/software/sutime.shtml) Java library*
dc
#### Build Status

![CircleCi Build Status](https://circleci.com/gh/FraBle/python-sutime.svg?style=shield&circle-token=c5b5f420bcb888abc19312d711493cb9d1641503)

#### Introduction

This library provides a simple access to SUTime functions in Python.


#### Installation

```bash
>> pip install sutime
>> # use package pom.xml to install all Java dependencies via Maven into ./jars
>> mvn dependency:copy-dependencies -DoutputDirectory=./jars
```

#### Example
```python
import os
import json
from sutime import SUTime

if __name__ == '__main__':
    test_case = u'I need a desk for tomorrow from 2pm to 3pm'
    jars = os.path.join(os.path.dirname(__file__), 'jars')
    sutime = SUTime(jars, mark_time_ranges=True)

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

Other examples can be found in the test directory.

#### Functions
```python
SUTime(jars, mark_time_ranges=False, include_range=False)
    """
    jars: Paths to the SUTime Java dependencies.
    mark_time_ranges: Optional attribute to specify CoreNLP property
        sutime.markTimeRanges. Default is False.
        "Tells sutime to mark phrases such as 'From January to March'
        instead of marking 'January' and 'March' separately"
    include_range: Optional attribute to specify CoreNLP property
        sutime.includeRange. Default is False.
        "Tells sutime to mark phrases such as 'From January to March'
        instead of marking 'January' and 'March' separately"
    """

sutime.parse(input_str):
    """Parses datetime information out of string input.

    It invokes the SUTimeWrapper.annotate() function in Java.

    Args:
        input_str: The input as string that has to be parsed.

    Returns:
        A list of dicts with the result from the SUTimeWrapper.annotate()
            call.

    Raises:
        RuntimeError: An error occurres when CoreNLP is not loaded.
    """
```

#### Future Work
- fixing all upcoming bug reports and issues.

#### Credit
- [The team behind Stanford CoreNLP](http://stanfordnlp.github.io/CoreNLP/) for their awesome work and tools for the NLP community
- [Luis Nell (Github: originell) and team](https://github.com/originell/jpype/) for maintaining JPype as interface between Python and Java

#### License
- GPLv3+ (check the LICENSE file)
