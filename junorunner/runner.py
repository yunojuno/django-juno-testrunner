from django.test.runner import DiscoverRunner
from junorunner.extended_runner import TextTestRunner


class JunoDiscoverRunner(DiscoverRunner):
    """
    The only real difference between this and the standard DiscoverRunner in Django 1.6+
    is the use of the custom TextTestRunner, which we hook in via run_suite()
    """

    def run_suite(self, suite, **kwargs):
        return TextTestRunner(
            verbosity=self.verbosity,
            failfast=self.failfast,
            total_tests=len(suite._tests)
        ).run(suite)
