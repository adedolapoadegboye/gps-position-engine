import numpy as np

def estimate_position(xs, pr, numSat, x0, b0, dim):
    """
    Estimate the user's position and clock bias.

    Args:
        xs (np.array): Satellite position matrix (shape: numSat x dim).
        pr (np.array): Corrected pseudo ranges (adjusted for satellite clock bias).
        numSat (int): Number of satellites.
        x0 (np.array): Initial estimate of user position (shape: (dim,)).
        b0 (float): Initial estimate of user clock bias.
        dim (int): Dimension (3 for 3D, 2 for 2D).

    Returns:
        x (np.array): Optimized user position (shape: (dim,)).
        b (float): Optimized user clock bias.
        norm_dp (float): Normalized pseudo-range difference.
        G (np.array): User-satellite geometry matrix (useful for DOP calculations).
    """

    dx = 100 * np.ones(dim)  # Initialize position difference
    db = 0  # Clock bias difference
    norm_dp = 100  # Large initial pseudo-range difference
    numIter = 0
    b = b0  # Initialize user clock bias

    # Iterate until the solution converges
    while np.linalg.norm(dx) > 1e-3:  # Stop when position change is small
        norms = np.linalg.norm(xs - x0, axis=0)  # Compute satellite-user distances

        print(f"norms: {norms}")


        # Compute delta pseudo range
        dp = pr - norms + b - b0

        print(f"dp: {dp}")

        # Construct the user-satellite geometry matrix G
        G = np.hstack((-(xs - x0) / norms[:, np.newaxis], np.ones((numSat, 1))))

        # Solve the least squares problem using the normal equation
        sol = np.linalg.inv(G.T @ G) @ G.T @ dp

        dx = sol[:dim]  # Position correction
        db = sol[dim]  # Clock bias correction
        norm_dp = np.linalg.norm(dp)  # Update pseudo-range difference
        numIter += 1

        # Update estimates
        x0 += dx
        b0 += db

        print(f"x0: {x0}")
        print(f"b0: {b0}")


    return x0, b0, norm_dp, G
