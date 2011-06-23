.. include:: beamerdefs.txt

================================
PyPy training session
================================

PyPy training session
---------------------

- Part 1: Run your application under PyPy

- Part 2: Write your own interpreter with PyPy


Part 1
------

* Run your application under PyPy


How to run PyPy
----------------

* ``pypy program.py``

* That's it!

  - (modulo details)

Challenge
---------

* ``html_fibo.py``

* HTML list of fibonacci numbers

* (the most complicate ever)

* run it on CPython

* run it on PyPy

* fix it!


Refcounting vs generational GC (1)
----------------------------------

|scriptsize|
|example<| |scriptsize| ``gc0.py`` |end_scriptsize| |>|

.. sourcecode:: python

   def foo():
       f = file('/tmp/bar.txt', 'w')
       f.write('hello world')

   foo()
   print file('/tmp/bar.txt').read()

|end_example|

|pause|
|example<| |scriptsize| ``gc1.py`` |end_scriptsize| |>|

.. sourcecode:: python

   def foo():
       f = file('/tmp/bar.txt', 'w')
       f.write('hello world')
       f.close() # <-------

|end_example|

|pause|
|example<| |scriptsize| ``gc2.py`` |end_scriptsize| |>|

.. sourcecode:: python

   def foo():
       with file('/tmp/bar.txt', 'w') as f:
           f.write('hello world')

|end_example|
|end_scriptsize|


Refcounting vs generational GC (2)
----------------------------------

* ``__del__``

  - especially files or sockets

  - don't leak file descriptors!

* weakrefs

* ``finally`` inside generators



How the JIT works
-----------------------

XXX write me


PYPYLOG
--------

|small|

* ``PYPYLOG=categories:logfile pypy program.py``

|end_small|

* categories:

  - gc-minor, gc-major

  - jit-log-noopt, jit-log-opt

  - jit-backend

  - jit-backend-counts


Inspecting the JIT log
-----------------------

|scriptsize|
|example<| |scriptsize| ``count.py`` |end_scriptsize| |>|

.. sourcecode:: python

    def count_mult_of_5(N):
        mult = 0
        not_mult = 0
        for i in range(N):
            if i % 5 == 0:
                mult += 1
            else:
                not_mult += 1
        return mult, not_mult

|end_example|
|end_scriptsize|

|small|

* ``PYPYLOG=jit-log-opt:mylog pypy count.py 2000``

* ``PYPYLOG=jit-log-opt:mylog pypy count.py 10000``

|end_small|


The jitviewer
-------------

|scriptsize|

* ``PYPYLOG=jit-log-opt,jit-backend-counts:mylog pypy count.py 2000``

* ``PYPYLOG=jit-log-opt,jit-backend-counts:mylog pypy count.py 10000``

* ``jitviewer.py log.pypylog``

* Look at the (missing) bridge!

|end_scriptsize|
