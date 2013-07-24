from convolution.convolution import Array2D
from array import array
import math

class Random(object):
    MDIG = 32
    ONE = 1
    m1 = (ONE << (MDIG-2)) + ((ONE << (MDIG-2) )-ONE)
    m2 = ONE << MDIG/2
    dm1  = 1.0 / float(m1);

    def __init__(self, seed):
        self.initialize(seed)
        self.left = 0.0
        self.right = 1.0
        self.width = 1.0
        self.haveRange = False

    def initialize(self, seed):
    
        self.seed = seed
        seed = abs(seed)
        jseed = min(seed, self.m1)
        if (jseed % 2 == 0):
            jseed -= 1
        k0 = 9069 % self.m2;
        k1 = 9069 / self.m2;
        j0 = jseed % self.m2;
        j1 = jseed / self.m2;
        self.m = array('d', [0]) * 17 
        for iloop in xrange(17):
            jseed = j0 * k0;
            j1 = (jseed / self.m2 + j0 * k1 + j1 * k0) % (self.m2 / 2);
            j0 = jseed % self.m2;
            self.m[iloop] = j0 + self.m2 * j1;
        self.i = 4;
        self.j = 16;

    def nextDouble(self):
        I, J, m = self.i, self.j, self.m
        k = m[I] - m[J];
        if (k < 0):
            k += self.m1;
        self.m[J] = k;

        if (I == 0):
            I = 16;
        else:
            I -= 1;
        self.i = I;

        if (J == 0):
            J = 16;
        else:
            J -= 1;
        self.j = J;

        if (self.haveRange):
            return  self.left +  self.dm1 * float(k) * self.width;
        else:
            return self.dm1 * float(k);

    def RandomMatrix(self, a):
        for x, y in a.indexes():
            a[x, y] = self.nextDouble()
        return a

    def RandomVector(self, n):
        return array('d', [self.nextDouble() for i in xrange(n)])
    

class ArrayList(Array2D):
    def __init__(self, w, h, data=None):
        self.width = w
        self.height = h
        self.data = [array('d', [0]) * w for y in xrange(h)]
        if data is not None:
            self.setup(data)

    def __getitem__(self, idx):
        if isinstance(idx, tuple):
            return self.data[idx[1]][idx[0]]
        else:
            return self.data[idx]

    def __setitem__(self, idx, val):
        if isinstance(idx, tuple):
            self.data[idx[1]][idx[0]] = val
        else:
            self.data[idx] = val

    def copy_data_from(self, other):
        for l1, l2 in zip(self.data, other.data):
            l1[:] = l2

def SOR_execute(omega, G, num_iterations):
    for p in xrange(num_iterations):
        for y in xrange(1, G.height - 1):
            for x in xrange(1, G.width - 1):
                G[x, y] = omega * 0.25 * (G[x, y-1] + G[x, y+1] + G[x-1, y] + G[x+1, y]) + \
                          (1.0 - omega) * G[x, y]
def SOR(args):
    n, cycles, Array = map(eval, args)
    a = Array(n, n)
    SOR_execute(1.25, a, cycles)
    return "SOR(%d, %d)" % (n, cycles)


def SparseCompRow_matmult(M, y, val, row, col, x, num_iterations):
    for reps in xrange(num_iterations):
        for r in xrange(M):
            sa = 0.0
            for i in xrange(row[r], row[r+1]):
                sa += x[ col[i] ] * val[i]
            y[r] = sa

def SparseMatMult(args):
    N, nz, cycles = map(int, args)
    x = array('d', [0]) * N
    y = array('d', [0]) * N
    result = 0.0
    nr = nz / N
    anz = nr * N
    val = array('d', [0]) * anz
    col = array('i', [0]) * nz
    row = array('i', [0]) * (N + 1)
    row[0] = 0
    for r in xrange(N):
        rowr = row[r]
        step = r / nr
        row[r+1] = rowr + nr
        if (step < 1):
            step = 1
        for i in xrange(nr):
            col[rowr + i] = i * step
    SparseCompRow_matmult(N, y, val, row, col, x, cycles);
    return "SparseMatMult(%d, %d, %d)" % (N, nz, cycles)

def MonteCarlo_integrate(Num_samples):
    rnd = Random(113)
    under_curve = 0
    for count in xrange(Num_samples):
        x = rnd.nextDouble()
        y = rnd.nextDouble()
        if x*x + y*y <= 1.0:
            under_curve += 1
    return float(under_curve) / Num_samples * 4.0

