django-juno-testrunner
======================

    .. image:: https://travis-ci.org/yunojuno/django-juno-testrunner.svg?branch=master
        :target: https://travis-ci.org/yunojuno/django-juno-testrunner

This is a drop-in test-runner alternative for Django 1.6+ which takes DiscoverRunner and adds the following:

- Generates a file with all failed or errored test output for inspection later
- Generates a file listing the dot-separated paths of all failed or errored tests to make it easy to re-run just the failed ones
- Displays test failure messages/tracebacks as they happen, without stopping the rest of the tests running
- Displays a countdown of tests as they run, showing each test's number out of the total
- Displays the elapsed time so far and a (rough) estimate of how long the remaining tests will take
- Colourised output to make it easier to grok how your test run is going (Plus, it's prettier)

The Python package you get, if you're interested, is called ``junorunner``. That's because it came from the `YunoJuno <https://www.yunojuno.com/>`_ codebase, and we'd put all of our pun skills into copy for the site, so we played it safe this time.

Installation
------------

1. Recommended installation is via **pip**, inside a **virtualenv**.

To get it from **PyPi** et al::

    $ pip install django-juno-testrunner

If you want the bleeding-edge version from GitHub::

    $ pip install -e git+ssh://git@github.com/YunoJuno/django-juno-testrunner.git#egg=django-juno-testrunner

Downloading the package's source and installing it yourself is also an option.

Once downloaded, run::

    $ python setup.py

But you knew that already, yep?

``django-juno-testrunner`` has one automatically installed dependency, the delightful `colorama <https://pypi.python.org/pypi/colorama>`_.

2. Update your ``settings.py`` to use this test runner::

    TEST_RUNNER = 'junorunner.testrunner.TestSuiteRunner'

3. Set some options, if you want.

By default, ``junorunner`` will show you test errors and failures as they happen, inline in the test output, so you can ponder them while waiting for the rest of the suite to run. You can disable this, of course::

    TEST_RUNNER_IMMEDIATELY_SHOW_FAILS = False

Also by default, ``junorunner`` puts the traceback from all test failures and errors in a file called 'test_failures.txt' in the project root. Alongside that is a file with the name of each failed test in full dot-separated syntax, one test per line, to make it easier to re-run just your failed tests (more on that later). If you don't like the default names, go to town with your own choices::

    TEST_RUNNER_RERUN_LOG_FILE_NAME = 'must_try_harder.txt'
    TEST_RUNNER_FAILURE_LIST_FILENAME = 'post_mortem.txt'

That's it.

Usage
-----

Running tests
'''''''''''''

``junorunner`` will replace the default Django 1.6+ DiscoverRunner so run your tests as 'normal', whether that's via a straight ``./manage.py test`` or Fabric or some big red button and an Arduino, as long as ``manage.py test`` is ultimately called, it's all good.

You'll get the most informative in-flight output with `--verbosity=2`.

When your test run is over, you'll get the usual detailed failure and error output, if any, plus there'll be the failures list (default name ``test_failures.txt``) and the rerun log (``test_rerun.txt``) in your project directory. If all your tests passed, these files will still exist, but will be empty.

Note that as soon as you start a new test run (even if you then Ctrl-C it to death or use an axe to cut the power cable), the contents of those files will be immediately zapped.

Using the rerun log
'''''''''''''''''''

If you're not sure how to to pump the dot-separated failed tests back into the test client, you can do this way::

    $ ./manage.py test $(cat test_rerun.txt)  # POSIX

or ::

    $ ./manage.py test $(< test_rerun.txt)  # bash


Generating JUnit compatible XML
'''''''''''''''''''''''''''''''

If you are running your tests in an environment that can process JUnit XML files (e.g. in Jenkins), you may want to set ``TEST_RUNNER_JUNIT_XML``::

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


