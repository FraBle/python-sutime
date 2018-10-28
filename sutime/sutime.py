import imp
import json
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

    _sutime_python_jar = "stanford-corenlp-sutime-python-1.3.0.jar"

    _supported_languages = {"english", "en", "british", "spanish", "es"}

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
        if language not in SUTime._supported_languages:
            raise RuntimeError("Unsupported language: {}".format(language))

        self.jars = jars if jars is not None else []

        if not jvm_started and not jpype.isJVMStarted():
            self._start_jvm(jvm_flags)

        if not jpype.isThreadAttachedToJVM():
            jpype.attachThreadToJVM()
        SUTimeWrapper = jpype.JClass("edu.stanford.nlp.python.SUTimeWrapper")
        self._sutime = SUTimeWrapper(mark_time_ranges, include_range, language)

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
