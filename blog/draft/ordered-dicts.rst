Faster, more memory efficient and more ordered dictionaries on PyPy
-------------------------------------------------------------------

Hello everyone!

As of today, we merged the latest branch that brings better dictionaries to PyPy by default. The work is based on an idea by Raymond Hettinger on python-dev [https://mail.python.org/pipermail/python-dev/2012-December/123028.html], with prior work done notably in Java.  It was done by Maciej Fijałkowski and Armin Rigo, with Laurence Tratt recently prodding us to finish it.  (Earlier work going in a similar direction include Alex Gaynor's work on ordered dicts in Topaz, which was also used in the Hippy VM.  Each of these pieces of work is itself based on the original dict implementation in RPython, whose origins fade in the Subversion prehistory of PyPy.)  Coincidentally, a very similar idea has been implemented in Zend PHP very recently [https://nikic.github.io/2014/12/22/PHPs-new-hashtable-implementation.html].

This post covers the basics of design and implementation as well as some basic benchmarks.


Dictionaries are now ordered!
-----------------------------

One surprising part is that the new design, besides being more
memory efficient, is ordered by design: it preserves the
insertion order.  This is not forbidden by the Python language, which allows any order.  It makes the ``collections.OrderedDict`` subclass much faster than before: it is now a thin subclass of ``dict``.  Obviously, we recommend that any portable Python program continues to use ``OrderedDict`` when ordering is important.  Note that a non-portable program might rely on more: for example, a ``**keywords`` argument now receives the keywords in the same order as the one in which they were given in the call.  (Whether such a thing might be called a language design change or not is a bit borderline.)  The point is that Python programs that work on CPython or previous versions of PyPy should continue to work on PyPy.

There is one exception, though.  The iterators of the ``OrderedDict`` subclass are now working just like the ones of the ``dict`` builtin: they will raise ``RuntimeError`` when iterating if the dictionary was modified.  In the CPython design, the class ``OrderedDict`` explicitly doesn't worry about that, and instead you get some result that might range from correct to incorrect to crashes (i.e. random Python exceptions).


Original PyPy dictionary design
-------------------------------

Originally, PyPy dictionaries, as well as CPython dictionaries
are implemented as follows (simplified view)::

  struct dict {
     long num_items;
     dict_entry* items;   /* pointer to array */
  }

  struct dict_entry {
     long hash;
     PyObject* key;
     PyObject* value;
  }

Where items is a sparse array, with 1/3 to 1/2 of the items being NULL.
The average space occupied by a dictionary is ``3 * WORD * 12/7`` plus some small constant (the smallest dict has 8 entries, which is
``8 * 3 * WORD + 2 * WORD = 26 WORDs``).


New PyPy dictionary design
--------------------------

The new PyPy dictionary is split in two arrays::

  struct dict {
      long num_items;
      variable_int *sparse_array;
      dict_entry* compact_array;
  }
  
  struct dict_entry {
      long hash;
      PyObject *key;
      PyObject *value;
  }
  
Here, ``compact_array`` stores all the items in order of insertion, while ``sparse_array`` is a 1/2 to 2/3 full array of integers. The integers themselves are of the smallest size necessary for indexing the ``compact_array``. So if ``compact_array`` has less than 256 items, then ``sparse_array`` will be made of bytes; if less than 2^16, it'll be two-byte integers; and so on.

This design saves quite a bit of memory. For example, on 64bit systems we can, but almost never, use indexing of more than 4 billion elements; and for small dicts, the extra ``sparse_array`` takes very little space.  For example a 100 element dict, would be on average for the original design on 64bit: 100 * 12/7 * WORD * 3 =~ 4100 bytes, while on new design it's 100 * 12/7 + 3 * WORD * 100 =~ 2600 bytes, quite a significant saving.

GC friendliness
---------------

The obvious benefit of having more compact dictionaries is an increased cache friendliness. In modern CPUs cache misses are much more costly than doing additional simple work, like having an additional level of (in-cache) indirection. Additionally, there is a GC benefit coming from it. When doing a minor collection, the GC has to visit all the GC fields in old objects that can point to young objects. In the case of large arrays, this can prove problematic since the array grows and with each minor collection we need to visit more and more GC pointers. In order to avoid it, large arrays in PyPy employ a technique called "card marking" where the GC only visits "cards" or subsets of arrays that were modified between collections. The problem with dictionaries was that by design modifications in a dictionary occur randomly, hence a lot of cards used to get invalidated. In the new design, however, new items are typically appended to the ``compact_array``, hence invalidate much fewer cards --- which improves GC performance.  (The new ``sparse_array`` is an array of integers, so it does not suffer from the same problems.)


Deletion
--------

Deleting entries from dictionaries is not very common, but important in a few use cases.  To preserve order, when we delete an entry, we mark the entry as removed but don't otherwise shuffle the remaining entries.  If we repeat this operation often enough, there will be a lot of removed entries in the (originally compact) array.  At this point, we need to do a "packing" operation, which moves all live entries to the start of the array (and then reindexes the sparse array, as the positions changed).  This works well, but there are use cases where previously no reindexing was ever needed, so it makes these cases a bit slower (for example when repeatedly adding and removing keys in equal number).

Benchmarks
----------

The PyPy speed benchmarks show mostly small effect [http://speed.pypy.org/changes/?tre=10&rev=75419%3Ac52fc1774518&exe=1&env=1]. The microbenchmarks that we did show large improvements on large and very large dictionaries (particularly, building dictionaries of at least a couple 100s of items is now twice faster) and break-even on small ones (between 20% slower and 20% faster depending very much on the usage patterns and sizes of dictionaries). The new dictionaries enable various optimization possibilities which we're going to explore in the near future.

Cheers,
fijal, arigo and the PyPy team
