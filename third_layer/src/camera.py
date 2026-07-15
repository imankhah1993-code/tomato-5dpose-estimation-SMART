import cv2
import pyzed.sl as sl


class ZEDCamera:

    def __init__(self):

        self.zed = sl.Camera()

        init = sl.InitParameters()
        init.coordinate_units = sl.UNIT.METER
        init.sdk_verbose = 1

        status = self.zed.open(init)

        if status != sl.ERROR_CODE.SUCCESS:
            raise RuntimeError(f"Failed to open ZED camera: {status}")

        self.image = sl.Mat()

    def get_frame(self):

        if self.zed.grab() != sl.ERROR_CODE.SUCCESS:
            return None

        self.zed.retrieve_image(self.image, sl.VIEW.LEFT)

        frame = self.image.get_data()

        return cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

    def get_fps(self):
        return int(self.zed.get_current_fps())

    def close(self):
        self.zed.close()