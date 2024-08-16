import ctypes
import numpy as np
from .flags import *
from . import _nfstlib
from . import nfst_plan

# Set arugment and return types for functions
_nfstlib.jnfst_init.argtypes = [
    ctypes.POINTER(nfst_plan),
    ctypes.c_int32,
    ctypes.POINTER(ctypes.c_int32),
    ctypes.c_int32,
    ctypes.POINTER(ctypes.c_int32),
    ctypes.c_int32,
    ctypes.c_uint32,
    ctypes.c_uint32,
]

_nfstlib.jnfst_alloc.restype = ctypes.POINTER(nfst_plan)
_nfstlib.jnfst_finalize.argtypes = [ctypes.POINTER(nfst_plan)]

_nfstlib.jnfst_set_x.argtypes = [
    ctypes.POINTER(nfst_plan),
    np.ctypeslib.ndpointer(np.float64, flags="C"),
]
_nfstlib.jnfst_set_f.argtypes = [
    ctypes.POINTER(nfst_plan),
    np.ctypeslib.ndpointer(np.float64, ndim=1, flags="C"),
]
_nfstlib.jnfst_set_fhat.argtypes = [
    ctypes.POINTER(nfst_plan),
    np.ctypeslib.ndpointer(np.float64, ndim=1, flags="C"),
]

_nfstlib.jnfst_trafo.argtypes = [ctypes.POINTER(nfst_plan)]
_nfstlib.jnfst_adjoint.argtypes = [ctypes.POINTER(nfst_plan)]
_nfstlib.jnfst_trafo_direct.argtypes = [ctypes.POINTER(nfst_plan)]
_nfstlib.jnfst_adjoint_direct.argtypes = [ctypes.POINTER(nfst_plan)]


