Mutant not killed due to module import issue
********************************************

Example of how importing modules under different names allows mutations to
survive. In this case the problem is related to how Cosmic-Ray loads the
mutated modules. It has already been fixed in
`PR #158 <https://github.com/sixty-north/cosmic-ray/pull/158>`_.

Reproducer
==========

::

    pip install https://github.com/sixty-north/cosmic-ray/zipball/2a48656
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

.. note::

    In this example ``test_control.py`` properly kills the mutant once
    the above issue is fixed.

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
