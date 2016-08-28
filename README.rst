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

Make sure your tools work
=========================

Mutation testing relies on dynamically modifying program modules and
loading the mutated instance from memory. Depending on the language specifics
there may be several ways to refer to the same module. In Python
the following are equivalent

.. code-block:: python

    import sandwich.ham.ham
    obj = sandwich.ham.ham.SomeClass()

    from sandwich.ham import ham
    obj = ham.SomeClass()

.. note::

    The equivalency here is in terms of having access to the same module API.

When we mutation test the right-most ``ham`` module our tools may not
be able to resolve to the same module if various importing styles are used.
For example see :doc:`python/example_00/README`.

Another possible issue is with programs that load modules dynamically or
change the module search path at runtime. Depending on how the
mutation testing tool works these operations may interfere with it.
For example see :doc:`python/example_01/README`.

TL,DR: explore your test tool first and manually verify the results before
going further. Unless you know the tools don't trust them!

Make sure your tests work
=========================

Mutation testing relies on the fact that your test suite will fail when a
mutation is introduced. In turn any kind of failure will kill the mutant!
The mutation test tool has no way of knowing whether your test suite failed
because the mutant tripped one of the assertions or whether it failed due
to other reasons.

For example see :doc:`python/example_02/README`.

TL,DR: make sure your test suite is robust and doesn't randomly fail due to
external factors!



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

TL,DR: Good source code and test organization will allow easy division of test
runs and tremendously speed up your mutation testing execution time!

Fail fast
=========

Mutation testing relies on your test suite failing when it detects a
faulty mutation. It doesn't matter which particular test has failed because
most of the tools have no way of telling whether or not the failed test is
related to the mutated code. That means it also doesn't matter if there are
more than one failing tests so you can use this to your advantage.

TL,DR: Whenever your test tools and framework support the **fail fast** option
make use of it to reduce test execution time even more!

Python: Refactor if string != ""
================================

Comparison operators may be mutated with each other which gives,
depending on the langauge about 10 possible mutations.

Every time ``string`` is not an empty string the following 3 variants
are evaluated to ``True``:

* ``if string != ""``
* ``if string > ""``
* ``if string not in ""``

The existing test cases pass and these mutations are never killed.
Refactoring this to ::

    if string:
        do_something()


is the best way to go about it. This also reduces the total number of
possible mutations.

For example see :doc:`python/example_03/README`

TL,DR: Refactor ``if string != "":`` to ``if string:``!


Python: Testing for X != 1
==========================

When testing the not equals condition we need at least 3 test cases:

* Test with value smaller than the condition
* Test with value that equals the condition
* Test with value greater than the condition

Most often we do test with value that equals the condition (the golden scenario)
and either one of the other bordering values but not both. This
leads to mutations which are not killed.

Example :doc:`python/example_04/README`.

TL,DR: when testing ``X != INT`` test with values ``INT-1``, ``INT`` and
``INT+1`` to cover all possible scenarios.


Python: Refactor if X != 0
==========================

TL,DR: Refactor ``if X != 0:`` to ``if X:``!


Python: Refactor if len(list) != 0
==================================

Every time ``list`` is not an empty list the following variants
are evaluated to ``True`` and result in surviving mutants:

* ``if len(lst) != 0``
* ``if len(lst) > 0``

Additionally if we don't have a test to validate the ``if`` body,
for example that it raises an exception, then the following mutation
will also survive:

* ``if len(lst) < 0``

Refactoring this to ::

    if list:
        do_something()


is the best way to go about it. This also reduces the total number of
possible mutations.

For example see :doc:`python/example_05/README`.

TL,DR: Refactor ``if len(list) != 0:`` to ``if list:``!


Python: Refactor if len(list) == 0
==================================

Refactoring this to ::

    if not list:
        do_something()


TL,DR: Refactor ``if len(list) == 0:`` to ``if not list:``!


Python: Refactor if len(list) > 0
=================================

This is similar to the previous pattern and doesn't need a comprehensive
example. In fact lists can't have negative length so both examples are
equivalent in practice.

TL,DR: Refactor ``if len(list) > 0:`` to ``if list:``!


Python: Refactor if X is None
=============================

When X has a value of None the following mutations are equivalent
are will survive:

* ``if X is None:``
* ``if X == None:``

in addition static analyzers will often report comparison to None
as an offence.

For example see :doc:`python/example_06/README`.


TL,DR: Refactor ``if X is None:`` to ``if not X:``


Python: Testing __eq__ and __ne__
=================================

For example see :doc:`python/example_07/README`.


TL,DR: Compare object to itself, None and then change the attributes
one by one to fully test custom equality methods.


Python: Testing sequence of if == int
=====================================

To completely test the following pattern

.. code-block:: python

    if X == int_1:
        pass
    elif X == int_2:
        pass
    elif X == int_3:
        pass

you need to test with values outside the allowed set.
For example see :doc:`python/example_08/README`

TL,DR: test with all descrete values and then with values
outside the allowed set.


Python: Missing or extra parameters
===================================

Depending on how your method signature is defined it is possible to either
accept additional parameters which are not needed or forget to pass along
parameters which control internal behavior. Mutation testing helps you
identify those cases and adjust your code accordingly.

For example see :doc:`python/example_09/README`.


Python: On boolean expressions
==============================

When dealing with non-trivial boolean expressions mutation testing often helps
put things into perspective.
For example see :doc:`python/example_10/README`.





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

