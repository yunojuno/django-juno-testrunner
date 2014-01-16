"""
Moderately customised test runner helpers to add in additional logging to
files to capture failures in one place and also to make re-running tests
easier.

Also adds in output colouring to make results easier to scan.
"""

import sys
import time
import unittest
import colorama

from django.utils.unittest import result
from django.conf import settings

try:
    from django.utils.unittest.signals import registerResult
except ImportError:
    def registerResult(_):
        pass

__unittest = True

colorama.init()

SET_ERROR_TEXT = colorama.Fore.RED
SET_PASS_TEXT = colorama.Fore.GREEN
SET_FAILURE_TEXT = colorama.Fore.YELLOW

SET_COUNTER_OUTPUT = colorama.Fore.YELLOW + colorama.Back.BLUE

SET_OK_OUTPUT = colorama.Fore.BLACK + colorama.Back.GREEN
SET_FAIL_OUTPUT = colorama.Fore.YELLOW + colorama.Back.RED
SET_ERROR_OUTPUT = colorama.Fore.WHITE + colorama.Back.RED + colorama.Style.BRIGHT
RESET_OUTPUT = colorama.Fore.RESET + colorama.Back.RESET + colorama.Style.RESET_ALL

class _WritelnDecorator(object):
    """Used to decorate file-like objects with a handy 'writeln' method"""
    def __init__(self, stream):
        self.stream = stream

    def __getattr__(self, attr):
        if attr in ('stream', '__getstate__'):
            raise AttributeError(attr)
        return getattr(self.stream, attr)

    def writeln(self, arg=None):
        if arg:
            self.write(arg)
        self.write('\n')  # text-mode streams translate to \r\n if needed