def MonteCarlo(args):
    n = int(args[0])
    MonteCarlo_integrate(n)
    return 'MonteCarlo(%d)' % n

def LU_factor(A, pivot):
    M, N = A.height, A.width
    minMN = min(M, N)
    for j in xrange(minMN):
        jp = j
        t = abs(A[j][j])
        for i in xrange(j + 1, M):
            ab = abs(A[i][j])
            if ab > t:
                jp = i
                t = ab
        pivot[j] = jp
        
        if A[jp][j] == 0:
            raise Exception("factorization failed because of zero pivot")

        if jp != j:
            A[j], A[jp] = A[jp], A[j]

        if j < M-1:
            recp =  1.0 / A[j][j]
            for k in xrange(j + 1, M):
                A[k][j] *= recp

        if j < minMN-1:
            for ii in xrange(j + 1, M):
                for jj in xrange(j + 1, N):
                    A[ii][jj] -= A[ii][j] * A[j][jj]

def LU(args):
    N, cycles = map(int, args)
    rnd = Random(7)
    A = rnd.RandomMatrix(ArrayList(N, N))
    lu = ArrayList(N, N)
    pivot = array('i', [0]) * N
    for i in xrange(cycles):
        lu.copy_data_from(A)
        LU_factor(lu, pivot)
    return 'LU(%d, %d)' % (N, cycles)

def int_log2(n):
    k = 1
    log = 0
    while k < n:
        k *= 2
        log += 1
    if n != 1 << log:
        raise Exception("FFT: Data length is not a power of 2: %s" % n)
    return log

def FFT_num_flops(N):
    return (5.0 * N - 2) * int_log2(N) + 2 * (N + 1)

def FFT_transform_internal(N, data, direction):
    n = N / 2
    bit = 0
    dual = 1
    if n == 1:
        return
    logn = int_log2(n)
    if N == 0:
        return
    FFT_bitreverse(N, data)

    # apply fft recursion
    # this loop executed int_log2(N) times
    bit = 0
    while bit < logn:
        w_real = 1.0
        w_imag = 0.0
        theta = 2.0 * direction * math.pi / (2.0 * float(dual))
        s = math.sin(theta)
        t = math.sin(theta / 2.0)
        s2 = 2.0 * t * t
        for b in range(0, n, 2 * dual):
            i = 2 * b
            j = 2 * (b + dual)
            wd_real = data[j]
            wd_imag = data[j + 1]
            data[j] = data[i] - wd_real
            data[j + 1] = data[i + 1] - wd_imag
            data[i] += wd_real
            data[i + 1] += wd_imag
        for a in xrange(1, dual):
            tmp_real = w_real - s * w_imag - s2 * w_real
            tmp_imag = w_imag + s * w_real - s2 * w_imag
            w_real = tmp_real
            w_imag = tmp_imag
            for b in range(0, n, 2 * dual):
                i = 2 * (b + a)
                j = 2 * (b + a + dual)
                z1_real = data[j]
                z1_imag = data[j + 1]
                wd_real = w_real * z1_real - w_imag * z1_imag
                wd_imag = w_real * z1_imag + w_imag * z1_real
                data[j] = data[i] - wd_real
                data[j + 1] = data[i + 1] - wd_imag
                data[i] += wd_real
                data[i + 1] += wd_imag
        bit += 1
        dual *= 2

def FFT_bitreverse(N, data):
    n = N / 2
    nm1 = n - 1
    j = 0
    for i in range(nm1):
        ii = i << 1
        jj = j << 1
        k = n >> 1
        if i < j:
            tmp_real = data[ii]
            tmp_imag = data[ii + 1]
            data[ii] = data[jj]
            data[ii + 1] = data[jj + 1]
            data[jj] = tmp_real
            data[jj + 1] = tmp_imag
        while k <= j:
            j -= k
            k >>= 1
        j += k

def FFT_transform(N, data):
    FFT_transform_internal(N, data, -1)

def FFT_inverse(N, data):
    n = N/2
    norm = 0.0
    FFT_transform_internal(N, data, +1)
    norm = 1 / float(n)
    for i in xrange(N):
        data[i] *= norm

def FFT(args):
    N, cycles = map(int, args)
    twoN = 2*N
    x = Random(7).RandomVector(twoN)
    for i in xrange(cycles):
        FFT_transform(twoN, x)
        FFT_inverse(twoN, x)
    return 'FFT(%d, %d)' % (N, cycles)

