Report back from our survey
===========================

Hi all,

I'm here to report back the results of our survey. First, we're very pleased to
report that a number of you guys are happilly running PyPy in production! Most
(97%) of the respondants using PyPy are using it because it's faster, but a
further 26% (respondants could choose multiple answers) are using it because of
lower memory usage. Of users who aren't using PyPy, the most common reason was
C extensions, followed by "Other".

From reading the extra comments section there are a few things we've learned:

a) Google docs needs a better UI for this stuff
b) A huge number of people want NumPy and SciPy, it was easily the most
   requested C extension (25% of respondants said somthing about NumPy). We've
   already blogged on the topic of `our plans for NumPy`_.
c) Having packages in the various OS's repositories would be a big help in
   getting users up and running.

A huge thanks to everyone who responded! Finally, if you're using PyPy in
production we'd love to get a testimonial from you, if you're willing to spare
a few minutes to give us a quote or two please get in contact with us via `our
mailing list`_.

Thanks,
Alex


.. _`our plans for NumPy`: http://morepypy.blogspot.com/2011/05/numpy-in-pypy-status-and-roadmap.html
.. _`our mailing list`: http://mail.python.org/mailman/listinfo/pypy-dev