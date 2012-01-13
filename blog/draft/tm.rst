Transactional Memory
====================

Here is an update about the `previous blog post`__ about the
Global Interpreter Lock (GIL).

.. __: http://morepypy.blogspot.com/p/global-interpreter-lock-or-how-to-kill.html

Let me remind you that the GIL is the technique used in both CPython and
PyPy to safely run multi-threaded programs: it is a global lock that
prevents multiple threads from actually running at the same time.  The
reason to do that is that it would have desastrous effects in the
interpreter if both threads access the same object concurrently --- to
the point that in CPython even just manipulating the object's reference
counter needs to be protected by the lock.

So far, the ultimate goal to enable true multi-CPU usage has been to remove
the infamous GIL from the interpreter, so that multiple threads could actually
run in parallel.  But we think we have a plan to implement a
different model for using multiple cores.  Believe it or not, this is
*better* than just removing the GIL from PyPy.  You might get to use all
your cores *without ever writing threads.*

You would instead just use some event dispatcher, say from Twisted, from
Stackless, or from your favorite GUI; or just write your own.  From
there, you (or someone else) would add some minimal extra code to the
event dispatcher's source code, to exploit the new transactional features
offered by PyPy.  Then you would run your program on a
special version of PyPy, and get some form of automatic parallelization.
Sounds magic, but the basic idea is simple: start handling multiple
events in parallel, giving each one its own *transaction.*  More about
it later.

Threads or Events?
------------------

First, why would this be better than "just" removing the GIL?  Because
using threads can be a mess in any complex program.  Some authors (e.g.
Lee_) have argued that the reason is that threads are fundamentally
non-deterministic.  This makes it very hard to reason about them.
Basically the programmer needs to "trim" down the non-determinism (e.g.
by adding locks, semaphores, etc.), and it's hard to be sure when he's
got a sufficiently deterministic result, if only because he can't write
exhaustive tests for it.

.. _Lee: http://www.eecs.berkeley.edu/Pubs/TechRpts/2006/EECS-2006-1.pdf

By contrast, consider a Twisted program.  It's not a multi-threaded
program, which means that it handles the "events" one after the other.
The exact ordering of the events is not really deterministic, because
they often correspond to external events; but that's the only source of
non-determinism.  The actual handling of each event occurs in a nicely
deterministic way, and most importantly, not in parallel with the
handling of other events.  The same is true about other libraries like
GUI toolkits, gevent, or Stackless.

(Of course the Twisted and the Stackless models, to cite only these two,
are quite different from each other; but they have in common the fact
that they are not multi-threaded, and based instead on "events" ---
which in the Stackless case means running a tasklet from one switch()
point to the next one.)

These two models --- threads or events --- are the two main models we
have right now.  The latter is more used in Python, because it is much
simpler to use than the former, and the former doesn't give any benefit
because of the GIL.  A third model, which is the only one that gives
multi-core benefits, is to use multiple processes, and do inter-process
communication.

The problem
-----------

Consider the case of a big program that has arbitrary complicated
dependencies.  Even assuming a GIL-less Python, this is likely enough to
prevent the programmer from even starting a multi-threaded rewrite,
because it would require a huge mess of locks.  He could also consider
using multiple processes instead, but the result is annoying as well:
the complicated dependencies translate into a huge mess of inter-process
synchronization.

The problem can also be down-sized to very small programs, like the kind
of hacks that you do and forget about.  In this case, the dependencies
might be simpler, but you still have to learn and use subtle locking
patterns or a complex inter-process library, which is overkill for the
purpose.  I would even argue that this is similar to how we might feel a
priori that automatic memory management is unnecessary in small programs
--- but of course anyone who wrote a number of 15-line Python scripts
knows this to be wrong.  This is even *so* wrong that the opposite is
obvious nowadays: it makes no sense whatsoever to manage object
lifetimes explicitly in most small scripts.  A garbage collector is not
overkill; it is part of the basics that you expect.

(I think the same will eventually be true for using multiple CPUs, but
the correct solution will take time to mature, like garbage collectors
did.  This post is a step in hopefully the right direction ``:-)``)

Events in Transactions
----------------------

Let me introduce the notion of *independent events*: two events are
independent if they don't touch the same set of objects. In a multi-threaded
world, it means that they can be executed in parallel without needing any lock
to ensure correctness.

