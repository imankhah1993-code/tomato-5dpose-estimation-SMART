import cv2

from src.camera import ZEDCamera
from src.detector import YOLODetector
from src.utils import (
    convert_zed_image,
    display_fps
)


MODEL_PATH = "models/best.pt"


def main():

    print("Starting ZED YOLO Tomato Detection...")

    camera = ZEDCamera()

    detector = YOLODetector(
        model_path=MODEL_PATH,
        confidence=0.4,
        image_size=1280
    )

    print("Press 'q' to exit")


    try:

        while True:

            frame = camera.get_frame()

            if frame is None:
                continue


            frame = convert_zed_image(frame)


            result = detector.predict(frame)


            output = detector.draw_results(result)


            output = display_fps(
                output,
                camera.get_fps()
            )


            cv2.imshow(
                "ZED Tomato Detection + Keypoints",
                output
            )


            if cv2.waitKey(1) & 0xFF == ord("q"):
                break


    finally:

        camera.close()
        cv2.destroyAllWindows()

        print("Shutdown complete.")



if __name__ == "__main__":
    main()
