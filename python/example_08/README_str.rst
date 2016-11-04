Testing sequence of if == string statements
*******************************************

Sometimes in programs we see the following pattern

.. code-block:: python

    if X == "string_1":
        pass
    elif X == "string_2":
        pass
    elif X == "string_3":
        pass

``X`` is compared to several allowed values of type string.
It is important to notice that ``X`` accepts a descrete set of
allowed values. When we forget to test with string values outside the allowed set
mutation testing will produce surviving mutants.

.. note::

    The order of if statements isn't important.


Reproducer
==========

::

    $ pip install nose
    $ pip install https://github.com/sixty-north/cosmic-ray/zipball/master
    $ celery -A cosmic_ray.tasks.worker worker

    $ cosmic-ray run --test-runner nose --baseline=10 example.json selinux_str.py -- tests_str.py:Test_mode_from_str
    $ cosmic-ray report example.json
    
    job ID 4:Outcome.SURVIVED:selinux_str
    command: cosmic-ray worker selinux_str mutate_comparison_operator 2 nose -- tests_str.py:Test_mode_from_str
    --- mutation diff ---
    --- a/example_08/selinux_str.py
    +++ b/example_08/selinux_str.py
    @@ -3,7 +3,7 @@
     
     def mode_from_str(str_mode):
         retval = None
    -    if (str_mode == 'disabled'):
    +    if (str_mode <= 'disabled'):
             retval = modes.SELINUX_DISABLED
         elif (str_mode == 'enforcing'):
             retval = modes.SELINUX_ENFORCING
    
    job ID 8:Outcome.SURVIVED:selinux_str
    command: cosmic-ray worker selinux_str mutate_comparison_operator 6 nose -- tests_str.py:Test_mode_from_str
    --- mutation diff ---
    --- a/example_08/selinux_str.py
    +++ b/example_08/selinux_str.py
    @@ -3,7 +3,7 @@
     
     def mode_from_str(str_mode):
         retval = None
    -    if (str_mode == 'disabled'):
    +    if (str_mode in 'disabled'):
             retval = modes.SELINUX_DISABLED
         elif (str_mode == 'enforcing'):
             retval = modes.SELINUX_ENFORCING
    
    job ID 12:Outcome.SURVIVED:selinux_str
    command: cosmic-ray worker selinux_str mutate_comparison_operator 10 nose -- tests_str.py:Test_mode_from_str
    --- mutation diff ---
    --- a/example_08/selinux_str.py
    +++ b/example_08/selinux_str.py
    @@ -5,7 +5,7 @@
         retval = None
         if (str_mode == 'disabled'):
             retval = modes.SELINUX_DISABLED
    -    elif (str_mode == 'enforcing'):
    +    elif (str_mode <= 'enforcing'):
             retval = modes.SELINUX_ENFORCING
         elif (str_mode == 'permissive'):
             retval = modes.SELINUX_PERMISSIVE

    job ID 16:Outcome.SURVIVED:selinux_str
    command: cosmic-ray worker selinux_str mutate_comparison_operator 14 nose -- tests_str.py:Test_mode_from_str
    --- mutation diff ---
    --- a/example_08/selinux_str.py
    +++ b/example_08/selinux_str.py
    @@ -5,7 +5,7 @@
         retval = None
         if (str_mode == 'disabled'):
             retval = modes.SELINUX_DISABLED
    -    elif (str_mode == 'enforcing'):
    +    elif (str_mode in 'enforcing'):
             retval = modes.SELINUX_ENFORCING
         elif (str_mode == 'permissive'):
             retval = modes.SELINUX_PERMISSIVE
    
    job ID 20:Outcome.SURVIVED:selinux_str
    command: cosmic-ray worker selinux_str mutate_comparison_operator 18 nose -- tests_str.py:Test_mode_from_str
    --- mutation diff ---
    --- a/example_08/selinux_str.py
    +++ b/example_08/selinux_str.py
    @@ -7,7 +7,7 @@
             retval = modes.SELINUX_DISABLED
         elif (str_mode == 'enforcing'):
             retval = modes.SELINUX_ENFORCING
    -    elif (str_mode == 'permissive'):
    +    elif (str_mode <= 'permissive'):
             retval = modes.SELINUX_PERMISSIVE
         return retval
     
    
    job ID 22:Outcome.SURVIVED:selinux_str
    command: cosmic-ray worker selinux_str mutate_comparison_operator 20 nose -- tests_str.py:Test_mode_from_str
    --- mutation diff ---
    --- a/example_08/selinux_str.py
    +++ b/example_08/selinux_str.py
    @@ -7,7 +7,7 @@
             retval = modes.SELINUX_DISABLED
         elif (str_mode == 'enforcing'):
             retval = modes.SELINUX_ENFORCING
    -    elif (str_mode == 'permissive'):
    +    elif (str_mode >= 'permissive'):
             retval = modes.SELINUX_PERMISSIVE
         return retval
     
    
    job ID 24:Outcome.SURVIVED:selinux_str
    command: cosmic-ray worker selinux_str mutate_comparison_operator 22 nose -- tests_str.py:Test_mode_from_str
    --- mutation diff ---
    --- a/example_08/selinux_str.py
    +++ b/example_08/selinux_str.py
    @@ -7,7 +7,7 @@
             retval = modes.SELINUX_DISABLED
         elif (str_mode == 'enforcing'):
             retval = modes.SELINUX_ENFORCING
    -    elif (str_mode == 'permissive'):
    +    elif (str_mode in 'permissive'):
             retval = modes.SELINUX_PERMISSIVE
         return retval
     
    
    total jobs: 25
    complete: 25 (100.00%)
    survival rate: 28.00%


Killing the mutants
===================


To kill some mutants we need to test with values outside the allowed set ::

    $ cosmic-ray run --test-runner nose --baseline=10 example.json selinux_str.py -- tests_str.py:TestCompletely
    $ cosmic-ray report example.json

Remaining mutants
=================

When testing string comparisons the ==/in mutations are equivalent and can not be killed:

::

    -    elif (str_mode == 'permissive'):
    +    elif (str_mode in 'permissive'):


Source code
===========


.. literalinclude:: modes.py
    :caption: modes.py
    :language: python

.. literalinclude:: selinux_str.py
    :caption: selinux_str.py
    :language: python

.. literalinclude:: tests_str.py
    :caption: tests_str.py
    :language: python
