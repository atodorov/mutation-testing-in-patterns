Testing __eq__ & __ne__
***********************

This is an example of testing overriden ``__eq__`` and ``__ne__`` methods.
In this example objects are identified by the value of their attributes.
There is an example where attributes are of the same type and an example
where attributes are of different types.

To kill all mutants we have to exercise all possible methods and comparison
branches in them, see source comments for more info.

Once we've stablished what is equal and how that compares to ``None`` and itself
we can start testing comparisons by modifying the attribute values one by one.
Note that equality comparison works both ways, that is ``X == Y`` is the same
as ``Y == X`` so we test it that way.

Comment out the ``test_default_objects_are_always_equal()`` method and one of
the ``assertNotEqual(sandwich_1, sandwich_2)`` lines and re-test to see the
difference in results!

Reproducer
==========

::

    $ pip install nose
    $ pip install https://github.com/sixty-north/cosmic-ray/zipball/master

    $ cosmic-ray run --test-runner nose --baseline=10 example.json sandwich.py -- tests.py
    $ cosmic-ray report example.json --full-report


Source code
===========


.. literalinclude:: sandwich.py
    :caption: sandwich.py
    :language: python

.. literalinclude:: tests.py
    :caption: tests.py
    :language: python
