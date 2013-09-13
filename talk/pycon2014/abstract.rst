Software Transactional Memory with PyPy
=======================================

Description
-----------

PyPy is a fast alternative Python implementation.  Software
Transactional Memory is a current academic research topic.  Put the two
together --brew for a couple of years-- and we obtain a version of PyPy
that runs on multiple cores, without the infamous Global Interpreter
Lock (GIL).  It has been released in 2013 in beta, including
integration with the Just-in-Time compiler.


Audience
--------

People interested in PyPy; people looking for concurrency solutions.


Objectives
----------

Attendees will learn about a way to use multiple cores in their
applications, and how it differs from other solutions like the
'multiprocessing' package.


Detailed abstract
-----------------

'pypy-stm' is a special version of PyPy that runs on multiple cores
without the infamous Global Interpreter Lock (GIL).  It means that it
can run a single Python program using multiple cores, rather than being
limited to one core, as it is the case for CPU-intensive programs on
CPython (or regular PyPy).

But the point is not only that: this approach can also give the
programmer the illusion of single-threaded programming, even when he
really wants the program to use multiple cores.  This naturally avoids a
whole class of bugs.  I will give examples of what exactly I mean by
that.  Starting from the usual multithreaded demos --with explicit
threads-- I will move to other examples where the actual threads are
hidden to the programmer.  I will explain how the core of async
libraries (Twisted, Tornado, gevent, ...) can be/have been modified to
use multiples threads, without exposing any concurrency issues to the
user of the library --- existing Twisted/etc. programs still run
correctly without change.  (They may need a few small changes to enable
parallelism.)

Depending on the status of pypy-stm at the time of the presentation, I
will give demos of this, explaining in detail what people can expect to
have to change (very little), and how it performs on real applications.

I will then give a comparison with the alternative approaches:
independent processes; the stdlib 'multiprocessing' package; or custom
solutions.

I will also give an overview of how things work under the cover: the
10000-feet view is to internally create copies of objects and write
changes into these copies.  This allows the originals to continue being
used by other threads.  It is an adaptation of previous work on
Software Transactional Memory (STM), notably RSTM.


Outline
-------

1. Intro (5 min): PyPy, STM

2. Examples and demos (10 min): simple multithreading; multithreading
   with atomic sections; Twisted/etc. model; performance numbers.

3. Comparison (5 min): independent processes; multiprocessing; custom
   solutions.

4. How things work under the cover (5 min): overview.

5. Questions (5 min).


Additional notes
----------------

* Follow the progress of STM in PyPy:
  http://morepypy.blogspot.ch/search/label/stm
