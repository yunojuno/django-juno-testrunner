.. image:: https://badge.fury.io/py/django-juno-testrunner.svg
    :target: https://badge.fury.io/py/django-juno-testrunner

.. image:: https://travis-ci.org/yunojuno/django-juno-testrunner.svg?branch=master
    :target: https://travis-ci.org/yunojuno/django-juno-testrunner

django-juno-testrunner
======================

This is a drop-in test-runner alternative for Django which adds the following:

- Generates a file with all failed or errored test output
- Generates a file listing the dot-separated paths of all failed
- Displays test failure messages/tracebacks as they happen
- Displays a countdown of tests as they run
- Displays the elapsed time and an estimate of time remaining
- Colourised output

Requirements
------------

This package is tested against Django 1.8-1.11, and Python 2.7, 3.4, 3.5, 3.6.
Other combinations _may_ work, but are not included in the CI build. It also
requires ``colorama``, which is used to provide colour output.

Installation
------------

Recommended installation is via **pip**:

.. code:: python

    $ pip install django-juno-testrunner

Update your ``settings.py`` to use this test runner:

.. code:: python

    TEST_RUNNER = 'junorunner.testrunner.TestSuiteRunner'

Options
-------

By default, ``junorunner`` will show you test errors and failures as they happen, inline in the test output. You can disable this:

.. code:: python

    TEST_RUNNER_IMMEDIATELY_SHOW_FAILS = False

By default ``junorunner`` puts the traceback from all test failures and errors
in a file called 'test_failures.txt' in the project root. Alongside that is a
file with the name of each failed test in full dot-separated syntax, to make
it easier to re-run just your failed tests. You can override the file names:

.. code:: python

    TEST_RUNNER_RERUN_LOG_FILE_NAME = 'must_try_harder.txt'
    TEST_RUNNER_FAILURE_LIST_FILENAME = 'post_mortem.txt'

Usage
-----

Running tests
'''''''''''''

``junorunner`` will replace the default Django ``DiscoverRunner`` so will run
your tests without any further change. It supports standard options, e.g. you
can use ``--verbosity=2`` for more detail. When your test run is over, you'll
get the usual detailed failure and error output, plus there'll be the failures
list (default name ``test_failures.txt``) and the rerun log (``test_rerun.txt``)
in your project directory.

**NB the rerun and failure files are deleted as soon as a new test run is started.**

Using the rerun log
'''''''''''''''''''

You can rerun all of the failed tests using the ``test_rerun.txt`` contents:

.. code:: shell

    $ ./manage.py test $(cat test_rerun.txt)  # POSIX

or

.. code:: shell

    $ ./manage.py test $(< test_rerun.txt)  # bash


Generating JUnit compatible XML
'''''''''''''''''''''''''''''''

If you are running your tests in an environment that can process JUnit XML files (e.g. in Jenkins), you may want to set ``TEST_RUNNER_JUNIT_XML``:

.. code:: python

    TEST_RUNNER_JUNIT_XML = os.path.join(BASE_DIR, 'junit.xml')

Roadmap
-------

- improve time-left-to-run estimate

Contributing
------------

Contributions and bug reports are welcome. Pull requests adding jazzy new features are even more welcome.

Thanks to:

* Tom Wardill for Python3 support - https://github.com/tomwardill
* Gergely Polonkai for JUnit XML support - https://github.com/gergelypolonkai
