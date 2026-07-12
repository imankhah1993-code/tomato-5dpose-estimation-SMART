import cv2
import pyzed.sl as sl

from src.detector import TomatoDetector
from src.geometry import GeometryEstimator
from src.pose import PoseEstimator

# ---------------------------------------------------
# Initialize detector
# ---------------------------------------------------
detector = TomatoDetector("models/best.pt")

geometry = GeometryEstimator()
pose = PoseEstimator()

# ---------------------------------------------------
# Initialize ZED
# ---------------------------------------------------
zed = sl.Camera()

init_params = sl.InitParameters()
init_params.coordinate_units = sl.UNIT.METER
init_params.depth_mode = sl.DEPTH_MODE.NEURAL

if zed.open(init_params) != sl.ERROR_CODE.SUCCESS:
    exit()

image = sl.Mat()
point_cloud = sl.Mat()

print("Press q to quit")

while True:

    if zed.grab() != sl.ERROR_CODE.SUCCESS:
        continue

    zed.retrieve_image(image, sl.VIEW.LEFT)
    frame = image.get_data()

    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    zed.retrieve_measure(point_cloud, sl.MEASURE.XYZ)

    annotated, detections = detector.detect(frame)

    for det in detections:

        geometry_data = geometry.compute(det, point_cloud)

        if geometry_data is None:
            continue

        pose_data = pose.compute(geometry_data)

        geometry.draw(annotated, geometry_data)

        pose.draw(annotated, pose_data)

    cv2.imshow("Tomato Pose", annotated)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

zed.close()
cv2.destroyAllWindows()