Mutant not killed when dynamically importing module
***************************************************

Example of how dynamically importing modules allows mutations to
survive. In this case the problem is a bug in Cosmic-Ray which still
hasn't been diagnosed properly.
`Issue #157 <https://github.com/sixty-north/cosmic-ray/issues/157>`_.

Reproducer
==========

::

    pip install https://github.com/sixty-north/cosmic-ray/zipball/b3c57a3
    celery -A cosmic_ray.tasks.worker worker

    cosmic-ray run --baseline=10 example.json sandwich/ham/ham.py -- tests
    cosmic-ray report example.json
    job ID 1:Outcome.SURVIVED:sandwich.ham.ham
    command: cosmic-ray worker sandwich.ham.ham number_replacer 0 unittest -- tests
    --- mutation diff ---
    --- a/sandwich/ham/ham.py
    +++ b/sandwich/ham/ham.py
    @@ -3,6 +3,6 @@
     
     class Ham(object):
     
    -    def __init__(self, pieces=10):
    +    def __init__(self, pieces=11):
             self.pieces = pieces
     
    
    total jobs: 1
    complete: 1 (100.00%)
    survival rate: 100.00%

Verify test works
=================

In this example ``test_control.py`` properly detects the mutant when the
source code is modified by hand and the test executed manually. To verify this
edit ``sandwich/ham/ham.py`` as shown above and then execute ::

    python -m unittest tests/test_control.py 
    F
    ======================================================================
    FAIL: test_loading_via_importlib (tests.test_control.TestControl)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "~/example_01/tests/test_control.py", line 7, in test_loading_via_importlib
        self.assertEqual(ham_in_fridge.pieces, 10)
    AssertionError: 11 != 10
    
    ----------------------------------------------------------------------
    Ran 1 test in 0.000s
    
    FAILED (failures=1)


Source code
===========


.. literalinclude:: sandwich/ham/ham.py
    :caption: sandwich/ham/ham.py
    :language: python

.. literalinclude:: sandwich/control.py
    :caption: sandwich/control.py
    :language: python

.. literalinclude:: tests/test_control.py
    :caption: tests/test_control.py
    :language: python
