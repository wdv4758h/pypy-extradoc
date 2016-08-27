Hi all,

PyPy's JIT now supports the 64-bit PowerPC architecture!  This is the
third architecture supported, in addition to x86 (32 and 64) and ARM
(32-bit only).  More precisely, we support Linux running the big- and the
little-endian variants of ppc64.  Thanks to IBM for funding this work!

The new JIT backend has been merged into "default".  You should be able
to translate PPC versions `as usual`__ directly on the machines.  For
the foreseeable future, I will compile and distribute binary versions
corresponding to the official releases (for Fedora), but of course I'd
welcome it if someone else could step in and do it.  Also, it is unclear
yet if we will run a buildbot.

.. __: http://pypy.org/download.html#building-from-source

To check that the result performs well, I logged in a ppc64le machine
and ran the usual benchmark suite of PyPy (minus sqlitesynth: sqlite
was not installed on that machine).  I ran it twice at a difference of
12 hours, as an attempt to reduce risks caused by other users suddenly
using the machine.  The machine was overall relatively quiet.  Of
course, this is scientifically not good enough; it is what I could come
up with given the limited resources.

Here are the results, where the numbers are speed-up factors between the
non-jit and the jit version of PyPy.  The first column is x86-64, for
reference.  The second and third columns are the two ppc64le runs.  All
are Linux.  A few benchmarks are not reported here because the runner
doesn't execute them on non-jit (however, apart from sqlitesynth, they
all worked).

::

    ai                        13.7342        16.1659          14.9091
    bm_chameleon               8.5944         8.5858             8.66
    bm_dulwich_log             5.1256         5.4368           5.5928
    bm_krakatau                5.5201         2.3915           2.3452
    bm_mako                    8.4802         6.8937           6.9335
    bm_mdp                     2.0315         1.7162           1.9131
    chaos                     56.9705        57.2608          56.2374
    sphinx                                          
    crypto_pyaes               62.505         80.149          79.7801
    deltablue                  3.3403         5.1199           4.7872
    django                    28.9829         23.206            23.47
    eparse                     2.3164         2.6281            2.589
    fannkuch                   9.1242        15.1768          11.3906
    float                     13.8145        17.2582          17.2451
    genshi_text               16.4608        13.9398          13.7998
    genshi_xml                 8.2782         8.0879           9.2315
    go                         6.7458        11.8226          15.4183
    hexiom2                   24.3612        34.7991          33.4734
    html5lib                   5.4515         5.5186            5.365
    json_bench                28.8774        29.5022          28.8897
    meteor-contest             5.1518         5.6567           5.7514
    nbody_modified            20.6138        22.5466          21.3992
    pidigits                   1.0118          1.022           1.0829
    pyflate-fast               9.0684        10.0168          10.3119
    pypy_interp                3.3977         3.9307           3.8798
    raytrace-simple           69.0114       108.8875         127.1518
    richards                  94.1863       118.1257         102.1906
    rietveld                   3.2421         3.0126           3.1592
    scimark_fft                                     
    scimark_lu                                      
    scimark_montecarlo                              
    scimark_sor                                     
    scimark_sparsematmul                            
    slowspitfire               2.8539         3.3924           3.5541
    spambayes                  5.0646         6.3446            6.237
    spectral-norm             41.9148        42.1831          43.2913
    spitfire                   3.8788         4.8214            4.701
    spitfire_cstringio          7.606         9.1809           9.1691
    sqlitesynth                                     
    sympy_expand               2.9537         2.0705           1.9299
    sympy_integrate            4.3805         4.3467           4.7052
    sympy_str                  1.5431         1.6248           1.5825
    sympy_sum                  6.2519          6.096           5.6643
    telco                     61.2416        54.7187          55.1705
    trans2_annotate                                 
    trans2_rtype                                    
    trans2_backendopt                               
    trans2_database                                 
    trans2_source                                   
    twisted_iteration         55.5019        51.5127          63.0592
    twisted_names              8.2262         9.0062           10.306
    twisted_pb                12.1134         13.644          12.1177
    twisted_tcp                4.9778          1.934           5.4931
                                                    
    GEOMETRIC MEAN               9.31           9.70            10.01

The last line reports the geometric mean of each column.  We see that
the goal was reached: PyPy's JIT actually improves performance by a
factor of around 9.7 to 10 times on ppc64le.  By comparison, it "only"
improves performance by a factor 9.3 on Intel x86-64.  I don't know why,
but I'd guess it mostly means that a non-jitted PyPy performs slightly
better on Intel than it does on PowerPC.

Why is that?  Actually, similar numbers are also higher on ARM than on
Intel.  We like to guess that on ARM, running the whole interpreter in
PyPy takes up a lot of resources, e.g. the instruction cache, which the
JIT's assembler doesn't need any more after the process is warmed up.
This argument doesn't work for PowerPC, but there are other more subtle
variants of it.  Notably, Intel is doing crazy things about branch
prediction, which likely helps a big interpreter---both the non-JITted
PyPy and CPython, and both for the interpreter's main loop itself and
for the numerous indirect branches that depend on the types of the
objects.  Moreover, on PowerPC I did notice that gcc itself is not
perfect at optimization: during development of this backend, I often
looked at assembler produced by gcc, and there are a number of
inefficiencies there.  All these are factors that slow down the
non-JITted version of PyPy, but don't influence the speed of the
assembler produced just-in-time.

Anyway, this is just guessing.  The fact remains that PyPy can now
be used on PowerPC machines.  Have fun!


A bientot,

Armin.
