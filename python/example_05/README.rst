Refactor if len(list) != 0
**************************

Reproducer
==========

::

    $ pip install nose
    $ pip install https://github.com/sixty-north/cosmic-ray/zipball/master

    $ cosmic-ray run --test-runner nose --baseline=10 example.json hello.py -- test_hello.py
    $ cosmic-ray report example.json
    
    job ID 7:Outcome.SURVIVED:hello
    command: cosmic-ray worker hello replace_NotEq_with_Gt 0 nose -- -v test_hello.py
    --- mutation diff ---
    --- a/example_05/hello.py
    +++ b/example_05/hello.py
    @@ -1,7 +1,7 @@
     
     
     def sayHello(name, friends):
    -    if (len(friends) != 0):
    +    if (len(friends) > 0):
             raise Exception("You can't say hello to other people's friends!")
         return ('Hello, ' + name)
     
    total jobs: 9
    complete: 9 (100.00%)
    survival rate: 11.11%

.. note::

    If we didn't have the ``test_sayHello_with_friends()`` test then the
    ``!= -> <`` mutation would have survived as well!

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
