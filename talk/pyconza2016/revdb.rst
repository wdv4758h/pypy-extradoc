RevDB, a reverse debugger
========================================


Abstract
--------

RevDB is an experimental "reverse debugger" for Python, similar to
UndoDB-GDB or LL for C. You run your program once, in "record" mode,
producing a log file; once you get buggy behavior, you start the
reverse-debugger on the log file. It gives an (improved) pdb-like
experience, but it is replaying your program exactly as it ran---all
input/outputs are replayed from the log file instead of being redone.

The main point is that you can then go backward as well as forward in
time: from a situation that looks really buggy you can go back and
discover how it came to be. You also get "watchpoints", which are very
useful to find when things change. Watchpoints work both forward and
backward.

I will show on small examples how you can use it, and also give an idea
about how it works. It is based on PyPy, not CPython, so you need to
ensure your program works on PyPy in the first place (but chances are
that it does).
