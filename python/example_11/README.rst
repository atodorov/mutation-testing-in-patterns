Refactor if X is not None
*************************

Objects of any type can be compared for not being ``None`` value however that
leads to surviving mutations. ``None`` is a special value but in most practical
cases it is equivalent to zero/empty value for the type.


Example
=======

::

    $ pip install nose
    $ pip install https://github.com/sixty-north/cosmic-ray/zipball/master
    $ celery -A cosmic_ray.tasks.worker worker

In ``example1.py`` we're accepting ``None`` as default parameter value and
correctly identified 3 test cases - when password is a string, when it is
empty string and when it is ``None``. There is one surviving mutant. ::

    $ cosmic-ray run --test-runner nose --baseline=10 example.json example1.py -- test1.py:
    $ cosmic-ray report example.json
    
    job ID 5:Outcome.SURVIVED:example1
    command: cosmic-ray worker example1 replace_IsNot_with_NotEq 0 nose -- -v test1.py
    --- mutation diff ---
    --- a/example_11/example1.py
    +++ b/example_11/example1.py
    @@ -1,7 +1,7 @@
     
     
     def reverse_password(password=None):
    -    if (password is not None):
    +    if (password != None):
             return password[::(- 1)]
         else:
             return ''
    
    total jobs: 11
    complete: 11 (100.00%)
    survival rate: 9.09%


If we decide to remove ``None`` and accept an empty string instead then
``example2.py`` is reduced to one line and there are no surviving
mutations. Also the number of mutations is significantly reduced. ::

    $ cosmic-ray run --test-runner nose --baseline=10 example.json example2.py -- -v test2.py 
    $ cosmic-ray report example.json 
    job ID 1:Outcome.KILLED:example2
    command: cosmic-ray worker example2 number_replacer 0 nose -- -v test2.py
    
    job ID 2:Outcome.KILLED:example2
    command: cosmic-ray worker example2 arithmetic_operator_deletion 0 nose -- -v test2.py
    
    total jobs: 2
    complete: 2 (100.00%)
    survival rate: 0.00%

Source code
===========

.. literalinclude:: example1.py
    :caption: example1.py
    :language: python

.. literalinclude:: test1.py
    :caption: test1.py
    :language: python

.. literalinclude:: example2.py
    :caption: example2.py
    :language: python

.. literalinclude:: test2.py
    :caption: test2.py
    :language: python
