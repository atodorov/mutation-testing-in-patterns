Testing for X != 1
******************

Reproducer
==========

::

    $ pip install nose
    $ pip install https://github.com/sixty-north/cosmic-ray/zipball/master
    $ celery -A cosmic_ray.tasks.worker worker

    $ cosmic-ray run --test-runner nose --baseline=10 example.json hello.py -- test_hello.py:TestHello
    $ cosmic-ray report example.json
    
    job ID 1:Outcome.SURVIVED:hello
    command: cosmic-ray worker hello replace_NotEq_with_Gt 0 nose -- -v test_hello.py:TestHello
    --- mutation diff ---
    --- a/example_04/hello.py
    +++ b/example_04/hello.py
    @@ -3,7 +3,7 @@
     
     def sayHello(name):
         names = myparser.parseArgs(name)
    -    if (len(names) != 1):
    +    if (len(names) > 1):
             raise Exception('You can say hello to only one person at a time!')
         return ('Hello, ' + name)
     
    job ID 3:Outcome.SURVIVED:hello
    command: cosmic-ray worker hello replace_NotEq_with_Lt 0 nose -- -v test_hello.py:TestHello
    --- mutation diff ---
    --- a/example_04/hello.py
    +++ b/example_04/hello.py
    @@ -3,7 +3,7 @@
     
     def sayHello(name):
         names = myparser.parseArgs(name)
    -    if (len(names) != 1):
    +    if (len(names) < 1):
             raise Exception('You can say hello to only one person at a time!')
         return ('Hello, ' + name)
    
    total jobs: 9
    complete: 9 (100.00%)
    survival rate: 22.22%


Now compare the results from ``TestHelloProperly`` ::

    $ cosmic-ray run --test-runner nose --baseline=10 example.json hello.py -- test_hello.py:TestHelloProperly
    $ cosmic-ray report example.json --full-report
    total jobs: 9
    complete: 9 (100.00%)
    survival rate: 0%


Source code
===========


.. literalinclude:: hello.py
    :caption: hello.py
    :language: python

.. literalinclude:: myparser.py
    :caption: myparser.py
    :language: python

.. literalinclude:: test_hello.py
    :caption: test_hello.py
    :language: python
