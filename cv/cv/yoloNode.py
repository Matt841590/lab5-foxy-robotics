import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from cv_bridge import CvBridge

from ultralytics import YOLO
import cv2


class YoloHumanDetectionNode(Node):
    def __init__(self):
        super().__init__('yolo_human_detection')

        # Load model
        self.model = YOLO("/home/ubuntu/YOLOv8-HumanDetection/best.pt")

        # Bridge between ROS and OpenCV
        self.bridge = CvBridge()

        # Subscribe to camera topic
        self.subscription = self.create_subscription(
            Image,
            '/depth_cam/rgb/image_raw',   # <-- change if needed
            self.image_callback,
            10
        )

        self.get_logger().info("YOLO Human Detection Node Started")

    def image_callback(self, msg):
        # Convert ROS image → OpenCV image
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        # Run YOLO
        results = self.model(frame, conf=0.3)

        # Draw detections
        annotated = results[0].plot()

        # Show result
        cv2.imshow("YOLO Detection", annotated)
        cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=args)
    node = YoloHumanDetectionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()