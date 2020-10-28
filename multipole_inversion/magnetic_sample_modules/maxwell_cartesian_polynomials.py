import numba
import numpy as np


# TODO: can be defined as static method
@numba.jit(nopython=True)
def dipole_Bz(dip_r, dip_m, pos_r, Bz_grid, Sx_range, Sy_range):
    """
    Compute the z-component of the dipole field at the pos_r position(s), from
    a group of particles located at the dip_r dipole_positions, and which have
    magnetic dipole moments given in the dip_m array.

    For these arrays, N > 1

    dip_r   :: N x 3 array with dipole positions (m)
    dip_m   :: N x 3 array with dipole moments (Am^2)
    pos_r   :: 1 x 3 array with coordinates of measurement point (m)

    Returns

    N x 3 array  :: Rows are Bz generated by each particle
    """
    # For every row of dip_r (Nx3 array), subtract pos_r (1x3 array)
    for j, y in enumerate(Sy_range):
        for i, x in enumerate(Sx_range):
            r = pos_r[j, i] - dip_r
            x, y, z = r[:, 0], r[:, 1], r[:, 2]

            rho2 = np.sum(r ** 2, axis=1)
            rho = np.sqrt(rho2)

            sp = dip_m[:, 0] * x + dip_m[:, 1] * y + dip_m[:, 2] * z
            f = 3e-7 * sp / (rho2 * rho2 * rho)
            g = -1e-7 / (rho2 * rho)

            # Only return Bz
            res = f * z + g * dip_m[:, 2]

            Bz_grid[j, i] += np.sum(res)

    return None


@numba.jit(nopython=True)
def quadrupole_Bz(quad_r, quad_m, pos_r, Bz_grid, Sx_range, Sy_range):
    """
    Compute the z-component of the field of a point quadrupole at the pos_r
    position(s), from a group of particles located at the quad_r quadrupole
    positions, and which have magnetic quadrupole moments given in the quad_m
    array.

    For these arrays, N > 1

    quad_r   :: N x 3 array with point quadrupole positions (m)
    quad_m   :: N x 3 array with quadrupole moments (A m)
    pos_r    :: 1 x 3 array (m)

    Returns

    N x 3 array
    """
    # For every row of dip_r (Nx3 array), subtract pos_r (1x3 array)
    for j, y in enumerate(Sy_range):
        for i, x in enumerate(Sx_range):

            r = pos_r[j, i] - quad_r
            x, y, z = r[:, 0], r[:, 1], r[:, 2]
            x2, y2, z2 = x ** 2, y ** 2, z ** 2

            rho2 = np.sum(r ** 2, axis=1)
            rho = np.sqrt(rho2)

            q1, q2, q3, q4, q5 = (quad_m[:, i] for i in range(5))

            q_field = q1 * (5 * z * (x2 - z2) + 2 * rho2 * z)
            q_field += q2 * 10 * x * y * z
            q_field += q3 * 2 * x * (5 * z2 - rho2)
            q_field += q4 * (5 * z * (y2 - z2) + 2 * rho2 * z)
            q_field += q5 * 2 * y * (5 * z2 - rho2)

            f = 1e-7 / (rho2 * rho2 * rho2 * rho)

            # Only return Bz
            Bz_grid[j, i] += f * q_field

    return None


@numba.jit(nopython=True)
def octupole_Bz(oct_r, oct_m, pos_r, Bz_grid, Sx_range, Sy_range):
    """
    Compute the z-component of the field of a point octupole at the pos_r
    position(s), from a group of particles located at the oct_r octupole
    positions, and which have magnetic octupole moments given in the oct_m
    array.

    For these arrays, N > 1

    oct_r   :: N x 3 array with point octupole positions (m)
    oct_m   :: N x 3 array with octupole moments (A m)
    pos_r    :: N x 3 array OR 1 x 3 array (m)

    Returns

    N x 3 array
    """
    for j, y in enumerate(Sy_range):
        for i, x in enumerate(Sx_range):
            r = pos_r[j, i] - oct_r
            x, y, z = r[:, 0], r[:, 1], r[:, 2]
            x2, y2, z2 = x ** 2, y ** 2, z ** 2

            rho2 = np.sum(r ** 2, axis=1)
            rho = np.sqrt(rho2)

            w1, w2, w3, w4, w5, w6, w7 = (oct_m[:, i] for i in range(7))

            o_field = w1 * 5 * x * z * (7 * (x2 - 3 * z2) + 6 * rho2)
            o_field += w2 * 15 * y * z * (7 * (x2 - z2) + 2 * rho2)
            o_field += w3 * 5 * (7 * z2 * (3 * x2 - z2) - 3 * rho2 * (x2 - z2))
            o_field += w4 * 30 * x * y * (7 * z2 - rho2)
            o_field += w5 * 15 * x * z * (7 * (y2 - z2) + 2 * rho2)
            o_field += w6 * 5 * y * z * (7 * (y2 - 3 * z2) + 6 * rho2)
            o_field += w7 * 5 * (7 * z2 * (3 * y2 - z2) - 3 * rho2 * (y2 - z2))

            f = 1e-7 / (rho2 * rho2 * rho2 * rho2 * rho)

            # Only return Bz
            Bz_grid += f * o_field

    return None
