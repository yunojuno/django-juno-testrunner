from __future__ import print_function

from .runner import JunoDiscoverRunner


class TestSuiteRunner(JunoDiscoverRunner):
    """
    Extended version of the standard Django test runner to support:

    * immediately showing error details during test progress, in addition
        to showing them once the suite  has completed
    * logging the dotted path for the failing tests to a file to make it
        easier to re-run failed tests via the YJ run_tests Fabric task
    * numbering tests/showing a progress counter
    * colourised output (and yes, that's the correct spelling of 'colourised' ;-) )

    """

    def __init__(self, *args, **kwargs):
        self.slow_test_count = int(kwargs.get('slow_test_count', 0))
        super(TestSuiteRunner, self).__init__(*args, **kwargs)

    @classmethod
    def add_arguments(cls, parser):
        super(TestSuiteRunner, cls).add_arguments(parser)
        parser.add_argument('-s', '--slow-tests',
            action='store',
            dest='slow_test_count',
            default=0,
            help="Print given number of slowest tests"
        )

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        """
        Run the unit tests for all the test labels in the provided list.
        """
        self.setup_test_environment()
        suite = self.build_suite(test_labels, extra_tests)

        print("%i tests found" % self.get_test_count(suite))

        old_config = self.setup_databases()
        result = self.run_suite(suite)
        self.teardown_databases(old_config)
        self.teardown_test_environment()
        return self.suite_result(suite, result)
