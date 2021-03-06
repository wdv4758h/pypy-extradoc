==========================
How PyPy runs your program
==========================

[[The talk will be given by Maciej Fijalkowski,
both long time PyPy core developer and expert in the area of
Python performance.]]

In this talk we would like to have a short introduction on how Python
programs are compiled and executed, with a special attention towards
just in time compilation done by PyPy. PyPy is the most advanced Python
interpreter around and while it should generally just speed up your programs
there is a wide range of performance that you can get out of PyPy, ranging from
slightly faster than CPython to C speeds, depending on how you write your
programs.

We will split the talk in two parts. In the first part we will explain
how things work and what can and what cannot be optimized as well as describe
the basic heuristics of JIT compiler and optimizer. In the next part we will
do a survey of existing tools for looking at performance of Python programs
with specific focus on PyPy.

As a result of this talk, an audience member should be better equipped with
tools how to write new software and improve existing software with performance
in mind.
