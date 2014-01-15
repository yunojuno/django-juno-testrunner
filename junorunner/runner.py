
from django.test.runner import DiscoverRunner

# import os
# from optparse import make_option

# from django.conf import settings
# from django.core.exceptions import ImproperlyConfigured
# from django.test import TestCase
# from django.test.utils import setup_test_environment, teardown_test_environment
# from django.utils import unittest
# from django.utils.unittest import TestSuite, defaultTestLoader

# CUSTOM IMPORT
from utils.unittest.extended_runner import TextTestRunner  # this is rather than unittest.TextTestRunner

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
