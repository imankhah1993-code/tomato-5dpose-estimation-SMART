from src.camera import ZEDCamera
from src.detector import TomatoDetector
from src.visualizer import Visualizer
from src.config import MODEL_PATH


def main():

    camera = ZEDCamera()
    detector = TomatoDetector(MODEL_PATH)
    visualizer = Visualizer()

    print("Press 'q' to exit")

    while True:

        frame = camera.get_frame()

        if frame is None:
            continue

        annotated = detector.detect(frame)

        annotated = visualizer.draw_fps(
            annotated,
            camera.get_fps()
        )

        visualizer.show(annotated)

        if visualizer.should_quit():
            break

    camera.close()
    visualizer.close()


if __name__ == "__main__":
    main()