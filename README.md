# sutimewfwfewfef
*Python wrapper for Stanford CoreNLP's [SUTime](http://nlp.stanford.edu/software/sutime.shtml) Java library*
dc
#### Build Status

![CircleCi Build Status](https://circleci.com/gh/FraBle/python-sutime.svg?style=shield&circle-token=ce50d3fb4d377c59a8eb1a25f3467dd0ebe9457a)

#### Introduction

This library provides a simple access to SUTime functions in Python.


#### Installation

```bash
>> pip install sutime
>> # install all Java dependencies via Maven in ./jars
>> mvn -f java/pom.xml dependency:copy-dependencies -DoutputDirectory=./jars
```

#### Example
```python
import os
from sutime import SUTime

if __name__ == '__main__':
    test_input = u'I need a desk for tomorrow from 2pm to 3pm'

    # tell SUTime where to find the Java dependencies
    jars = os.path.join(os.path.dirname(__file__), 'jars')

    # initialize SUTime 
    sutime = SUTime(jars, mark_time_ranges=True)

    print(sutime.parse(test_input))
```
Other examples can be found in the test directory.

#### Future Work
- fixing all upcoming bug reports and issues.

#### Credit
- [The team behind Stanford CoreNLP](http://stanfordnlp.github.io/CoreNLP/) for their awesome work and tools for the NLP community
- [Luis Nell (Github: originell) and team](https://github.com/originell/jpype/) for maintaining JPype as interface between Python and Java

#### License
- GPLv3+ (check the LICENSE file)
