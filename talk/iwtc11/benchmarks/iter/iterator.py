from array import array

class range1(object):
    def __init__(self, n):
        self.i = -1
        self.n = n

    def __iter__(self):
        return self

    def next(self):
        self.i += 1
        if self.i >= self.n:
            raise StopIteration
        return self.i

class range2(object):
    def __init__(self, w, h):
        self.x = -1
        self.y = 0
        self.w = w
        self.h = h

    def __iter__(self):
        return self

    def next(self):
        self.x += 1
        if self.x >= self.w:
            self.x = 0
            self.y += 1
        if self.y >= self.h:
            raise StopIteration
        return self.x, self.y

def range2(w, h):
    y = x = 0
    while y < h:
        yield x, y
        x += 1
        if x >= w:
            x = 0
            y += 1

def _sum1d(a):
    sa = 0
    for i in range1(len(a)):
        sa += a[i]

def _xsum1d(a):
    sa = 0
    for i in range1(len(a)):
        sa += a[i] + i

def _wsum1d(a):
    sa = 0
    for i in range1(len(a)):
        sa += a[i] + len(a)

def _sum2d(a, w, h):
    sa = 0
    for x, y in range2(w, h):
        sa += a[y*w + x]

def _wsum2d(a, w, h):
    sa = 0
    for x, y in range2(w, h):
        sa += a[y*w + x] + w

def _xsum2d(a, w, h):
    sa = 0
    for x, y in range2(w, h):
        sa += a[y*w + x] + x

def _whsum2d(a, w, h):
    sa = 0
    for x, y in range2(w, h):
        sa += a[y*w + x] + w + h

def _xysum2d(a, w, h):
    sa = 0
    for x, y in range2(w, h):
        sa += a[y*w + x] + x + y

def sum1d(args):
    run1d(args, _sum1d)
    return "sum1d"

def xsum1d(args):
    run1d(args, _xsum1d)
    return "xsum1d"

def wsum1d(args):
    run1d(args, _wsum1d)
    return "wsum1d"

def sum2d(args):
    run2d(args, _sum2d)
    return "sum2d"

def wsum2d(args):
    run2d(args, _wsum2d)
    return "wsum2d"

def xsum2d(args):
    run2d(args, _xsum2d)
    return "xsum2d"

def whsum2d(args):
    run2d(args, _whsum2d)
    return "whsum2d"

def xysum2d(args):
    run2d(args, _xysum2d)
    return "xysum2d"

def run1d(args, f):
    a = array('d', [1]) * 100000000
    n = int(args[0])
    for i in xrange(n):
        f(a)
    return "sum1d"

def run2d(args, f):
    a = array('d', [1]) * 100000000
    n = int(args[0])
    for i in xrange(n):
        f(a, 10000, 10000)
    return "sum1d"

    
