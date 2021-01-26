# -*- coding: utf-8 -*-
"""A Python wrapper for Stanford CoreNLP's SUTime."""

import glob
import importlib
import json
import logging
import os
import socket
import sys
import threading
from pathlib import Path
from typing import Dict, List, Optional

import jpype  # pyre-ignore[21]

SOCKED_DEFAULT_TIMEOUT = 15
socket.setdefaulttimeout(SOCKED_DEFAULT_TIMEOUT)


class SUTime(object):
    """Python wrapper for SUTime (CoreNLP) by Stanford."""

    _sutime_python_jar = 'stanford-corenlp-sutime-python-1.4.0.jar'
    _sutime_java_class = 'edu.stanford.nlp.python.SUTimeWrapper'
    _corenlp_version = '4.0.0'

    # full name or ISO 639-1 code
    _languages = {
        'arabic': 'arabic',
        'ar': 'arabic',
        'chinese': 'chinese',
        'zh': 'chinese',
        'english': 'english',
        'british': 'british',
        'en': 'english',
        'french': 'french',
        'fr': 'french',
        'german': 'german',
        'de': 'german',
        'spanish': 'spanish',
        'es': 'spanish',
    }

    # https://github.com/stanfordnlp/CoreNLP/tree/master/src/edu/stanford/nlp/time/rules
    _supported_languages = {'british', 'english', 'spanish'}

    _required_jars = {
        'stanford-corenlp-{0}-models.jar'.format('4.0.0'),
        'stanford-corenlp-{0}.jar'.format('4.0.0'),
        'gson-2.8.6.jar',
        'slf4j-simple-1.7.30.jar',
    }

    def __init__(
        self,
        jars: Optional[str] = None,
        jvm_started: Optional[bool] = False,
        mark_time_ranges: Optional[bool] = False,
        include_range: Optional[bool] = False,
        jvm_flags: Optional[List[str]] = None,
        language: Optional[str] = 'english',
    ):
        """Initialize `SUTime` wrapper.

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
        self.mark_time_ranges = mark_time_ranges
        self.include_range = include_range
        self._is_loaded = False
        self._sutime = None
        self._lock = threading.Lock()
        module_root = Path(__file__).resolve().parent
        self.jars = Path(jars) if jars else os.path.join(
                Path(importlib.util.find_spec('sutime').origin).parent, 'jars')

        self._check_language_model_dependency(
            language.lower() if language else '',
        )

        if not jvm_started:
            self._classpath = self._create_classpath()
            self._start_jvm(jvm_flags)

        self._load_java_wrapper_class(language)

    def parse(
        self, input_str: str, reference_date: Optional[str] = '',
    ) -> List[Dict]:
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
        if self._is_loaded is False:
            raise RuntimeError('Please load SUTime first!')

        if reference_date:
            return json.loads(str(self._sutime.annotate(
                input_str, reference_date,
            )))
        return json.loads(str(self._sutime.annotate(input_str)))

    def _load_java_wrapper_class(self, language: Optional[str]):
        try:
            # make it thread-safe
            if threading.active_count() > 1:
                if not jpype.isThreadAttachedToJVM():
                    jpype.attachThreadToJVM()
            self._lock.acquire()
            wrapper = jpype.JClass(self._sutime_java_class)
            self._sutime = wrapper(
                self.mark_time_ranges, self.include_range, language,
            )
            self._is_loaded = True
        except Exception as exc:
            sys.exit('Could not load JVM: {0}'.format(exc))
        finally:
            self._lock.release()

    def _check_language_model_dependency(self, language: str):
        if language not in self._languages:
            raise RuntimeError('Unsupported language: {0}'.format(language))
        normalized_language = self._languages[language]

        if normalized_language not in self._supported_languages:
            logging.warning('{0}: {1}. {2}.'.format(
                normalized_language.capitalize(),
                'is not (yet) supported by SUTime',
                'Falling back to default model',
            ))
            return

        language_model_file = (
            self.jars / 'stanford-corenlp-{0}-models-{1}.jar'.format(
                self._corenlp_version,
                normalized_language,
            ))

        language_model_file_exists = glob.glob(str(language_model_file))
        is_english_language = normalized_language in {'english', 'british'}

        if not (language_model_file_exists or is_english_language):
            raise RuntimeError(
                'Missing language model for {0}! Run {1} {2} {3}'.format(
                    self._languages[language].capitalize(),
                    'mvn dependency:copy-dependencies',
                    '-DoutputDirectory=./sutime/jars -P',
                    self._languages[language],
                ),
            )

    def _start_jvm(self, additional_flags: Optional[List[str]]):
        flags = ['-Djava.class.path={0}'.format(self._classpath)]
        if additional_flags:
            flags.extend(additional_flags)
        logging.info('jpype.isJVMStarted(): {0}'.format(jpype.isJVMStarted()))
        if not jpype.isJVMStarted():
            jpype.startJVM(jpype.getDefaultJVMPath(), *flags)

    def _create_classpath(self):
        sutime_jar = (
            Path(importlib.util.find_spec('sutime').origin).parent /
            'jars' / self._sutime_python_jar
        )
        jars = [sutime_jar]
        jar_file_names = []
        for top, _, files in os.walk(self.jars):
            for file_name in files:
                if file_name.endswith('.jar'):
                    jars.append(Path(top, file_name))
                    jar_file_names.append(file_name)
        if not self._required_jars.issubset(jar_file_names):
            logging.warning([
                jar for jar in self._required_jars if jar not in jar_file_names
            ])
            raise RuntimeError(
                'Not all necessary Java dependencies have been downloaded!',
            )
        return os.pathsep.join(str(jar) for jar in jars)