class TextTestResult(result.TestResult):
    """A test result class that can print formatted text results to a stream.

    Used by TextTestRunner.
    """
    separator1 = '=' * 70
    separator2 = '-' * 70

    RERUN_LOG_FILE_NAME = getattr(settings, "TEST_RUNNER_RERUN_LOG_FILE_NAME", "test_rerun.txt")
    FAILURE_LIST_FILENAME = getattr(settings, "TEST_RUNNER_FAILURE_LIST_FILENAME", "test_failures.txt")
    IMMEDIATELY_SHOW_FAILS = getattr(settings, 'TEST_RUNNER_IMMEDIATELY_SHOW_FAILS', True)

    def __init__(self, stream, descriptions, verbosity, total_tests=None):
        super(TextTestResult, self).__init__()
        self.stream = stream
        self.showAll = verbosity > 1
        self.dots = verbosity == 1
        self.descriptions = descriptions

        # Custom properties
        self.total_tests = total_tests
        self.current_test_number = 1

        self.openLogFiles()

    def startTestRun(self):
        super(TextTestResult, self).startTestRun()
        self.start_time = time.time()

    def openLogFiles(self):
        self.rerun_log_file = open(self.RERUN_LOG_FILE_NAME, "w+")
        if self.current_test_number == 1:
            self.rerun_log_file.truncate()  # zero previous content
        self.rerun_log_stream = _WritelnDecorator(self.rerun_log_file)

        self.error_log_file = open(self.FAILURE_LIST_FILENAME, "w+")
        if self.current_test_number == 1:
            self.error_log_file.truncate()  # zero previous content
        self.error_log_stream = _WritelnDecorator(self.error_log_file)

    def closeLogFiles(self):
        for _file in [
            self.rerun_log_file,
            self.error_log_file
        ]:
            try:
                _file.close()
            except AttributeError:
                pass

    def addtoErrorLog(self, test, formatted_error):
        self.error_log_stream.writeln(
            self.getDescription(test) + formatted_error + "\n" + self.separator2 + "\n"
        )

    def addToReRunLog(self, test):
        """
        Turn the descriptors for a failed test into a string that can
        be used to re-run the test later.
        """
        incantation_string = "%s.%s.%s" % (
            test.__module__,
            test.__class__.__name__,
            test._testMethodName,
        )
        self.rerun_log_stream.writeln(incantation_string)

    def getDescription(self, test):
        doc_first_line = test.shortDescription()
        if self.descriptions and doc_first_line:
            return '\n'.join((str(test), doc_first_line))
        else:
            return str(test)

    def format_time(self, time):
        return (u"%02d:%02d:%02d" % (time//3600, time//60, time%60))

    @property
    def _elapsed_time(self):
        return time.time() - self.start_time

    @property
    def _estimated_time(self):
        "Calculate and estimated time to complete the test run."
        elapsed = self._elapsed_time
        factor = float(self.total_tests) / float(self.current_test_number)
        if self.current_test_number > self.total_tests:
            return 0
        else:
            estimate = self._elapsed_time * factor
            return estimate - elapsed

    def _results_breakdown(self):
        "Return the Error, Failure, Skipped counts as a formatted string."
        return (
            (
                u"%(error_colour)s Errors: %(error_count)i%(clear)s, "
                "%(fail_colour)s Failures: %(fail_count)i%(clear)s, "
                " Skipped: %(skip_count)i, "
                "%(pass_colour)s Passed: %(pass_count)i %(clear)s"
            ) % {
                'error_colour': SET_ERROR_TEXT,
                'fail_colour': SET_FAILURE_TEXT,
                'pass_colour': SET_PASS_TEXT,
                'clear': RESET_OUTPUT,
                'error_count': len(self.errors),
                'fail_count': len(self.failures),
                'skip_count': len(self.skipped),
                'pass_count': (
                    self.current_test_number
                    - len(self.errors)
                    - len(self.failures)
                    - len(self.skipped)
                    - 1 # to account for the += 1 in startTest
                )
            }
        )

    def stopTest(self, test):
        super(TextTestResult, self).stopTest(test)

        if self.showAll:
            self.stream.writeln(
                "[..%04d <- %04d] Elapsed: %s; Remaining: %s; %s] " % (
                    self.current_test_number-1,
                    self.total_tests,
                    self.format_time(self._elapsed_time),
                    self.format_time(self._estimated_time),
                    self._results_breakdown()
                )
            )

    def startTest(self, test):
        super(TextTestResult, self).startTest(test)

        if self.showAll:
            self.stream.write(
                "%s[%04d.. -> %04d]%s " % (
                    SET_COUNTER_OUTPUT,
                    self.current_test_number,
                    self.total_tests,
                    RESET_OUTPUT
                )
            )
            self.stream.write(self.getDescription(test))
            self.stream.write(" ... ")
            self.stream.flush()
            self.current_test_number += 1

    def addSuccess(self, test):
        super(TextTestResult, self).addSuccess(test)
        if self.showAll:
            self.stream.writeln(SET_OK_OUTPUT + " OK " + RESET_OUTPUT)
        elif self.dots:
            self.stream.write(SET_OK_OUTPUT + '.' + RESET_OUTPUT)
            self.stream.flush()

    def addError(self, test, err):
        super(TextTestResult, self).addError(test, err)
        if self.showAll:
            self.stream.writeln(SET_ERROR_OUTPUT + " ERROR " + RESET_OUTPUT)
            # ALSO show the error as it happens
            formatted_err = self._exc_info_to_string(err, test)
            if self.IMMEDIATELY_SHOW_FAILS:
                self.printSingleError(
                    SET_ERROR_OUTPUT + " ERROR " + RESET_OUTPUT + " Immediate details",
                    test,
                    formatted_err
                )
            self.addtoErrorLog(test, formatted_err)
        elif self.dots:
            self.stream.write(SET_ERROR_OUTPUT + 'E' + RESET_OUTPUT)
            self.stream.flush()

        self.addToReRunLog(test)

    def addFailure(self, test, err):
        super(TextTestResult, self).addFailure(test, err)

        if self.showAll:
            self.stream.writeln(SET_FAIL_OUTPUT + " FAIL " + RESET_OUTPUT)
            # ALSO show the error as it happens
            formatted_err = self._exc_info_to_string(err, test)
            if self.IMMEDIATELY_SHOW_FAILS:
                self.printSingleError(
                    SET_FAIL_OUTPUT + " FAIL " + RESET_OUTPUT + " Immediate details",
                    test,
                    formatted_err
                )
            self.addtoErrorLog(test, formatted_err)
        elif self.dots:
            self.stream.write(SET_FAIL_OUTPUT + 'F' + RESET_OUTPUT)
            self.stream.flush()

        self.addToReRunLog(test)

    def addSkip(self, test, reason):
        super(TextTestResult, self).addSkip(test, reason)
        if self.showAll:
            self.stream.writeln("skipped %r" % (reason,))
        elif self.dots:
            self.stream.write("s")
            self.stream.flush()

    def addExpectedFailure(self, test, err):
        super(TextTestResult, self).addExpectedFailure(test, err)
        if self.showAll:
            self.stream.writeln("expected failure")
        elif self.dots:
            self.stream.write("x")
            self.stream.flush()

    def addUnexpectedSuccess(self, test):
        super(TextTestResult, self).addUnexpectedSuccess(test)
        if self.showAll:
            self.stream.writeln("unexpected success")
        elif self.dots:
            self.stream.write("u")
            self.stream.flush()

    def printErrors(self):
        if self.dots or self.showAll:
            self.stream.writeln()
        self.printErrorList('ERROR', self.errors)
        self.printErrorList('FAIL', self.failures)

    def printErrorList(self, flavour, errors):
        for test, err in errors:
            self.printSingleError(flavour, test, err)

    def printSingleError(self, flavour, test, err):
        self.stream.writeln(self.separator1)
        self.stream.writeln("%s: %s" % (flavour, self.getDescription(test)))
        self.stream.writeln(self.separator2)
        # at this point, err is a tuple of:
        # (type, exception, traceback)
        self.stream.writeln("%s" % err)

    def stopTestRun(self):
        super(TextTestResult, self).stopTestRun()
        self.printErrors()


class TextTestRunner(unittest.TextTestRunner):
    """A test runner class that displays results in textual form.

    It prints out the names of tests as they are run, errors as they
    occur, and a summary of the results at the end of the test run.
    """
    resultclass = TextTestResult

    def __init__(
            self,
            stream=sys.stderr,
            descriptions=True,
            verbosity=1,
            failfast=False,
            buffer=False,
            resultclass=None,
            total_tests=None
    ):
        self.stream = _WritelnDecorator(stream)
        self.descriptions = descriptions
        self.verbosity = verbosity
        self.failfast = failfast
        self.buffer = buffer
        if resultclass is not None:
            self.resultclass = resultclass
        self.total_tests = total_tests

    def _makeResult(self):
        return self.resultclass(
            self.stream,
            self.descriptions,
            self.verbosity,
            total_tests=self.total_tests
        )

    def run(self, test):
        "Run the given test case or test suite."
        result = self._makeResult()
        result.failfast = self.failfast
        result.buffer = self.buffer
        registerResult(result)

        startTime = time.time()
        startTestRun = getattr(result, 'startTestRun', None)
        if startTestRun is not None:
            startTestRun()
        try:
            test(result)
        finally:
            stopTestRun = getattr(result, 'stopTestRun', None)
            if stopTestRun is not None:
                stopTestRun()
            else:
                result.printErrors()
        stopTime = time.time()
        timeTaken = stopTime - startTime
        if hasattr(result, 'separator2'):
            self.stream.writeln(result.separator2)
        run = result.testsRun
        self.stream.writeln("Ran %d test%s in %.3fs" %
                            (run, run != 1 and "s" or "", timeTaken))
        self.stream.writeln()

        expectedFails = unexpectedSuccesses = skipped = 0
        try:
            results = map(len, (result.expectedFailures,
                                result.unexpectedSuccesses,
                                result.skipped))
            expectedFails, unexpectedSuccesses, skipped = results
        except AttributeError:
            pass
        infos = []
        if not result.wasSuccessful():
            self.stream.write(SET_FAIL_OUTPUT + " FAILED " + RESET_OUTPUT)
            failed, errored = map(len, (result.failures, result.errors))
            if failed:
                infos.append("%sfailures=%d%s" % (SET_FAILURE_TEXT, failed, RESET_OUTPUT))
            if errored:
                infos.append("%serrors=%d%s" % (SET_ERROR_TEXT, errored, RESET_OUTPUT))
        else:
            self.stream.write(SET_OK_OUTPUT + " OK " + RESET_OUTPUT)
        if skipped:
            infos.append("skipped=%d" % skipped)
        if expectedFails:
            infos.append("expected failures=%d" % expectedFails)
        if unexpectedSuccesses:
            infos.append("unexpected successes=%d" % unexpectedSuccesses)
        if infos:
            self.stream.writeln(" (%s)" % (", ".join(infos),))
        else:
            self.stream.write("\n")

        result.closeLogFiles()
        return result