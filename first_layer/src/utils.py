import cv2


def convert_zed_image(frame):
    """
    Convert ZED RGBA image to OpenCV BGR format.
    """

    return cv2.cvtColor(
        frame,
        cv2.COLOR_BGRA2BGR
    )


def display_fps(frame, fps):

    cv2.putText(
        frame,
        f"FPS: {fps}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )

    return frame
