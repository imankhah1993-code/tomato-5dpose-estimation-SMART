import math
import cv2

from .utils import draw_vector


class PoseEstimator:

    def compute(self, geometry):

        vec = geometry["center3d"] - geometry["stem3d"]

        X, Y, Z = geometry["sphere_center"]

        yaw = math.degrees(math.atan2(vec[0], vec[2]))

        pitch = math.degrees(

            math.atan2(

                -vec[1],

                math.sqrt(vec[0] ** 2 + vec[2] ** 2)

            )

        )

        return {

            "x": X,
            "y": Y,
            "z": Z,
            "yaw": yaw,
            "pitch": pitch,
            "geometry": geometry

        }

    def draw(self, image, pose):

        g = pose["geometry"]

        draw_vector(image, g["center2d"], g["stem2d"])

        x, y = g["bbox_center"]

        cv2.putText(

            image,

            f"Yaw:{pose['yaw']:.1f}",

            (x + 10, y),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.5,

            (255,255,255),

            1

        )

        cv2.putText(

            image,

            f"Pitch:{pose['pitch']:.1f}",

            (x + 10, y + 20),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.5,

            (255,255,255),

            1

        )

        cv2.putText(

            image,

            f"X:{pose['x']:.2f}",

            (x + 10, y + 40),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.5,

            (0,255,255),

            1

        )

        cv2.putText(

            image,

            f"Y:{pose['y']:.2f}",

            (x + 10, y + 60),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.5,

            (0,255,255),

            1

        )

        cv2.putText(

            image,

            f"Z:{pose['z']:.2f}",

            (x + 10, y + 80),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.5,

            (0,255,255),

            1

        )