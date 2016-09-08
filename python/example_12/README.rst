Testing for 0 <= X <= 100
*************************

It is common for programs to expect numerical variables to accept values
matching a certain range. A good example is a ``percent`` variable with
allowed values from 0 to 100 inclusive.

Test for such code will often validate correct operation with
a value inside the range and expect an error for a value outside the range.
As a bonus the test may be expecting errors when testing with values on
both sides of the range!


Reproducer
==========

::

    $ pip install https://github.com/sixty-north/cosmic-ray/zipball/master
    $ celery -A cosmic_ray.tasks.worker worker

    $ cosmic-ray run --test-runner nose --baseline=10 example.json percent.py -- test1.py
    $ cosmic-ray report example.json
    
    job ID 6:Outcome.SURVIVED:percent
    command: cosmic-ray worker percent replace_Lt_with_LtE 0 nose -- -v test1.py
    --- mutation diff ---
    --- a/example_12/percent.py
    +++ b/example_12/percent.py
    @@ -1,7 +1,7 @@
     
     
     def validate_percent(percent):
    -    if ((percent < 0) or (percent > 100)):
    +    if ((percent <= 0) or (percent > 100)):
             raise Exception('Percent must be between 0 and 100')
         return percent
     
    
    job ID 15:Outcome.SURVIVED:percent
    command: cosmic-ray worker percent replace_Gt_with_GtE 0 nose -- -v test1.py
    --- mutation diff ---
    --- a/example_12/percent.py
    +++ b/example_12/percent.py
    @@ -1,7 +1,7 @@
     
     
     def validate_percent(percent):
    -    if ((percent < 0) or (percent > 100)):
    +    if ((percent < 0) or (percent >= 100)):
             raise Exception('Percent must be between 0 and 100')
         return percent
     
    
    job ID 16:Outcome.SURVIVED:percent
    command: cosmic-ray worker percent number_replacer 0 nose -- -v test1.py
    --- mutation diff ---
    --- a/example_12/percent.py
    +++ b/example_12/percent.py
    @@ -1,7 +1,7 @@
     
     
     def validate_percent(percent):
    -    if ((percent < 0) or (percent > 100)):
    +    if ((percent < 1) or (percent > 100)):
             raise Exception('Percent must be between 0 and 100')
         return percent
     
    
    job ID 17:Outcome.SURVIVED:percent
    command: cosmic-ray worker percent number_replacer 1 nose -- -v test1.py
    --- mutation diff ---
    --- a/example_12/percent.py
    +++ b/example_12/percent.py
    @@ -1,7 +1,7 @@
     
     
     def validate_percent(percent):
    -    if ((percent < 0) or (percent > 100)):
    +    if ((percent < 0) or (percent > 101)):
             raise Exception('Percent must be between 0 and 100')
         return percent
     
    
    total jobs: 20
    complete: 20 (100.00%)
    survival rate: 20.00%


To fully test this code you have to test with both border values and
with the next possible values, which are outside of the range. Testing with
a value that falls within the range, but isn't a border one doesn't affect
mutation testing. ::

    $ cosmic-ray run --test-runner nose --baseline=10 example.json percent.py -- -v test2.py
    $ cosmic-ray report example.json 
    
    total jobs: 20
    complete: 20 (100.00%)
    survival rate: 0.00%

.. note::

    This is similar to :doc:`../example_04/README`

Source code
===========

.. literalinclude:: percent.py
    :caption: percent.py
    :language: python

.. literalinclude:: test1.py
    :caption: test1.py
    :language: python

.. literalinclude:: test2.py
    :caption: test2.py
    :language: python
