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

Mutation testing tools
======================

This is a list of mutation testing tools which are under active use and
maintenance from the community:

* Python  
    * `Cosmic Ray <https://github.com/sixty-north/cosmic-ray>`_
    * `mutmut <https://github.com/boxed/mutmut>`_
* Ruby - `Mutant <https://github.com/mbj/mutant>`_
* Java - `Pitest <https://github.com/hcoles/pitest>`_
* JavaScript - `Stryker <https://github.com/stryker-mutator/stryker>`_
* PHP - `Humbug <https://github.com/padraic/humbug>`_

For LLVM-based languages such as C, C++, Rust and Objective-C checkout
[mull](https://github.com/mull-project/mull), which looks like a nice project
but may not be ready for production use!


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


Make sure your tests work
=========================

Mutation testing relies on the fact that your test suite will fail when a
mutation is introduced. In turn any kind of failure will kill the mutant!
The mutation test tool has no way of knowing whether your test suite failed
because the mutant tripped one of the assertions or whether it failed due
to other reasons.


Make sure your test suite is robust and doesn't randomly fail due to
external factors!
For example see :doc:`python/example_02/README`.



Divide and conquer
==================

The basic mutation test algorithm is this

.. code-block:: python

    for operator in mutation-operators:
        for site in operator.sites(code):
            operator.mutate(site)
            run_tests()

- **mutation-operators** are the things that make small changes to your code
- **operator.sites** are the places in your code where operators can be
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

.. note::

    Other tools and languages may have a convention of how tests are organized or
    which tests are executed by the mutation testing tool. For example in Ruby the
    convention is to have all tests under `spec/*_spec.rb` which maps with the idea
    proposed above. Mutant, the Ruby mutation testing tool, uses this convention to
    find the tests it needs. For Python, on the other hand, the user needs to manually
    specify which tests should be executed!


Fail fast
=========

Mutation testing relies on your test suite failing when it detects a
faulty mutation. It doesn't matter which particular test has failed because
most of the tools have no way of telling whether or not the failed test is
related to the mutated code. That means it also doesn't matter if there are
more than one failing tests so you can use this to your advantage.

Whenever your test tools and framework support the **fail fast** option
make use of it to reduce test execution time even more!

Refactor comparison to empty string
===================================

Comparison operators may be mutated with each other which gives,
depending on the langauge, about 10 possible mutations.

Every time ``S`` is not an empty string the following 3 variants
are evaluated to ``True``:

* ``if S != ""``
* ``if S > ""``
* ``if S not in ""``

The existing test cases pass and these mutations are never killed.
In languages like Python, non-empty sequences are evaluated to `True` in boolean
context and you don't need to use comparisons. This reduces the number of
possible mutations.

For Python you may use the *emptystring* extension of pylint

.. code-block:: bash

    pylint a.py --load-plugins=pylint.extensions.emptystring

See `pylint #1183 <https://github.com/PyCQA/pylint/pull/1183>`_ for more info and
:doc:`python/example_03/README` for an example.

.. warning::

    In some cases empty string is an acceptable value and refactoring will
    change the behavior of the program! Be careful when doing this.


Refactor comparison to zero
===========================

This is similar to the previous section but for integer values. For Python use
the *comparetozero* extension to detect possible offenses.

.. code-block:: bash

    pylint a.py --load-plugins=pylint.extensions.comparetozero

See `pylint #1243 <https://github.com/PyCQA/pylint/pull/1243>`_ for more info.


Python: Refactor len(X) comparisons to zero
===========================================

Every time ``X`` is not an empty sequence the following variants
are evaluated to ``True`` and result in surviving mutants:

* ``if len(X) != 0``
* ``if len(X) > 0``

Additionally if we don't have a test to validate the ``if`` body,
for example that it raises an exception, then the following mutation
will also survive:

* ``if len(X) < 0``

Refactoring this to ::

    if X:
        do_something()


is the best way to go about it. This also reduces the total number of
possible mutations. A more
complicated example, using two lists and boolean operation can be
seen below.

.. code-block:: diff

    -   if len(self.disabled) == 0 and len(self.enabled) == 0:
    +   if not (self.disabled or self.enabled):


Consider the following example

.. code-block:: python

    # All the port:proto strings go into a comma-separated list.
    portstr = ",".join(filteredPorts)
    if len(portstr) > 0:
        portstr = " --port=" + portstr
    else:
        portstr = ""

Similar to previous examples the ``len() > 0`` expression can be refactored.
Since joining an empty list will produce an empty string the ``else`` block
is not necessary. The example can be re-written as

.. code-block:: python

    # All the port:proto strings go into a comma-separated list.
    portstr = ",".join(filteredPorts)
    if portstr:
        portstr = " --port=" + portstr

In pylint 2.0 there is a new checker called *len-as-condition* which will
warn you about code snippets that compare the result of a `len()` call to zero.
For more information see
`pylint #1154 <https://github.com/PyCQA/pylint/pull/1154>`_.

For practical example see :doc:`python/example_05/README`.


Python: Refactor if len(list) == 1
==================================

The following code

.. code-block:: python

    if len(ns.password) == 1:
        self.password = ns.password[0]
    else:
        self.password = ""


can be refactored into this

.. code-block:: python

    if ns.password:
        self.password = ns.password[0]
    else:
        self.password = ""

.. warning::

    This refactoring may have side effects when the list length is greater
    than 1, e.g. 2. Depending on your program this may ot may-not be the case.


Testing for X != 1
==================

When testing the not equals condition we need at least 3 test cases:

* Test with value smaller than the condition
* Test with value that equals the condition
* Test with value greater than the condition

Most often we do test with value that equals the condition (the golden scenario)
and either one of the other bordering values but not both. This
leads to mutations which are not killed.

Example :doc:`python/example_04/README`.


Python: Refactor if X is None
=============================

When X has a value of None the following mutations are equivalent
are will survive:

* ``if X is None:``
* ``if X == None:``

in addition static analyzers may report comparison to None
as an offence. To handle this refactor
``if X is None:`` to ``if not X:`` when possible.


For example see :doc:`python/example_06/README`.


Python: Refactor if X is not None
=================================

This is the opposite of the previous section.
Refactor ``if X is not None:`` to ``if X:``.
For example see :doc:`python/example_11/README`.



Python: Testing __eq__ and __ne__
=================================

When objects are compared by comparing their attributes then full
mutation test coverage can be achieved by comparing the object to itself,
comparing to None, comparing two objects with the same attribute values
and then test by changing the attributes one by one.

For example see :doc:`python/example_07/README`.

Consider if there is the following mistake in the example:

.. code-block:: python

    def __eq__(self, other):
        if not y:
            return False

        return self.device and self.device == y.device

Notice the redundant `self.device and` in the expression above!
When `self.device` contains a value (string in this case) the expression is
equivalent to `self.device == other.device`. On the other hand when
`self.device` is `None` or an empty string the expression will always return `False`!

If we have all of the above tests (which mutation testing has identified)
then our test suite will fail and properly detect the defect ::

    $ python -m nose -- tests.py
    F.....
    ======================================================================
    FAIL: Newly created objects with the same attribute values
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "~/example_07/tests.py", line 15, in test_default_objects_are_always_equal
        self.assertEqual(self.sandwich_1, self.sandwich_2)
    AssertionError: <sandwich.Sandwich object at 0x7f4603cece80> != <sandwich.Sandwich object at 0x7f4603ceceb8>

    ----------------------------------------------------------------------
    Ran 6 tests in 0.001s

    FAILED (failures=1)

.. note::

    At the time of writing *Cosmic Ray* did not fail if there was a failure
    during the baseline test execution and all mutations would be reported as killed
    because, well the test suite failed! This was reported in
    `CR#111 <https://github.com/sixty-north/cosmic-ray/issues/111>`_ and fixed in
    `CR#181 <https://github.com/sixty-north/cosmic-ray/pull/181>`_.


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

you need to test with all descrete values plus values outside the allowed set.
For example see :doc:`python/example_08/README`


Python: Testing sequence of if == string
========================================

To fully test the following pattern

.. code-block:: python

    if X == "string_1":
        pass
    elif X == "string_2":
        pass
    elif X == "string_3":
        pass

you need to test with all possible string values as well as with values
outside the allowed set. For example see :doc:`python/example_08/README_str`.


Python: Missing or extra parameters
===================================

Depending on how your method signature is defined it is possible to either
accept additional parameters which are not needed or forget to pass along
parameters which control internal behavior. Mutation testing helps you
identify those cases and adjust your code accordingly.

For example see :doc:`python/example_09/README`.


Python: Testing for 0 <= X < 100
=================================


When testing numerical ranges we need at least 4 tests:

* Test with both border values
* Test with values outside the range, ideally +1/-1
* Testing with a value in the middle of the range is not required
  for full mutation coverage!

For example see :doc:`python/example_12/README`.


Python: On boolean expressions
==============================

When dealing with non-trivial boolean expressions mutation testing often helps
put things into perspective. It causes you to rethink the expression which often
leads to refactoring and killing mutants.
For example see :doc:`python/example_10/README`.


Refactor multiple boolean expressions
=====================================

Consider the following code where the expression left of ``and``
is always the same

.. code-block:: python

    if name == "method":
        self._clear_seen()

    if name == "method" and value == "cdrom":
        setattr(self.handler.cdrom, "seen", True)
    elif name == "method" and value == "harddrive":
        setattr(self.handler.harddrive, "seen", True)
    elif name == "method" and value == "nfs":
        setattr(self.handler.nfs, "seen", True)
    elif name == "method" and value == "url":
        setattr(self.handler.url, "seen", True)

This can easily be refactored by removing the
``name == "method"`` expression and making the subsequent if
statements nested under the first one.

.. code-block:: python

    if name == "method":
        self._clear_seen()

        if value == "cdrom":
            setattr(self.handler.cdrom, "seen", True)
        elif value == "harddrive":
            setattr(self.handler.harddrive, "seen", True)
        elif value == "nfs":
            setattr(self.handler.nfs, "seen", True)
        elif value == "url":
            setattr(self.handler.url, "seen", True)

The refactored code is shorter and provides less mutation sites thus
reducing overall mutation test execution time.
This code can be refactored even more aggressively into

.. code-block:: python

    if name == "method":
        self._clear_seen()

        if value in ["cdrom", "harddrive", "nfs", "url"]:
            setattr(getattr(self.handler, value), "seen", True)



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
