import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from std_srvs.srv import Trigger


from .zed_camera import ZEDCamera
from .detector import TomatoDetector
from .geometry import GeometryEstimator
from .pose import PoseEstimator



class TomatoVisionNode(Node):


    def __init__(self):

        super().__init__(
            "tomato_vision_node"
        )


        self.declare_parameter(
            "model_path",
            "models/best.pt"
        )


        model=self.get_parameter(
            "model_path"
        ).value



        self.camera=ZEDCamera()

        self.detector=TomatoDetector(model)

        self.geometry=GeometryEstimator()

        self.pose=PoseEstimator()



        self.bridge=CvBridge()



        self.image_pub=self.create_publisher(
            Image,
            "tomato/image",
            10
        )


        self.next_srv=self.create_service(
            Trigger,
            "tomato/next",
            self.next_callback
        )


        self.reset_srv=self.create_service(
            Trigger,
            "tomato/reset",
            self.reset_callback
        )


        self.timer=self.create_timer(
            0.1,
            self.process
        )


        self.index=0


    def process(self):


        frame,pc=self.camera.get_frame()


        if frame is None:
            return



        detections,img=(
            self.detector.detect(frame)
        )


        for det in detections:


            geo=self.geometry.compute(
                det,
                pc
            )


            if geo is None:
                continue



            pose=self.pose.compute(
                geo
            )


            self.get_logger().info(
                str(pose)
            )



        msg=self.bridge.cv2_to_imgmsg(
            img,
            "bgr8"
        )

        self.image_pub.publish(msg)



    def next_callback(
        self,
        req,
        res
    ):

        self.index+=1

        res.success=True
        res.message=str(self.index)

        return res



    def reset_callback(
        self,
        req,
        res
    ):

        self.index=0

        res.success=True
        res.message="reset"

        return res



    def destroy_node(self):

        self.camera.close()

        super().destroy_node()