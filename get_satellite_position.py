import numpy as np
from scipy.optimize import fsolve

from utils import mu, OMEGA_E

def kepler_equation(E, e, Mk):
    """ Kepler's Equation: E - e*sin(E) = Mk """
    return E - e * np.sin(E) - Mk

def get_satellite_position(eph, t, compute_harmonic_correction=True):
    """
    Computes the satellite position at a given time t using ephemeris data.

    Args:
        eph (dict): Ephemeris data containing necessary parameters.
        t (float): Receiver time of week (TOW) in seconds.
        compute_harmonic_correction (bool): Apply harmonic correction if True.

    Returns:
        tuple: (x, y, z) Satellite ECEF coordinates in meters.
    """

    # Compute semi-major axis
    A = eph['sqrtA'] ** 2
    cmm = np.sqrt(mu / A ** 3)  # Computed mean motion
    tk = t - eph['toe']

    # Handle GPS week rollover
    if tk > 302400:
        tk -= 604800
    elif tk < -302400:
        tk += 604800

    # Apply mean motion correction
    n = cmm + eph['dn']

    # Compute Mean Anomaly
    Mk = eph['m0'] + (n * tk)

    # Solve Kepler's Equation for Eccentric Anomaly (Ek)
    Ek_initial = Mk  # Initial guess for numerical solver
    Ek = fsolve(kepler_equation, Ek_initial, args=(eph['e'], Mk))[0]

    # Compute True Anomaly (ν)
    sin_nu = (np.sqrt(1 - eph['e'] ** 2) * np.sin(Ek)) / (1 - eph['e'] * np.cos(Ek))
    cos_nu = (np.cos(Ek) - eph['e']) / (1 - eph['e'] * np.cos(Ek))
    nu = np.arctan2(sin_nu, cos_nu)  # True anomaly

    # Compute Argument of Latitude (Φ)
    Phi = nu + eph['w']

    # Compute Harmonic Corrections
    du, dr, di = 0, 0, 0
    if compute_harmonic_correction:
        du = eph['cus'] * np.sin(2 * Phi) + eph['cuc'] * np.cos(2 * Phi)
        dr = eph['crs'] * np.sin(2 * Phi) + eph['crc'] * np.cos(2 * Phi)
        di = eph['cis'] * np.sin(2 * Phi) + eph['cic'] * np.cos(2 * Phi)

    # Compute Corrected Parameters
    u = Phi + du  # Corrected argument of latitude
    r = A * (1 - eph['e'] * np.cos(Ek)) + dr  # Corrected radius
    i = eph['i0'] + eph['idot'] * tk + di  # Corrected inclination

    # Compute Satellite Position in Orbital Plane
    x_prime = r * np.cos(u)
    y_prime = r * np.sin(u)

    # Compute Longitude of Ascending Node
    omega = eph['omg0'] + (eph['omgdot'] - OMEGA_E) * tk - OMEGA_E * eph['toe']

    # Convert to ECEF Coordinates
    x = x_prime * np.cos(omega) - y_prime * np.cos(i) * np.sin(omega)
    y = x_prime * np.sin(omega) + y_prime * np.cos(i) * np.cos(omega)
    z = y_prime * np.sin(i)

    return np.array([[x, y, z]])