Events might also be *mostly independent*, i.e. they rarely access the same
object concurrently.  Of course, in a multi-threaded world we would still need
a lock to ensure correctness, but the point is that without the lock the
program would run correctly "most of the time".

Consider again the Twisted example I gave above.  There are often several
events pending in the dispatch queue (assuming the program is using 100%
of our single usable CPU, otherwise the whole discussion is moot).  The case I am
interested in is the case in which these events are *generally mostly
independent*, i.e. we expect few conflicts between them.  However
they don't *have* to be proved independent.  In fact it is fine if
they have arbitrary complicated dependencies as described above.  The
point is the expected common case.  Imagine that you have a GIL-less
Python and that you can, by a wave of your hand, have all the careful
locking mess magically done.  Then what I mean here is the case in which
such a theoretical program would run mostly in parallel on multiple
core, without waiting too often on the locks.

In this case, with minimal tweaks in the event dispatch loop, we can
handle multiple events on multiple threads, each in its own transaction.
A transaction_ is basically a tentative execution of the corresponding
piece of code: if we detect conflicts with other concurrently executing
transactions, we abort the whole transaction and restart it from
scratch.

.. _transaction: http://en.wikipedia.org/wiki/Transactional_memory

By now, the fact that it can basically work should be clear: multiple
transactions will only get into conflict when modifying the same data
structures, which is the case where the magical wand above would have
put locks.  If the magical program could progress without too many
locks, then the transactional program can progress without too many
conflicts.  In a way, you get even more than what the magical program
can give you: each event is dispatched in its own transaction, which
means that from each event's point of view, we have the illusion that
nobody else is running concurrently.  This is exactly what all existing
Twisted-/Stackless-/etc.-based programs are assuming.

Note that this solution, without transactions, already exists in some
other languages: for example, Erlang is all about independent events.
This is the simple case where we can just run them on multiple cores,
knowing by construction of the language that you can't get conflicts.
Of course, it doesn't work for Python or for a lot of other languages.
From that point of view, what I'm suggesting is merely that
transactional memory could be a good model to cope with the risks of
conflicts that come from not having a special-made language.

Not a perfect solution
----------------------

I would like to put some emphasis on the fact that transactional memory
(TM) is not a perfect solution either.  Right now, the biggest issue is
the performance hit that comes from the software implementation (STM).
In time, hardware support (HTM) is `likely to show up`_ and help
mitigate the problem; but I won't deny the fact that in some cases,
because it's simple enough and/or because you really need the top
performance, TM is not the best solution.

.. _`likely to show up`: http://en.wikipedia.org/wiki/Haswell_%28microarchitecture%29

Also, the explanations above are silent on what is a hard point for TM,
namely system calls.  The basic general solution is to suspend other
transactions as soon as a transaction does its first system call, so
that we are sure that the transaction will succeed.  Of course this
solution is far from optimal.  Interestingly, it's possible to do better
on a case-by-case basis: for example, by adding in-process buffers, we
can improve the situation for sockets, by having recv() store in a
buffer what is received so that it can be re-recv()-ed later if the
transaction is aborted; similarly, send() or writes to log files can be
delayed until we are sure that the transaction will commit.

From my point of view, the most important point is that the TM solution
comes from the correct side of the "determinism" scale.  With threads,
you have to prune down non-determinism.  With TM, you start from a
mostly deterministic point, and if needed, you add non-determinism.  The
reason you would want to do so is to make the transactions shorter:
shorter transactions have less risks of conflicts, and when there are
conflicts, less things to redo.  So making transactions shorter
increases the parallelism that your program can achieve, while at the
same time requiring more care.

In terms of an event-driven model, the equivalent would be to divide the
response of a big processing event into several events that are handled
one after the other: the first event sets things up and fires the second
event, which does the actual computation; and afterwards a third event
writes the results back.  As a result, the second event's transaction
has little risks of getting aborted.  On the other hand, the writing
back needs to be aware of the fact that it's not in the same transaction
as the original setting up, which means that other unrelated
transactions may have run in-between.

One step in the future?
-----------------------

These, and others, are the problems of the TM approach.  They are "new"
problems, too, in the sense that the existing ways of programming don't
have these problems.

Still, as you have guessed, I think that it is overall a win, and
possibly a big win --- a win that might be on the same scale for the age
of multiple CPUs as automatic garbage collection was 20 years ago for
the age of RAM size explosion.

Stay tuned for more!

--- Armin