class NFST:
    """
    Class to perform non-equispaced fast sine transforms (NFST)
    With a dimension of **D**.
    Just **N** and **M** are required for initializing a plan.
    """

    def __init__(self, N, M, n=None, m=default_window_cut_off, f1=None, f2=f2_default):
        self.plan = _nfstlib.jnfst_alloc()
        self.N = N  # bandwidth tuple
        N_ct = N.ctypes.data_as(ctypes.POINTER(ctypes.c_int32))
        self.M = M  # number of nodes
        self.n = n  # oversampling per dimension
        self.m = m  # window size
        self.D = len(N)  # dimensions

        if any(x <= 0 for x in N):
            raise ValueError(f"Invalid N: {N}. Argument must be a positive integer")

        if M <= 0:
            raise ValueError(f"Invalid M: {M}. Argument must be a positive integer")

        if n is None:
            self.n = (2 ** (np.ceil(np.log(self.N) / np.log(2)) + 1)).astype("int32")
            n_ct = self.n.ctypes.data_as(ctypes.POINTER(ctypes.c_int32))

        if any(x <= 0 for x in self.n):
            raise ValueError(
                f"Invalid n: {self.n}. Argument must be a positive integer"
            )

        if any(x <= y for x, y in zip(self.n, N)):
            raise ValueError(f"Invalid n: {self.n}. Argument must fulfil n_i > N_i")

        if sum(x % 2 for x in self.n) != 0:
            raise ValueError(f"Invalid n: {self.n}. Argument must be an even integer")

        if m <= 0:
            raise ValueError(f"Invalid m: {m}. Argument must be a positive integer")

        if f1 is None:
            self.f1 = f1_default if self.D > 1 else f1_default_1d
        else:
            self.f1 = f1

        self.f2 = f2  # FFTW flags
        _nfstlib.jnfst_init(
            self.plan, self.D, N_ct, self.M, n_ct, self.m, self.f1, self.f2
        )
        self.init_done = True  # bool for plan init
        self.finalized = False  # bool for finalizer
        self.x = None  # nodes, will be set later
        self.f = None  # function values
        self.fhat = None  # Fourier coefficients

    def __del__(self):
        self.finalize_plan()

    def nfst_finalize_plan(self):
        """
        Finalizes an NFST plan.
        This function does not have to be called by the user.
        """
        _nfstlib.jnfst_finalize.argtypes = (ctypes.POINTER(nfst_plan),)  # P

        if not self.init_done:
            raise ValueError("NFST not initialized.")

        if not self.finalized:
            self.finalized = True
            _nfstlib.jnfst_finalize(self.plan)

    def finalize_plan(self):
        """
        Alternative call for **nfst_finalize_plan()**
        """
        return self.nfst_finalize_plan()

    def nfst_init(self):
        """
        Initializes the NFCT plan in C.
        This function does not have to be called by the user.
        """
        # Convert N and n to numpy arrays for passing them to C
        Nv = np.array(self.N, dtype=np.int32)
        n = np.array(self.n, dtype=np.int32)

        # Call init for memory allocation
        ptr = _nfstlib.jnfst_alloc()

        # Set the pointer
        self.plan = ctypes.cast(ptr, ctypes.POINTER(nfst_plan))

        # Initialize values
        _nfstlib.jnfst_init(
            self.plan,
            ctypes.c_int(self.D),
            ctypes.cast(Nv.ctypes.data, ctypes.POINTER(ctypes.c_int)),
            ctypes.c_int(self.M),
            ctypes.cast(n.ctypes.data, ctypes.POINTER(ctypes.c_int)),
            ctypes.c_int(self.m),
            ctypes.c_uint(self.f1),
            ctypes.c_uint(self.f2),
        )
        self.init_done = True

    def init(self):
        """
        Alternative call for **nfst_init()**
        """
        return self.nfst_init()

    @property
    def x(self):
        return self._X

    @x.setter
    def x(self, value):
        if value is not None:
            if not (
                isinstance(value, np.ndarray)
                and value.dtype == np.float64
                and value.flags["C"]
            ):
                raise RuntimeError("x has to be C-continuous, numpy float64 array")
            if self.D == 1:
                _nfstlib.jnfst_set_x.restype = np.ctypeslib.ndpointer(
                    dtype=np.float64, ndim=2, shape=self.M, flags="C"
                )
            else:
                _nfstlib.jnfst_set_x.restype = np.ctypeslib.ndpointer(
                    dtype=np.float64, ndim=2, shape=(self.M, self.D), flags="C"
                )
            self._X = _nfstlib.jnfst_set_x(self.plan, value)

    @property
    def f(self):
        return self._f

    @f.setter
    def f(self, value):
        if value is not None:
            if not (
                isinstance(value, np.ndarray)
                and value.dtype == np.float64
                and value.flags["C"]
            ):
                raise RuntimeError("f has to be C-continuous, numpy float64 array")
            _nfstlib.jnfst_set_f.restype = np.ctypeslib.ndpointer(
                np.float64, ndim=1, shape=self.M, flags="C"
            )
            self._f = _nfstlib.jnfst_set_f(self.plan, value)

    @property
    def fhat(self):
        return self._fhat

    @fhat.setter
    def fhat(self, value):
        Ns = np.prod(self.N - 1)
        if value is not None:
            if not (isinstance(value, np.ndarray) and value.dtype == np.float64):
                raise RuntimeError("fhat has to be a numpy float64 array")
            if not value.flags["C"]:
                raise RuntimeError("fhat has to be C-continuous")
            if value.size != Ns:
                raise ValueError(f"fhat has to be an array of size {Ns}")
            _nfstlib.jnfst_set_fhat.argtypes = [
                ctypes.POINTER(nfst_plan),
                np.ctypeslib.ndpointer(np.float64, ndim=1, flags="C"),
            ]
            _nfstlib.jnfst_set_fhat.restype = np.ctypeslib.ndpointer(
                np.float64, ndim=1, shape=(Ns,), flags="C_CONTIGUOUS"
            )
            self._fhat = _nfstlib.jnfst_set_fhat(self.plan, value)

    @property
    def num_threads(self):
        return _nfstlib.nfft_get_num_threads()

    def nfst_trafo(self):
        """
        Computes the NDFT via the fast NFST algorithm for the provided nodes in **x** and coefficients in **fhat**.
        """
        Ns = np.prod(self.N - 1)
        _nfstlib.jnfst_trafo.restype = np.ctypeslib.ndpointer(
            np.float64, shape=Ns, flags="C"
        )
        # Prevent bad stuff from happening
        if self.finalized:
            raise RuntimeError("NFST already finalized")

        if not hasattr(self, "fhat"):
            raise ValueError("fhat has not been set.")

        if not hasattr(self, "x"):
            raise ValueError("x has not been set.")

        ptr = _nfstlib.jnfst_trafo(self.plan)
        self.f = ptr

    def trafo(self):
        """
        Alternative call for **nfst_trafo()**
        """
        return self.nfst_trafo()

    def nfst_trafo_direct(self):
        """
        Computes the NDST via naive matrix-vector multiplication for provided nodes in **x** and coefficients in **fhat**.
        """
        Ns = np.prod(self.N - 1)
        _nfstlib.jnfst_trafo_directed.restype = np.ctypeslib.ndpointer(
            np.float64, shape=Ns, flags="C"
        )
        # Prevent bad stuff from happening
        if self.finalized:
            raise RuntimeError("NFST already finalized")

        if self.fhat is None:
            raise ValueError("fhat has not been set.")

        if self.x is None:
            raise ValueError("x has not been set.")

        ptr = _nfstlib.jnfst_trafo_direct(self.plan)
        self.f = ptr

    def trafo_direct(self):
        """
        Alternative call for nfst_trafo_direct()
        """
        return self.nfst_trafo_direct()

    def nfst_transposed(self):
        """
        Computes the transposed NDST via the fast transposed NFST algorithm for the provided nodes in **x** and coefficients in **f**.
        """
        Ns = np.prod(self.N - 1)
        _nfstlib.jnfst_adjoint.restype = np.ctypeslib.ndpointer(
            np.float64, shape=Ns, flags="C"
        )
        # Prevent bad stuff from happening
        if self.finalized:
            raise RuntimeError("NFST already finalized")

        if self.f is None:
            raise ValueError("f has not been set.")

        if self.x is None:
            raise ValueError("x has not been set.")

        ptr = _nfstlib.jnfst_adjoint(self.plan)
        self.fhat = ptr

    def nfst_transposed_direct(self):
        """
        Computes the transposed NDST via naive matrix-vector multiplication for provided nodes in **x** and coefficients in **f**.
        """
        # Prevent bad stuff from happening
        if self.finalized:
            raise RuntimeError("NFST already finalized")

        if self.f is None:
            raise ValueError("f has not been set.")

        if self.x is None:
            raise ValueError("x has not been set.")

        ptr = _nfstlib.jnfst_adjoint_direct(self.plan)
        self.fhat = ptr

    def nfst_adjoint(self):
        """
        Alternative call for nfst_transposed()
        """
        return self.nfst_transposed()

    def nfst_adjoint_direct(self):
        """
        Alternative call for nfst_transposed_direct()
        """
        return self.nfst_transposed_direct()

    def adjoint(self):
        """
        Alternative call for nfst_adjoint()
        """
        return self.nfst_adjoint()

    def adjoint_direct(self):
        """
        Alternative call for nfst_adjoint_direct()
        """
        return self.nfst_adjoint_direct()
