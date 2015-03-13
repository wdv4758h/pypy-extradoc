"From a software engineering perspective, 10 years is indistinguishable
from infinity, so I don't care what happens 10 years from now -- as
long as you don't blame me. :-)" - Guido van Rossum, Python creator.

10 years is indeed a long time. PyPy was created approximately 10 years ago,
with the exact date being lost in the annals of the version control system.
We've come a long way during those 10 years, from a "minimal Python" that
was supposed to serve mostly as an educational tool, through to a vehicle for
academic research to a high performance VM for Python and beyond.

Some facts from the PyPy timeline:

* In 2007, at the end of the EU funding period, we promised the JIT was just around the corner.
  It turned out we misjudged it pretty badly -- the first usable PyPy was released in 2010.

* At some point we decided to have a JavaScript backend so one could compile RPython programs
  to JavaScript and run them in a browser. Turned out it was a horrible idea.

* Another option we tried was using RPython to write CPython C extensions. Again, it turned out RPython
  is a bad language and instead we made a fast JIT, so you don't have to write C extensions.

* We made N attempts to use LLVM.  Seriously, N is 4 or 5.  But we haven't fully given up yet :-)
  They all run into issues one way or another.

* We were huge fans of ctypes at the beginning. Up to the point where we tried to make
  a restricted subset with static types, called rctypes for RPython. Turned out to be horrible.
  Twice.

* We were very hopeful about creating a JIT generator from the beginning. But the first one failed miserably,
  generating too much assembler. The second failed too. The third first burned down and then failed.
  However, we managed to release a working JIT in 2010, against all odds.

* Martijn Faassen used to ask us "how fast is PyPy" so we decided to name an option enabling all
  optimizations "--faassen".  Then "--no-faassen" was naturally added too. Later we
  decided to grow up and renamed it to "-O2", and now "-Ojit".

* The first time the Python interpreter successfully compiled to C, it segfaulted because the code generator used signed chars instead of unsigned chars...

* To make it more likely to be accepted, the proposal for the EU project contained basically every feature under the sun a language could have. This proved to be annoying, because we had to actually implement all that stuff. Then we had to do a cleanup sprint where we deleted 30% of codebase and 70% of features.

* At one sprint someone proposed a new software development methodology: 'Terminology-Driven Programming' means to pick a fancy name, then discuss what it could mean, then implement it. Examples: timeshifter, rainbow interpreter, meta-space bubble, hint annotations (all but one of these really existed).

* There is a conspiracy theory that the reason why translation is so slow is because time is stored away during it, which is later retrieved when an actual program runs to make them appear faster

Overall, it was a really long road.  However, 10 years later we are in
good shape.  A quick look on the immediate future: we are approaching
PyPy 2.0 with stackless+JIT and cffi support,
the support for Python 3 is taking shape, non-standard
extensions like STM are slowly getting ready (more soon), and there are
several non-Python interpreters around the corner (Hippy, Topaz and more).

Cheers,
fijal, arigo, cfbolz and the pypy team.
