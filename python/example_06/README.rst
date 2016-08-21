Refactor if X is None
*********************

Reproducer
==========

::

    $ pip install nose
    $ pip install https://github.com/sixty-north/cosmic-ray/zipball/master
    $ celery -A cosmic_ray.tasks.worker worker

    $ cosmic-ray run --test-runner nose --baseline=10 example.json hello.py -- test_hello.py
    $ cosmic-ray report example.json
    
    job ID 4:Outcome.SURVIVED:hello
    command: cosmic-ray worker hello replace_Is_with_Eq 0 nose -- -v test_hello.py
    --- mutation diff ---
    --- a/example_06/hello.py
    +++ b/example_06/hello.py
    @@ -1,7 +1,7 @@
     
     
     def sayHello(name, title=None):
    -    if (title is None):
    +    if (title == None):
             title = 'Mr.'
         return ('Hello %s %s' % (title, name))
    
    total jobs: 9
    complete: 9 (100.00%)
    survival rate: 11.11%

.. note::

    Since `PR #162 <https://github.com/sixty-north/cosmic-ray/pull/162>`_
    *Cosmic-Ray* skips mutations of the kind ``== -> is`` but doesn't skip
    the opposite of ``is -> ==``!

Now compare the results after refactoring ::

    $ cosmic-ray run --test-runner nose --baseline=10 example.json hello2.py -- test_hello2.py
    $ cosmic-ray report example.json --full-report
    total jobs: 0
    no jobs completed

Functionality is the same but we have reduced the number of possible mutations!

Source code
===========


.. literalinclude:: hello.py
    :caption: hello.py
    :language: python

.. literalinclude:: test_hello.py
    :caption: test_hello.py
    :language: python

.. literalinclude:: hello2.py
    :caption: hello2.py
    :language: python

.. literalinclude:: test_hello2.py
    :caption: test_hello2.py
    :language: python
