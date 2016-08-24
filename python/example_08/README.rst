Testing sequence of if == int statements
****************************************

Sometimes in programs we see the following pattern

.. code-block:: python

    if X == int_1:
        pass
    elif X == int_2:
        pass
    elif X == int_3:
        pass

``X`` is compared to several allowed values of type integer.
It is important to notice that ``X`` accepts a descrete set of
allowed values. When we forget to test with values outside the allowed set
mutation testing will produce surviving mutants.

.. note::

    The order of if statements isn't important.


Reproducer
==========

::

    $ pip install nose
    $ pip install https://github.com/sixty-north/cosmic-ray/zipball/master
    $ celery -A cosmic_ray.tasks.worker worker

    $ cosmic-ray run --test-runner nose --baseline=10 example.json selinux.py -- tests.py:Test_mode_from_int
    $ cosmic-ray report example.json
    
    job ID 3:Outcome.SURVIVED:selinux
    command: cosmic-ray worker selinux replace_Eq_with_GtE 2 nose -- -v tests.py:Test_mode_from_int
    --- mutation diff ---
    --- a/example_08/selinux.py
    +++ b/example_08/selinux.py
    @@ -7,7 +7,7 @@
             retval += 'disabled'
         elif (int_mode == modes.SELINUX_ENFORCING):
             retval += 'enforcing'
    -    elif (int_mode == modes.SELINUX_PERMISSIVE):
    +    elif (int_mode >= modes.SELINUX_PERMISSIVE):
             retval += 'permissive'
         return retval
     
    job ID 16:Outcome.SURVIVED:selinux
    command: cosmic-ray worker selinux replace_Eq_with_LtE 0 nose -- -v tests.py:Test_mode_from_int
    --- mutation diff ---
    --- a/example_08/selinux.py
    +++ b/example_08/selinux.py
    @@ -3,7 +3,7 @@
     
     def mode_from_int(int_mode):
         retval = ''
    -    if (int_mode == modes.SELINUX_DISABLED):
    +    if (int_mode <= modes.SELINUX_DISABLED):
             retval += 'disabled'
         elif (int_mode == modes.SELINUX_ENFORCING):
             retval += 'enforcing'
    
    job ID 17:Outcome.SURVIVED:selinux
    command: cosmic-ray worker selinux replace_Eq_with_LtE 1 nose -- -v tests.py:Test_mode_from_int
    --- mutation diff ---
    --- a/example_08/selinux.py
    +++ b/example_08/selinux.py
    @@ -5,7 +5,7 @@
         retval = ''
         if (int_mode == modes.SELINUX_DISABLED):
             retval += 'disabled'
    -    elif (int_mode == modes.SELINUX_ENFORCING):
    +    elif (int_mode <= modes.SELINUX_ENFORCING):
             retval += 'enforcing'
         elif (int_mode == modes.SELINUX_PERMISSIVE):
             retval += 'permissive'
    
    job ID 18:Outcome.SURVIVED:selinux
    command: cosmic-ray worker selinux replace_Eq_with_LtE 2 nose -- -v tests.py:Test_mode_from_int
    --- mutation diff ---
    --- a/example_08/selinux.py
    +++ b/example_08/selinux.py
    @@ -7,7 +7,7 @@
             retval += 'disabled'
         elif (int_mode == modes.SELINUX_ENFORCING):
             retval += 'enforcing'
    -    elif (int_mode == modes.SELINUX_PERMISSIVE):
    +    elif (int_mode <= modes.SELINUX_PERMISSIVE):
             retval += 'permissive'
         return retval
     
    total jobs: 24
    complete: 24 (100.00%)
    survival rate: 16.67%


Killing the mutants
===================


To kill all mutants we need to test with values outside the allowed set ::

    $ cosmic-ray run --test-runner nose --baseline=10 example.json selinux.py -- tests.py:TestCompletely
    $ cosmic-ray report example.json


Source code
===========


.. literalinclude:: selinux.py
    :caption: selinux.py
    :language: python

.. literalinclude:: modes.py
    :caption: modes.py
    :language: python

.. literalinclude:: tests.py
    :caption: tests.py
    :language: python
