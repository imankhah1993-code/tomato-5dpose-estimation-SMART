import numpy as np
import pyzed.sl as sl
import cv2


def get_3d(point_cloud, x, y):

    err, point = point_cloud.get_value(int(x), int(y))

    if err != sl.ERROR_CODE.SUCCESS:
        return None

    X, Y, Z = point[:3]

    if np.isnan([X, Y, Z]).any():
        return None

    if np.isinf([X, Y, Z]).any():
        return None

    return np.array([X, Y, Z])


def draw_vector(img, start, end):

    cv2.arrowedLine(
        img,
        start,
        end,
        (0, 255, 255),
        2,
        tipLength=0.3,
    )