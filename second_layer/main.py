import cv2
import numpy as np

from src.camera import ZEDCamera
from src.detector import TomatoDetector
from src.geometry import fit_sphere, project_point
from src.visualization import draw_sphere
from src.config import *

camera = ZEDCamera()
detector = TomatoDetector()

while True:

    frame, pc = camera.grab()

    if frame is None:
        continue

    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    annotated = frame.copy()

    H, W, _ = pc.shape

    results = detector.detect(frame)

    for box in results.boxes:

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(W-1, x2)
        y2 = min(H-1, y2)

        pts = pc[y1:y2, x1:x2, :3].reshape(-1,3)

        pts = pts[np.isfinite(pts[:,2])]
        pts = pts[pts[:,2] > 0]

        if len(pts) < MIN_POINTS:
            continue

        median = np.median(pts[:,2])

        tomato = pts[np.abs(pts[:,2]-median) < DEPTH_THRESHOLD]

        if len(tomato) < MIN_TOMATO_POINTS:
            continue

        try:

            cx, cy, cz, r = fit_sphere(tomato)

            center = project_point(
                (cx,cy,cz),
                camera.fx,
                camera.fy,
                camera.cx,
                camera.cy
            )

            if center is None:
                continue

            radius_px = int(r * camera.fx / cz)

            annotated = draw_sphere(
                annotated,
                center,
                radius_px,
                cz
            )

        except Exception:
            pass

    cv2.putText(
        annotated,
        f"FPS: {camera.fps()}",
        (20,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,0,255),
        2
    )

    cv2.imshow("Tomato Sphere Fitting", annotated)

    if cv2.waitKey(1) == ord("q"):
        break

camera.close()
cv2.destroyAllWindows()
