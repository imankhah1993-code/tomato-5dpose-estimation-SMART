import rclpy

from src.ros_node import TomatoVisionNode


def main(args=None):

    rclpy.init(args=args)

    node = TomatoVisionNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()