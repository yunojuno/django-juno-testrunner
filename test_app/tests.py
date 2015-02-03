from django.test import TestCase, TransactionTestCase


class JunorunnerTestCase(TestCase):

    def test_can_run_tests(self):
        pass


class JunorunnerTransactionTestCase(TransactionTestCase):

    def test_can_run_transaction_bound_tests(self):
        pass
