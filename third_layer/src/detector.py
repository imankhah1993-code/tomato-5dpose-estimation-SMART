import cv2
from ultralytics import YOLO

from src.config import (
    CONFIDENCE,
    IMAGE_SIZE,
    STEM_KEYPOINT
)


class TomatoDetector:

    def __init__(self, model_path):

        self.model = YOLO(model_path)

    def detect(self, frame):

        results = self.model(
            frame,
            conf=CONFIDENCE,
            imgsz=IMAGE_SIZE
        )

        r = results[0]

        annotated = r.plot(labels=False)

        if r.boxes is None or r.keypoints is None:
            return annotated

        boxes = r.boxes.xyxy.cpu().numpy()
        keypoints = r.keypoints.xy.cpu().numpy()

        for box, kp in zip(boxes, keypoints):

            x1, y1, x2, y2 = box

            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)

            if len(kp) <= STEM_KEYPOINT:
                continue

            stem_x, stem_y = kp[STEM_KEYPOINT].astype(int)

            cv2.circle(annotated, (cx, cy), 5, (255, 0, 0), -1)
            cv2.circle(annotated, (stem_x, stem_y), 5, (0, 0, 255), -1)

            cv2.arrowedLine(
                annotated,
                (cx, cy),
                (stem_x, stem_y),
                (0, 255, 0),
                2,
                tipLength=0.2,
            )

        return annotated