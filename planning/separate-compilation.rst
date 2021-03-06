Separate Compilation
====================

Goal
----

Translation extension modules written in RPython.
The best form is probably the MixedModule.

Strategy
--------

The main executable (bin/pypy-c or libpypy-c.dll) exports RPython
functions; this "first translation" also produces a pickled object
that describe these functions: signatures, exception info, etc.

It will probably be necessary to list all exported functions and methods,
or mark them with some @exported decorator.

The translation of an extension module (the "second translation") will
reuse the information from the pickled object; the content of the
MixedModule is annotated as usual, except that functions exported by
the main executable are now external calls.

The extension module simply has to export a single function
"init_module()", which at runtime uses space operations to create and
install a module.


Roadmap
-------

* First, a framework to test and measure progress; builds two
  shared libraries (.so or .dll):
  
  - the first one is the "core module", which exports functions 
  - that can be called from the second module, which exports a single
    entry point that we call call with ctypes.

* Find a way to mark functions as "exported".  We need to either
  provide a signature, or be sure that the functions is somehow
  annotated (because it is already used by the core interpreter)

* Pass structures (as opaque pointers). At this step, only the core
  module has access to the fields.

* Implement access to struct fields: an idea is to use a Controller
  object, and redirect attribute access to the ClassRepr computed by
  the first translation.

* Implement method calls, again with the help of the Controller which
  can replace calls to bound methods with calls to exported functions.

* Share the ExceptionTransformer between the modules: a RPython
  exception raised on one side can be caught by the other side.

* Support subclassing.  Two issues here:

  - isinstance() is translated into a range check, but these minid and
    maxid work because all classes are known at translation time.
    Subclasses defined in the second module must use the same minid
    and maxid as their parent; isinstance(X, SecondModuleClass) should
    use an additional field.  Be sure to not confuse classes
    separately created in two extension modules.

  - virtual methods, that override methods defined in the first
    module.

* specialize.memo() needs to know all possible values of a
  PreBuildConstant to compute the results during translation and build
  some kind of lookup table.  The most obvious case is the function
  space.gettypeobject(typedef).  Fortunately a PBC defined in a module
  can only be used from the same module, so the list of prebuilt
  results is probably local to the same module and this is not really
  an issue.

* Integration with GC.  The GC functions should be exported from the
  first module, and we need a way to register the static roots of the
  second module.

* Integration with the JIT.
