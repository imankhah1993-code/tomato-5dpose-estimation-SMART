import numpy as np
import cv2

from .utils import get_3d


class GeometryEstimator:

    def compute(self, det, point_cloud):

        x1, y1, x2, y2 = det["box"]

        stem = det["stem"]

        stem_x, stem_y = stem

        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2

        dx = cx - stem_x
        dy = cy - stem_y

        dist = np.hypot(dx, dy)

        if dist == 0:
            return None

        ux = dx / dist
        uy = dy / dist

        radius = min(x2 - x1, y2 - y1) / 2

        center_x = stem_x + ux * radius
        center_y = stem_y + uy * radius

        stem3d = get_3d(point_cloud, stem_x, stem_y)
        center3d = get_3d(point_cloud, center_x, center_y)
        sphere3d = get_3d(point_cloud, cx, cy)

        if stem3d is None:
            return None

        if center3d is None:
            return None

        if sphere3d is None:
            return None

        return {

            "stem2d": (int(stem_x), int(stem_y)),
            "center2d": (int(center_x), int(center_y)),
            "bbox_center": (int(cx), int(cy)),
            "stem3d": stem3d,
            "center3d": center3d,
            "sphere_center": sphere3d,
            "diameter": radius * 2

        }

    def draw(self, image, data):

        cv2.circle(image, data["center2d"], 6, (0,255,0), -1)

        cv2.circle(image, data["stem2d"], 6, (0,255,255), -1)

        cv2.circle(image, data["bbox_center"], 6, (255,0,255), -1)