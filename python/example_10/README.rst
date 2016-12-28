Testing and refactoring boolean expressions
*******************************************

When dealing with non-trivial boolean expressions mutation testing often helps
put things into perspective. It causes you to rethink the expression which often
leads to refactoring and killing mutants.

Example
=======

::

    $ pip install nose
    $ pip install https://github.com/sixty-north/cosmic-ray/zipball/master

Initially we start with the example in ``boolops1.py`` and ``test1.py``.
Although the test appears to be correct, all possible values for ``list_a`` and
``list_b`` are tested, there are still surviving mutants. ::

    $ cosmic-ray run --test-runner nose --baseline=10 example.json boolops1.py -- test1.py:
    $ cosmic-ray report example.json
    
    job ID 5:Outcome.SURVIVED:boolops
    command: cosmic-ray worker boolops replace_Eq_with_LtE 0 nose -- -v test1.py
    --- mutation diff ---
    --- a/example_10/boolops1.py
    +++ b/example_10/boolops1.py
    @@ -1,6 +1,6 @@
     
     
     def xnor_raise(list_a, list_b):
    -    if (((len(list_a) == 0) and (len(list_b) == 0)) or ((len(list_a) > 0) and (len(list_b) > 0))):
    +    if (((len(list_a) <= 0) and (len(list_b) == 0)) or ((len(list_a) > 0) and (len(list_b) > 0))):
             raise Exception('TEST')
     
    
    job ID 6:Outcome.SURVIVED:boolops
    command: cosmic-ray worker boolops replace_Eq_with_LtE 1 nose -- -v test1.py
    --- mutation diff ---
    --- a/example_10/boolops1.py
    +++ b/example_10/boolops1.py
    @@ -1,6 +1,6 @@
     
     
     def xnor_raise(list_a, list_b):
    -    if (((len(list_a) == 0) and (len(list_b) == 0)) or ((len(list_a) > 0) and (len(list_b) > 0))):
    +    if (((len(list_a) == 0) and (len(list_b) <= 0)) or ((len(list_a) > 0) and (len(list_b) > 0))):
             raise Exception('TEST')
     
    
    job ID 13:Outcome.SURVIVED:boolops
    command: cosmic-ray worker boolops replace_Gt_with_NotEq 0 nose -- -v test1.py
    --- mutation diff ---
    --- a/example_10/boolops1.py
    +++ b/example_10/boolops1.py
    @@ -1,6 +1,6 @@
     
     
     def xnor_raise(list_a, list_b):
    -    if (((len(list_a) == 0) and (len(list_b) == 0)) or ((len(list_a) > 0) and (len(list_b) > 0))):
    +    if (((len(list_a) == 0) and (len(list_b) == 0)) or ((len(list_a) != 0) and (len(list_b) > 0))):
             raise Exception('TEST')
     
    
    job ID 14:Outcome.SURVIVED:boolops
    command: cosmic-ray worker boolops replace_Gt_with_NotEq 1 nose -- -v test1.py
    --- mutation diff ---
    --- a/example_10/boolops1.py
    +++ b/example_10/boolops1.py
    @@ -1,6 +1,6 @@
     
     
     def xnor_raise(list_a, list_b):
    -    if (((len(list_a) == 0) and (len(list_b) == 0)) or ((len(list_a) > 0) and (len(list_b) > 0))):
    +    if (((len(list_a) == 0) and (len(list_b) == 0)) or ((len(list_a) > 0) and (len(list_b) != 0))):
             raise Exception('TEST')
     
    
    job ID 23:Outcome.SURVIVED:boolops
    command: cosmic-ray worker boolops replace_Gt_with_IsNot 0 nose -- -v test1.py
    --- mutation diff ---
    --- a/example_10/boolops1.py
    +++ b/example_10/boolops1.py
    @@ -1,6 +1,6 @@
     
     
     def xnor_raise(list_a, list_b):
    -    if (((len(list_a) == 0) and (len(list_b) == 0)) or ((len(list_a) > 0) and (len(list_b) > 0))):
    +    if (((len(list_a) == 0) and (len(list_b) == 0)) or ((len(list_a) is not 0) and (len(list_b) > 0))):
             raise Exception('TEST')
     
    
    job ID 24:Outcome.SURVIVED:boolops
    command: cosmic-ray worker boolops replace_Gt_with_IsNot 1 nose -- -v test1.py
    --- mutation diff ---
    --- a/example_10/boolops1.py
    +++ b/example_10/boolops1.py
    @@ -1,6 +1,6 @@
     
     
     def xnor_raise(list_a, list_b):
    -    if (((len(list_a) == 0) and (len(list_b) == 0)) or ((len(list_a) > 0) and (len(list_b) > 0))):
    +    if (((len(list_a) == 0) and (len(list_b) == 0)) or ((len(list_a) > 0) and (len(list_b) is not 0))):
             raise Exception('TEST')
     
    
    total jobs: 38
    complete: 38 (100.00%)
    survival rate: 15.79%


If we proceed to refactor ``len(list)`` comparisons as shown previously it
is easier to figure out that the boolean function is XNOR (if and only if),
also called logical equality. In ``boolops2.py`` *Cosmic-Ray* doesn't
detect any possible mutations because at the moment of writing it doesn't
support mutating boolean operators. ::

    $ cosmic-ray run --test-runner nose --baseline=10 example.json boolops2.py -- test2.py:
    $ cosmic-ray report example.json
    total jobs: 0
    no jobs completed


Another possible refactoring is ``boolops3.py`` where valid parameters are
enumerated before the condition is checked. ::

    $ cosmic-ray run --test-runner nose --baseline=10 example.json boolops3.py -- test3.py:
    $ cosmic-ray report example.json
    total jobs: 12
    complete: 12 (100.00%)
    survival rate: 0.00%

Yet another possible refactoring is ``boolops4.py`` where the condition is
expressed using the built-ins ``any`` and ``all``. Unfortunately *Cosmic-Ray*
doesn't recognize these as possible mutations either. ::

    $ cosmic-ray run --test-runner nose --baseline=10 example.json boolops4.py -- test4.py:
    $ cosmic-ray report example.json
    total jobs: 0
    no jobs completed



Source code
===========

.. literalinclude:: boolops1.py
    :caption: boolops1.py
    :language: python

.. literalinclude:: test1.py
    :caption: test1.py
    :language: python

.. literalinclude:: boolops2.py
    :caption: boolops2.py
    :language: python

.. literalinclude:: test2.py
    :caption: test2.py
    :language: python

.. literalinclude:: boolops3.py
    :caption: boolops3.py
    :language: python

.. literalinclude:: test3.py
    :caption: test3.py
    :language: python

.. literalinclude:: boolops4.py
    :caption: boolops4.py
    :language: python

.. literalinclude:: test4.py
    :caption: test4.py
    :language: python
