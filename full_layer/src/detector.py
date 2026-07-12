import numpy as np
from ultralytics import YOLO


class TomatoDetector:

    def __init__(self, model_path):

        self.model = YOLO(model_path)

    def detect(self, frame):

        results = self.model(frame, conf=0.4, imgsz=1280)

        annotated = results[0].plot(labels=False)

        detections = []

        r = results[0]

        if r.keypoints is None:
            return annotated, detections

        boxes = r.boxes.xyxy.cpu().numpy()
        keypoints = r.keypoints.xy.cpu().numpy()

        for box, kp in zip(boxes, keypoints):

            detections.append({

                "box": box,
                "stem": kp[0]

            })

        return annotated, detections