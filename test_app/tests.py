from django.test import TestCase, TransactionTestCase


class JunorunnerTestCase(TestCase):

    def test_can_run_tests(self):
        pass

    def test_counts_tests_correctly(self):
        """
        Added this test to make sure the number of tests != number of
        test cases (so that we can assert the total count is correct
        when running tests in parallel)
        """
        pass


class JunorunnerTransactionTestCase(TransactionTestCase):

    def test_can_run_transaction_bound_tests(self):
        pass
