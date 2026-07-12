import pyzed.sl as sl


class ZEDCamera:

    def __init__(self):

        self.zed = sl.Camera()

        params = sl.InitParameters()
        params.coordinate_units = sl.UNIT.METER
        params.depth_mode = sl.DEPTH_MODE.NEURAL

        if self.zed.open(params) != sl.ERROR_CODE.SUCCESS:
            raise RuntimeError("Cannot open ZED camera")

        self.runtime = sl.RuntimeParameters()

        self.image = sl.Mat()
        self.point_cloud = sl.Mat()

        calib = self.zed.get_camera_information()\
            .camera_configuration\
            .calibration_parameters.left_cam

        self.fx = calib.fx
        self.fy = calib.fy
        self.cx = calib.cx
        self.cy = calib.cy

    def grab(self):

        if self.zed.grab(self.runtime) != sl.ERROR_CODE.SUCCESS:
            return None, None

        self.zed.retrieve_image(self.image, sl.VIEW.LEFT)
        self.zed.retrieve_measure(self.point_cloud, sl.MEASURE.XYZ)

        return self.image.get_data(), self.point_cloud.get_data()

    def fps(self):
        return int(self.zed.get_current_fps())

    def close(self):
        self.zed.close()