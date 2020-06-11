import os
import imp
import jpype
import socket
import threading
import json

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
    """

    _required_jars = {
        'stanford-corenlp-3.9.2-models.jar',
        'stanford-corenlp-3.9.2.jar',
        'gson-2.8.5.jar',
        'slf4j-simple-1.7.25.jar'
    }

    def __init__(self, jvm_started=False, mark_time_ranges=False, include_range=False,jars=None):
        """Initializes SUTime.
        """
        self.mark_time_ranges = mark_time_ranges
        self.include_range = include_range
        self._is_loaded = False
        self._lock = threading.Lock()
        
        if not jars:
            jars_files = os.path.join(os.path.dirname(__file__), 'jars')
            self.jars = jars_files

        if not jvm_started:
            self._classpath = self._create_classpath()
            self._start_jvm()

        try:
            # make it thread-safe
            if threading.activeCount() > 1:
                if jpype.isThreadAttachedToJVM() is not 1:
                    jpype.attachThreadToJVM()
            self._lock.acquire()

            SUTimeWrapper = jpype.JClass(
                'edu.stanford.nlp.python.SUTimeWrapper')
            self._sutime = SUTimeWrapper(
                self.mark_time_ranges, self.include_range)
            self._is_loaded = True
        finally:
            self._lock.release()

    def _start_jvm(self):
        if jpype.isJVMStarted() is not 1:
            jpype.startJVM(
                jpype.getDefaultJVMPath(),
                '-Djava.class.path={classpath}'.format(
                    classpath=self._classpath)
            )

    def _create_classpath(self):
        sutime_jar = os.path.join(*[
            imp.find_module('sutime')[1],
            'jars',
            'stanford-corenlp-sutime-python-1.0.0.jar'
        ])
        jars = [sutime_jar]
        jar_file_names = []
        for top, dirs, files in os.walk(self.jars):
            for file_name in files:
                if file_name.endswith('.jar'):
                    jars.append(os.path.join(top, file_name))
                    jar_file_names.append(file_name)
        if not SUTime._required_jars.issubset(jar_file_names):
            print([j for j in SUTime._required_jars if not j in jar_file_names])
            raise RuntimeError(
                'Not all necessary Java dependencies have been downloaded!')
        return os.pathsep.join(jars)

    def parse(self, input_str, reference_date=''):
        """Parses datetime information out of string input.

        It invokes the SUTimeWrapper.annotate() function in Java.

        Args:
            input_str: The input as string that has to be parsed.
            reference_date: Optional reference data for SUTime.

        Returns:
            A list of dicts with the result from the SUTimeWrapper.annotate()
                call.

        Raises:
            RuntimeError: An error occurres when CoreNLP is not loaded.
        """
        if self._is_loaded is False:
            raise RuntimeError('Please load SUTime first!')

        if reference_date:
            return json.loads(self._sutime.annotate(input_str, reference_date))
        return json.loads(self._sutime.annotate(input_str))
