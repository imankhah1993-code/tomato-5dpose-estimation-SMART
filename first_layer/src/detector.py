from ultralytics import YOLO


class YOLODetector:
    """
    YOLO object detection wrapper.
    """

    def __init__(
        self,
        model_path,
        confidence=0.4,
        image_size=1280
    ):

        self.model = YOLO(model_path)

        self.confidence = confidence
        self.image_size = image_size


    def predict(self, frame):

        results = self.model(
            frame,
            conf=self.confidence,
            imgsz=self.image_size
        )

        return results[0]


    def draw_results(self, result):

        return result.plot(
            labels=False
        )
