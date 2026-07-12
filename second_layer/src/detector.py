from ultralytics import YOLO
from src.config import MODEL_PATH


class TomatoDetector:

    def __init__(self):
        self.model = YOLO(MODEL_PATH)

    def detect(self, image):
        return self.model(
            image,
            conf=0.4,
            imgsz=1280
        )[0]