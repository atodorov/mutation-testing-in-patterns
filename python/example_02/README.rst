Mutant killed due to flaky test
*******************************

Sometimes mutants may be falsely reported as killed simply because the
test case failed. When your test suite isn't reliable your mutation testing
isn't realiable as well.

Reproducer
==========

::

    $ pip install nose
    $ pip install https://github.com/sixty-north/cosmic-ray/zipball/master

    $ cosmic-ray run --test-runner nose --baseline=10 example.json flaky.py -- test_flaky.py:TestFlaky
    $ cosmic-ray report example.json 
    job ID 1:Outcome.KILLED:flaky
    command: cosmic-ray worker flaky boolean_replacer 0 unittest -- .
    
    job ID 2:Outcome.KILLED:flaky
    command: cosmic-ray worker flaky number_replacer 0 unittest -- .
    
    total jobs: 2
    complete: 2 (100.00%)
    survival rate: 0.00%

    $ cat test.txt 
    Hello World
    Hello World
    HELLO WORLD
    HELLO WORLD
    Hello World
    Hello World
    Hello World

Verify mutants have survived
============================

The ``TestFlaky`` test isn't reliable because it doesn't take into account
the interaction with the filesystem.
In the example above the first 2 lines appear when *Cosmic-Ray* executes
the baseline test suite, that is execute the test suite without any modifications.
The next 2 lines come when ``upcase`` is mutated to ``True`` and the last 3
lines come when ``number`` is mutated to ``3``.

Notice that ``TestFlaky`` never asserts the contents of the written text,
nor the fact that it may be in upper case. However due to unrelated failures
we're left to think that the test suite tests everything correctly. To see the
real results execute ::

    $ rm test.txt
    $ cosmic-ray worker flaky boolean_replacer 0 nose -- test_flaky.py:TestFlaky
    Outcome.SURVIVED
    --- mutation diff ---
    --- a/example_02/flaky.py
    +++ b/example_02/flaky.py
    @@ -5,7 +5,7 @@
         data_file.write(content)
         data_file.close()
    
    -def sayHello(times=2, upcase=False):
    +def sayHello(times=2, upcase=True):
         text = 'Hello World\\n'
         if upcase:
             text = text.upper()

    $ rm test.txt
    $ cosmic-ray worker flaky number_replacer 0 nose -- test_flaky.py:TestFlaky
    Outcome.KILLED
    Traceback (most recent call last):
      File "./example_02/test_flaky.py", line 10, in test_sayHello
        self.assertEqual(len(lines), 2)
        AssertionError: 3 != 2

    --- mutation diff ---
    --- a/example_02/flaky.py
    +++ b/example_02/flaky.py
    @@ -5,7 +5,7 @@
         data_file.write(content)
         data_file.close()
    
    -def sayHello(times=2, upcase=False):
    +def sayHello(times=3, upcase=False):
         text = 'Hello World\\n'
         if upcase:
             text = text.upper()


The second test ``TestFlakyWithMock`` is better because it properly isolates
interaction with the filesystem and because
it properly verifies the expected behavior. All mutants are properly killed
this time ::

    $ cosmic-ray run --test-runner nose --baseline=10 example.json flaky.py -- test_flaky.py:TestFlakyWithMock
    $ cosmic-ray report example.json --full-report
    $ ls -l test.txt
    ls: cannot access test.txt: No such file or directory

.. note::

    Since commit `db7b7c6` Cosmic Ray will fail if baseline test execution fails.
    This isn't the same as having unreliable tests but may help you identify
    something isn't right sooner than later. If you want to experiment execute the
    above `cosmic-ray run` command twice without deleting `test.txt` between test runs!


Source code
===========


.. literalinclude:: flaky.py
    :caption: flaky.py
    :language: python

.. literalinclude:: test_flaky.py
    :caption: test_flaky.py
    :language: python
