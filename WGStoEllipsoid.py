import numpy as np

def WGStoEllipsoid(x, y, z):
    """
    Convert ECEF coordinates to Ellipsoidal (longitude, latitude, height above WGS-84 ellipsoid).

    Args:
        x (ndarray[tuple[int, ...]]): X-coordinate in ECEF (meters).
        y (ndarray[tuple[int, ...]]): Y-coordinate in ECEF (meters).
        z (ndarray[tuple[int, ...]]): Z-coordinate in ECEF (meters).

    Returns:
        lambda_ (float): Longitude in radians.
        phi (float): Latitude in radians.
        h (float): Height above the ellipsoid in meters.
    """

    # WGS-84 ellipsoid parameters
    a = 6378137.0  # Semi-major axis (meters)
    f = 1 / 298.257223563  # Flattening
    e = np.sqrt(2 * f - f**2)  # Eccentricity

    # Compute longitude
    lambda_ = np.arctan2(y, x)  # atan2 ensures correct quadrant

    # Compute auxiliary value
    p = np.sqrt(x**2 + y**2)

    # Initial assumption for phi (latitude) assuming h = 0
    h = 0
    phi = np.arctan2(z, p * (1 - e**2))  # Equation 4.A.5

    # Compute the prime vertical radius of curvature
    N = a / np.sqrt(1 - (e * np.sin(phi))**2)

    # Iterative solution to refine h and phi
    delta_h = 1e6  # Large initial value
    while delta_h > 0.01:  # Convergence threshold: 1 cm
        prev_h = h
        phi = np.arctan2(z, p * (1 - e**2 * (N / (N + h))))  # Equation 4.A.5
        N = a / np.sqrt(1 - (e * np.sin(phi))**2)  # Update N
        h = p / np.cos(phi) - N  # Compute new height
        delta_h = abs(h - prev_h)  # Check convergence

    return lambda_, phi, h  # Longitude, Latitude, Height
