
Software Transactional Memory lisp experiments
==============================================

As covered in `the previous blog post`_, the STM subproject of PyPy has been
back on the drawing board and the result of this experiment is an STM-aware
garbage collector written in C. This is finished by now, thanks to Armin
and Remi_M work, we have a fully functional garbage collector and STM subsystem
that can be used from any C program with enough effort. Using it is more than
a little mundane, since you have to inserts write and read barriers by hand
everywhere in your code that reads or writes to garbage collector controlled
memory. Once we finish PyPy integration, those sort of things would be inserted
automatically by STM transformation in the interpreter.

However, to experiment some more, we created a `lisp interpreter`_
(called duhton), that follows closely CPython's implementation strategy
and for anyone familiar with CPython's source code, it should be pretty
readable. This interpreter works like a normal and very basic lisp variant,
however it comes with ``(transaction`` builtin, that lets you spawn transactions
using STM system. We implemented a few demos that let you play with the
transaction system. All the demos are running without conflicts, which means
there is no conflicting writes to global memory and hence are amenable to
parallelization very well. They exercise:

* arithmetics - ``demo/many_sqare_roots.duh``

* read-only access to globals - ``demo/trees.duh``

* read-write access to local objects - ``demo/trees2.duh``

With the latter ones being very similar to the classic gcbench. STM-aware
duhton can be found in `the stmgc repo`_, while the STM-less duhton,
that uses refcounting, can be found in `the duhton repo`_ under the ``base``
branch.
