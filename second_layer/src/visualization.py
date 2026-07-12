import cv2
from src.config import ALPHA


def draw_sphere(image, center, radius, depth):

    overlay = image.copy()

    cv2.circle(image, center, radius, (0,255,255),3)
    cv2.circle(image, center, 5, (0,0,255),-1)

    cv2.circle(overlay, center, radius, (255,0,0),-1)

    image = cv2.addWeighted(
        overlay,
        ALPHA,
        image,
        1-ALPHA,
        0
    )

    cv2.putText(
        image,
        f"R={radius}",
        (center[0]-40, center[1]-radius-10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0,255,255),
        2
    )

    cv2.putText(
        image,
        f"Z={depth:.2f}m",
        (center[0]-40, center[1]+radius+25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255,255,255),
        2
    )

    return image