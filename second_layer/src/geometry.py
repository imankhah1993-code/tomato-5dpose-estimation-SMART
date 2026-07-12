import numpy as np


def fit_sphere(points):
    X = points[:, 0]
    Y = points[:, 1]
    Z = points[:, 2]

    A = np.column_stack((2 * X, 2 * Y, 2 * Z, np.ones(len(points))))
    b = X**2 + Y**2 + Z**2

    x, *_ = np.linalg.lstsq(A, b, rcond=None)

    cx, cy, cz, d = x
    radius = np.sqrt(d + cx**2 + cy**2 + cz**2)

    return cx, cy, cz, radius


def project_point(point3d, fx, fy, cx, cy):

    X, Y, Z = point3d

    if Z <= 0:
        return None

    u = int(fx * X / Z + cx)
    v = int(fy * Y / Z + cy)

    return u, v