Missing or extra method parameters
**********************************

Reproducer
==========

::

    $ pip install nose
    $ pip install https://github.com/sixty-north/cosmic-ray/zipball/master
    $ celery -A cosmic_ray.tasks.worker worker


Initially we start with a set of tests which doesn't validate default values
for method parameters. It may validate some other behavior which was considered
more important at the time. In this example the test is empty because there is
no other behavior present. This is ``test1.py``. Mutation testing will identify
the missing tests as shown below ::


    $ cosmic-ray run --test-runner nose --baseline=10 example.json roads.py -- test1.py:
    $ cosmic-ray report example.json
    job ID 1:Outcome.SURVIVED:roads
    command: cosmic-ray worker roads number_replacer 0 nose -- -v test1.py
    --- mutation diff ---
    --- a/example_09/roads.py
    +++ b/example_09/roads.py
    @@ -2,7 +2,7 @@
     
     class UrbanRoad(object):
     
    -    def __init__(self, speedLimit=50, *args, **kwargs):
    +    def __init__(self, speedLimit=51, *args, **kwargs):
             self.speedLimit = speedLimit
     
     class RuralRoad(UrbanRoad):
    
    job ID 2:Outcome.SURVIVED:roads
    command: cosmic-ray worker roads number_replacer 1 nose -- -v test1.py
    --- mutation diff ---
    --- a/example_09/roads.py
    +++ b/example_09/roads.py
    @@ -7,7 +7,7 @@
     
     class RuralRoad(UrbanRoad):
     
    -    def __init__(self, speedLimit=90, *args, **kwargs):
    +    def __init__(self, speedLimit=91, *args, **kwargs):
             UrbanRoad.__init__(self, *args, **kwargs)
     
     class BaseMotorway(object):
    
    job ID 3:Outcome.SURVIVED:roads
    command: cosmic-ray worker roads number_replacer 2 nose -- -v test1.py
    --- mutation diff ---
    --- a/example_09/roads.py
    +++ b/example_09/roads.py
    @@ -13,7 +13,7 @@
     class BaseMotorway(object):
     
         def __init__(self, *args, **kwargs):
    -        self.minSpeed = 50
    +        self.minSpeed = 51
     
     class Motorway(BaseMotorway):
     
    
    job ID 4:Outcome.SURVIVED:roads
    command: cosmic-ray worker roads number_replacer 3 nose -- -v test1.py
    --- mutation diff ---
    --- a/example_09/roads.py
    +++ b/example_09/roads.py
    @@ -17,6 +17,6 @@
     
     class Motorway(BaseMotorway):
     
    -    def __init__(self, speedLimit=130, *args, **kwargs):
    +    def __init__(self, speedLimit=131, *args, **kwargs):
             BaseMotorway.__init__(self, speedLimit, *args, **kwargs)
     
    
    total jobs: 4
    complete: 4 (100.00%)
    survival rate: 100.00%

Then we proceed to add the missing tests in ``test2.py``. Executing this
test stand-alone identifies that something is wrong with the code under test.
The ``Motorway`` constructor passes along an extra parameter which isn't
consumed in the base class. In the ``RuralRoad`` constructor we've forgotten
to pass the ``speedLimit`` parameter to the base constructor. ::


    $ python -m nose test2.py 
    EF.
    ======================================================================
    ERROR: test_motorway (test2.TestRoadLimits)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "./example_09/test2.py", line 15, in test_motorway
        self.assertEqual(road.speedLimit, 130)
    AttributeError: 'Motorway' object has no attribute 'speedLimit'
    
    ======================================================================
    FAIL: test_rural_road (test2.TestRoadLimits)
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "./example_09/test2.py", line 11, in test_rural_road
        self.assertEqual(road.speedLimit, 90)
    AssertionError: 50 != 90
    
    ----------------------------------------------------------------------
    Ran 3 tests in 0.001s
    
    FAILED (errors=1, failures=1)

Next we proceed to refactor the code under test in ``roads2.py``

.. code-block:: diff

    --- roads.py    2016-08-26 10:59:58.342135344 +0300
    +++ roads2.py   2016-08-26 11:18:30.639663587 +0300
    @@ -4,7 +4,7 @@
     
     class RuralRoad(UrbanRoad):
         def __init__(self, speedLimit=90, *args, **kwargs):
    -        UrbanRoad.__init__(self, *args, **kwargs)
    +        UrbanRoad.__init__(self, speedLimit, *args, **kwargs)
     
     class BaseMotorway(object):
         def __init__(self, *args, **kwargs):
    @@ -12,4 +12,5 @@
     
     class Motorway(BaseMotorway):
         def __init__(self, speedLimit=130, *args, **kwargs):
    -        BaseMotorway.__init__(self, speedLimit, *args, **kwargs)
    +        BaseMotorway.__init__(self, *args, **kwargs)
    +        self.speedLimit = speedLimit


In this example the refactored file is called ``roads2.py`` and its
test is called ``test3.py``.

.. code-block:: diff

    --- test2.py    2016-08-26 11:15:17.768878361 +0300
    +++ test3.py    2016-08-26 11:19:54.241167276 +0300
    @@ -1,4 +1,4 @@
    -import roads
    +import roads2 as roads
     import unittest
     
     class TestRoadLimits(unittest.TestCase):


Finally we can verify that the test and refactored code work together and all
mutants have been killed ::

    $ python -m nose test3.py 
    ...
    ----------------------------------------------------------------------
    Ran 3 tests in 0.001s
    
    OK
    $ cosmic-ray run --test-runner nose --baseline=10 example.json roads2.py -- -v test3.py 
    $ cosmic-ray report example.json
    total jobs: 4
    complete: 4 (100.00%)
    survival rate: 0.00%

Source code
===========

.. literalinclude:: roads.py
    :caption: roads.py
    :language: python

.. literalinclude:: roads2.py
    :caption: roads2.py
    :language: python

.. literalinclude:: test1.py
    :caption: test1.py
    :language: python

.. literalinclude:: test2.py
    :caption: test2.py
    :language: python

.. literalinclude:: test3.py
    :caption: test3.py
    :language: python
