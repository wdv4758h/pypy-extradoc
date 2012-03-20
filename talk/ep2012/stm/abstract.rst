
PyPy: status and GIL-less future
================================

In the first part of the talk we will present the current status and
speed of PyPy, the Python interpreter written in Python.

The second part of the talk is about one particular feature whose
development is in progress in PyPy: Automatic Mutual Exclusion.
What it is needs some explanation:

  The GIL, or Global Interpreter Lock, is a well-known issue for Python
  programmers that want to have a single program using the multiple
  cores of today's machines.

  This talk is *not* about writing a GIL-less Python interpreter;
  although hard, this has been done before, notably in Jython.  The real
  issue is that writing each and every multi-threaded Python programs is
  hard too.  The ``threading`` module offers locks in several variants,
  conditions, events, semaphores...  But using them correctly without
  missing one case is difficult, impossible to seriously test, often
  impossible to retrofit into existing programs, and arguably doesn't
  scale.  (Other solutions like the ``multiprocessing`` module are at
  best workarounds, suffering some of the same issues plus their own
  ones.)

  Instead, this talk is about an alternate solution: a minimal
  thread-less API that lets programs use multiple cores, without
  worrying about races.  This may sound impossible, but is in fact
  similar to the API simplification of using a garbage collected
  language over an explicitly managed one --- what is not minimal is
  "just" the internal implementation of that API.  I will explain how it
  can actually be done using Automatic Mutual Exclusion, a technique
  based on Transactional Memory.  I will give preliminary results on a
  modified version of the PyPy Python interpreter that show that it can
  actually work.  I will also explain how the API is used, e.g. in a
  modified Twisted reactor that gives multi-core capability to any
  existing, non-thread-based Twisted program.
