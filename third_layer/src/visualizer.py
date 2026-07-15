import cv2


class Visualizer:

    WINDOW_NAME = "ZED Tomato Detection"

    def draw_fps(self, frame, fps):

        cv2.putText(
            frame,
            f"FPS: {fps}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2,
        )

        return frame

    def show(self, frame):
        cv2.imshow(self.WINDOW_NAME, frame)

    def should_quit(self):
        return cv2.waitKey(1) & 0xFF == ord("q")

    def close(self):
        cv2.destroyAllWindows()