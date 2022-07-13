cimport numpy as cnp
import numpy as np
from libc.stdlib cimport malloc, free
from cpython.mem cimport PyMem_Malloc, PyMem_Free 

# -----------------------------------------------------------------------------

cdef extern from "spherical_harmonics_basis_c.cuh":

    void SHB_populate_matrix_cuda(double * r_sources,
                                  double * r_sensors,
                                  double * Q,
                                  unsigned long long Nsources,
                                  unsigned long long Nsensors,
                                  int multipole_order,
                                  int verbose
                                  )

# -----------------------------------------------------------------------------

def SHB_populate_matrix(double [:] r_sources, double [:] r_sensors,
                        double [:] Q,
                        unsigned long long Nsources,
                        unsigned long long Nsensors,
                        int multipole_order,
                        int verbose
                        ):

    # Call the C function
    SHB_populate_matrix_cuda(&r_sources[0], &r_sensors[0], &Q[0],
                             Nsources, Nsensors, multipole_order, verbose)

