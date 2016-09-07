from django.test.runner import DiscoverRunner
from junorunner.extended_runner import TextTestRunner

try:
    # Django 1.6
    from django.utils import unittest
except ImportError:
    # Django 1.7+ because bundled unittest is going away
    import unittest


class JunoTestLoader(unittest.TestLoader):
    def loadTestsFromName(self, name, module=None):
        if name.startswith('unittest.loader.ModuleImportFailure'):
            name = name[36:]

        return super(JunoTestLoader, self).loadTestsFromName(name,
                                                             module=module)


class JunoDiscoverRunner(DiscoverRunner):
    """
    The only real difference between this and the standard DiscoverRunner in Django 1.6+
    is the use of the custom TextTestRunner, which we hook in via run_suite()
    """
    def get_test_count(self, suite):
        """
        When running tests in parallel, a core suite is generated to contain a collection of
        sub-suites that are then ran in parallel.

        In that case we have to go and retrieve the count from each of the sub-suites as
        the parent will not directly contain the tests.
        """
        if getattr(self, 'parallel', 1) > 1:
            return sum([len(subsuite._tests) for subsuite in suite.subsuites])
        return len(suite._tests)

    test_loader = JunoTestLoader()

    def run_suite(self, suite, **kwargs):
        return TextTestRunner(
            verbosity=self.verbosity,
            failfast=self.failfast,
            total_tests=self.get_test_count(suite),
            slow_test_count=self.slow_test_count
        ).run(suite)
