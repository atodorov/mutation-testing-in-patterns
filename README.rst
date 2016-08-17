Mutation Testing in Patterns
****************************

.. image:: https://readthedocs.org/projects/mutation-testing-patterns/badge/?version=latest
    :target: http://mutation-testing-patterns.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

Mutation testing is a technique used to evaluate the quality of existing software
tests. Mutation testing involves modifying a program in small ways, for example
replacing ``True`` constants with ``False`` and re-running its test suite.
When the test suite fails the *mutant* is *killed*. This tells us how good the
test suite is. The goal of this paper is to describe different software and
testing patterns related using practical examples.

Some of them are language specific so please see the relevant sections for
information about installing and running the necessary tools and examples.

.. toctree::
   :maxdepth: 2

Make sure your tests work
=========================

Mutation testing relies on the fact that your test suite will fail when a
mutation is introduced. In turn any kind of failure is said to kill the mutant.
The mutation test tool has no way of knowing whether your test suite failed
because the mutant tripped one of the test cases or whether it failed due
to other reasons.

One possible source of failures comes from software which dynamically loads
modules or changes the module load path at runtime. Depending on how the
mutation testing tool works these operations may interfere with it.


TODO: For example Python

When starting with mutation testing get to know how your tools work
internally and experiment one module at a time to make sure everything
is working as expected!

Divide and conquer
==================

The basic mutation test algorithm is this

.. code-block:: python

    for operator in mutation-operators:
        for site in operator.sites(code):
            operator.mutate(site)
            run_tests()

- **mutation-operators** are the things that make small changes to your code
- **operator.sites** are the places in your code where this operator can be
  applied


As you can see mutation testing is a very expensive operation. For example
the `pykickstart <http://github.com/rhinstaller/pykickstart>`_ project
started with 5523 possible mutations and 347 tests, which took on average
100 seconds to execute. A full mutation testing execution needs more than
6 days to complete!

In practice however not all tests are related to, or even make use of
all program modules. This means that mutated operators are only tested via
subset of the entire test suite. This fact can be used to reduce
execution time by scheduling mutation tests against each individual
file/module using only the tests which are related to it.
The best case scenario is when your source file names map directly to
test file names.

For example something like this

.. code-block:: bash

    for f in `find ./src -type f -name "*.py" | sort`; do
        TEST_NAME="tests/$f"
        runTests $f $TEST_NAME
    done

Where **runTests** executes the mutation testing tool against a single file
and executes only the test which is related to this file.
For *pykickstart* this approach reduced  the entire execution time to little
over 6 hours!

Good source code and test organization will allow easy division of test
runs and tremendously speed up your mutation testing execution time!

Fail fast
=========

Mutation testing relies on your test suite failing when it detects a
faulty mutation. It doesn't matter which particular test has failed because
most of the tools have no way of telling whether or not the failed test is
related to the mutated code. That means it also doesn't matter if there are
more than one failing tests so you can use this to your advantage.

Whenever your test tools and framework support the **fail fast** option
make use of it to reduce test execution time even more!


Appendix. Mutation testing with Python
======================================

`Cosmic-Ray <https://github.com/sixty-north/cosmic-ray>`_ is the mutation testing
tool for Python. It is recommended that you install the latest version from git::

    pip install https://github.com/sixty-north/cosmic-ray/zipball/master

*Cosmic-Ray* uses *Celery* to allow concurrent execution of workers (e.g.
mutation test jobs). To start the worker ::

    cd myproject/
    celery -A cosmic_ray.tasks.worker worker

To execute a test job (called session) use a different terminal and ::

    cd myproject/
    cosmic-ray run --baseline=10 session_name.json some/module.py -- tests/some/test.py

.. note::

    Test runner and additional test parameters can be specified. Refer to Cosmic-Ray's
    documentation for more details!

To view the mutation results execute ::

    cosmic-ray report session_name.json

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

