import pyzed.sl as sl


class ZEDCamera:
    """
    Wrapper class for ZED camera operations.
    """

    def __init__(self):
        self.zed = sl.Camera()

        init_params = sl.InitParameters()
        init_params.coordinate_units = sl.UNIT.METER
        init_params.sdk_verbose = 0

        status = self.zed.open(init_params)

        if status != sl.ERROR_CODE.SUCCESS:
            raise RuntimeError(f"Failed to open ZED camera: {status}")

        self.image = sl.Mat()

    def get_frame(self):
        """
        Capture and return the left camera image.
        """

        if self.zed.grab() == sl.ERROR_CODE.SUCCESS:

            self.zed.retrieve_image(
                self.image,
                sl.VIEW.LEFT
            )

            frame = self.image.get_data()

            return frame

        return None

    def get_fps(self):
        return int(self.zed.get_current_fps())

    def close(self):
        self.zed.close()
