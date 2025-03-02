import numpy as np
from scipy.optimize import fsolve
from sympy import symbols, Eq, solve

from utils import F, mu, DEBUG

def estimate_satellite_clock_bias(t, eph):
    """
    Estimates the satellite clock bias at time t using ephemeris data.

    Args:
        t (float): Receiver time of week.
        eph (dict): Ephemeris data containing necessary parameters.

    Returns:
        float: Satellite clock bias (seconds).
    """
    # Debugging: Ensure eph is passed correctly
    print("DEBUG: Inside estimate_satellite_clock_bias()") if DEBUG else None
    print(f"DEBUG: Received t = {t}") if DEBUG else None
    print(f"DEBUG: Received eph = {eph}") if DEBUG else None

    # Check if eph is None or not a dictionary
    if eph is None:
        raise ValueError("Error: eph is None. Ensure valid ephemeris data is passed.")

    if not isinstance(eph, dict):
        raise TypeError(f"Error: eph is of type {type(eph)}, expected dict.")

    required_keys = ['sqrtA', 'toe', 'dn', 'm0', 'e', 'af0', 'af1', 'af2', 'toc']
    for key in required_keys:
        if key not in eph:
            raise KeyError(f"Error: Missing key '{key}' in ephemeris data.")

    # Compute semi-major axis
    A = eph['sqrtA'] ** 2
    cmm = np.sqrt(mu / (A ** 3))  # Computed mean motion
    tk = t - eph['toe']

    # Handle GPS week crossover
    if tk > 302400:
        tk -= 604800
    elif tk < -302400:
        tk += 604800

    # Apply mean motion correction
    n = cmm + eph['dn']

    # Compute Mean Anomaly
    Mk = eph['m0'] + (n * tk)

    # Solve for Eccentric Anomaly numerically
    Ek_initial = Mk  # Initial guess

    def kepler_eq(Ek):
        return Ek - eph['e'] * np.sin(Ek) - Mk

    # Ensure kepler_eq is defined and working
    try:
        Ek = fsolve(kepler_eq, Ek_initial)[0]
    except Exception as e:
        raise RuntimeError(f"Error in solving Kepler's equation: {e}") if DEBUG else None

    # Compute satellite clock bias
    dsv = (eph['af0'] +
           eph['af1'] * (t - eph['toc']) +
           eph['af2'] * (t - eph['toc']) ** 2 +
           F * eph['e'] * eph['sqrtA'] * np.sin(Ek))

    print(f"DEBUG: Computed satellite clock bias = {dsv}") if DEBUG else None
    return float(dsv)


