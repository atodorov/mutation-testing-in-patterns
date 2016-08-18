Killing mutants by refactoring if str != ""
*******************************************

Reproducer
==========

::

    $ pip install nose
    $ pip install https://github.com/sixty-north/cosmic-ray/zipball/master
    $ celery -A cosmic_ray.tasks.worker worker

    $ cosmic-ray run --test-runner nose --baseline=10 example.json hello.py -- test_hello.py 
    $ cosmic-ray report example.json
    
    job ID 3:Outcome.SURVIVED:hello
    command: cosmic-ray worker hello replace_NotEq_with_NotIn 0 nose -- test_hello.py
    --- mutation diff ---
    --- a/example_03/hello.py
    +++ b/example_03/hello.py
    @@ -1,7 +1,7 @@
     
     
     def sayHello(name, greeting=''):
    -    if (greeting != ''):
    +    if (greeting not in ''):
             return ((greeting + ', ') + name)
         else:
             return ('Hello, ' + name)
    
    job ID 8:Outcome.SURVIVED:hello
    command: cosmic-ray worker hello replace_NotEq_with_Gt 0 nose -- test_hello.py
    --- mutation diff ---
    --- a/example_03/hello.py
    +++ b/example_03/hello.py
    @@ -1,7 +1,7 @@
     
     
     def sayHello(name, greeting=''):
    -    if (greeting != ''):
    +    if (greeting > ''):
             return ((greeting + ', ') + name)
         else:
             return ('Hello, ' + name)
    
    total jobs: 8
    complete: 8 (100.00%)
    survival rate: 25.00%


Now compare the results with ``hello2.py`` and ``test_hello2.py`` where we've
refactored the condition to ``if greeting:``::

    $ cosmic-ray run --test-runner nose --baseline=10 example.json hello2.py -- test_hello2.py
    $ cosmic-ray report example.json
    total jobs: 0
    no jobs completed


Source code
===========


.. literalinclude:: hello.py
    :caption: hello.py
    :language: python

.. literalinclude:: hello2.py
    :caption: hello2.py
    :language: python

.. literalinclude:: test_hello.py
    :caption: test_hello.py
    :language: python

.. literalinclude:: test_hello2.py
    :caption: test_hello2.py
    :language: python
