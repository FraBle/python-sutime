import glob
import imp
import json
import logging
import os
import socket

import jpype

socket.setdefaulttimeout(15)


class SUTime(object):
    """Python wrapper for SUTime (CoreNLP) by Stanford.

    Attributes:
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

    _required_jars = {
        "stanford-corenlp-3.9.2-models.jar",
        "stanford-corenlp-3.9.2.jar",
        "gson-2.8.5.jar",
        "slf4j-simple-1.7.25.jar",
    }

    _sutime_python_jar = "stanford-corenlp-sutime-python-1.4.0.jar"

    # full name or ISO 639-1 code
    _languages = {
        "arabic": "arabic",
        "ar": "arabic",
        "chinese": "chinese",
        "zh": "chinese",
        "english": "english",
        "british": "british",
        "en": "english",
        "french": "french",
        "fr": "french",
        "german": "german",
        "de": "german",
        "spanish": "spanish",
        "es": "spanish",
    }

    # https://github.com/stanfordnlp/CoreNLP/tree/master/src/edu/stanford/nlp/time/rules
    _supported_languages = {"british", "english", "spanish"}

    def __init__(
        self,
        jars=None,
        jvm_started=False,
        mark_time_ranges=False,
        include_range=False,
        jvm_flags=None,
        language="english",
    ):
        """Initializes SUTime.
        """
        self.jars = jars if jars is not None else []
        self._check_language_model_dependency(language.lower())

        if not jvm_started and not jpype.isJVMStarted():
            self._start_jvm(jvm_flags)

        if not jpype.isThreadAttachedToJVM():
            jpype.attachThreadToJVM()
        wrapper = jpype.JClass("edu.stanford.nlp.python.SUTimeWrapper")
        self._sutime = wrapper(mark_time_ranges, include_range, language)

    def _check_language_model_dependency(self, language):
        if language not in SUTime._languages:
            raise RuntimeError("Unsupported language: {}".format(language))
        normalized_language = SUTime._languages[language]

        if normalized_language not in SUTime._supported_languages:
            logging.warning(
                "%s is not (yet) supported by SUTime. "
                "Falling back to default model.",
                normalized_language.capitalize(),
            )
            return

        language_model_file = os.path.join(
            self.jars,
            "stanford-corenlp-3.9.2-models-{}.jar".format(normalized_language),
        )

        if not (
            glob.glob(language_model_file)
            or normalized_language in {"english", "british"}
        ):
            raise RuntimeError(
                "Missing language model for {}! ".format(
                    SUTime._languages[language].capitalize()
                )
                + "Please run: mvn dependency:copy-dependencies "
                + "-DoutputDirectory=./jars -P {}".format(
                    SUTime._languages[language]
                )
            )

    def _start_jvm(self, additional_flags):
        flags = ["-Djava.class.path=" + self._create_classpath()]
        if additional_flags:
            flags.extend(additional_flags)
        jpype.startJVM(jpype.getDefaultJVMPath(), *flags)

    def _create_classpath(self):
        sutime_jar = os.path.join(
            *[imp.find_module("sutime")[1], "jars", SUTime._sutime_python_jar]
        )
        jars = [sutime_jar]
        jar_file_names = []
        for top, _, files in os.walk(self.jars):
            for file_name in files:
                if file_name.endswith(".jar"):
                    jars.append(os.path.join(top, file_name))
                    jar_file_names.append(file_name)
        if not SUTime._required_jars.issubset(jar_file_names):
            raise RuntimeError(
                "Not all necessary Java dependencies have been downloaded!"
            )
        return os.pathsep.join(jars)

    def parse(self, input_str, reference_date=""):
        """Parses datetime information out of string input.

        It invokes the SUTimeWrapper.annotate() function in Java.

        Args:
            input_str: The input as string that has to be parsed.
            reference_date: Optional reference data for SUTime.

        Returns:
            A list of dicts with the result from the SUTimeWrapper.annotate()
                call.
        """
        if not jpype.isThreadAttachedToJVM():
            jpype.attachThreadToJVM()
        if reference_date:
            return json.loads(self._sutime.annotate(input_str, reference_date))
        return json.loads(self._sutime.annotate(input_str))
