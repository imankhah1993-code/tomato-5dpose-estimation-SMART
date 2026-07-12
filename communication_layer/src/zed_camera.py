import pyzed.sl as sl
import cv2


class ZEDCamera:


    def __init__(self):

        self.zed = sl.Camera()

        params = sl.InitParameters()

        params.coordinate_units = sl.UNIT.METER
        params.depth_mode = sl.DEPTH_MODE.NEURAL


        status = self.zed.open(params)

        if status != sl.ERROR_CODE.SUCCESS:
            raise RuntimeError(
                f"ZED error {status}"
            )


        self.image = sl.Mat()
        self.point_cloud = sl.Mat()



    def get_frame(self):

        if self.zed.grab() != sl.ERROR_CODE.SUCCESS:
            return None,None


        self.zed.retrieve_image(
            self.image,
            sl.VIEW.LEFT
        )


        frame = self.image.get_data()

        frame=cv2.cvtColor(
            frame,
            cv2.COLOR_BGRA2BGR
        )


        self.zed.retrieve_measure(
            self.point_cloud,
            sl.MEASURE.XYZ
        )


        return frame,self.point_cloud



    def close(self):

        self.zed.close()