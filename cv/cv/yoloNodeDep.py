import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from cv_bridge import CvBridge

from ultralytics import YOLO
import cv2
import numpy as np


class YoloHumanDetectionNodeDepth(Node):
    def __init__(self):
        super().__init__('yolo_human_detection_depth')

        # Load model
        self.model = YOLO("/home/ubuntu/YOLOv8-HumanDetection/best.pt")

        # Bridge
        self.bridge = CvBridge()

        # Latest depth frame storage
        self.depth_frame = None

        # RGB subscriber
        self.create_subscription(
            Image,
            '/depth_cam/rgb/image_raw',
            self.rgb_callback,
            10
        )

        # Depth subscriber
        self.create_subscription(
            Image,
            '/depth_cam/depth/image_raw',
            self.depth_callback,
            10
        )

        self.get_logger().info("YOLO Human Detection Node Started")

    def depth_callback(self, msg):
        """Store latest depth frame"""
        try:
            depth_img = self.bridge.imgmsg_to_cv2(msg)

            # Keep raw depth (handle both 16UC1 and 32FC1)
            self.depth_frame = depth_img

        except Exception as e:
            self.get_logger().error(f"Depth conversion error: {e}")

    def rgb_callback(self, msg):
        self.get_logger().info("Received RGB frame")

        # Convert RGB image
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        # Run YOLO
        results = self.model(frame, conf=0.3)[0]

        annotated = frame.copy()

        if self.depth_frame is None:
            self.get_logger().warn("No depth frame yet")
            return

        h, w = frame.shape[:2]

        for box in results.boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)

            # Compute center of bounding box
            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)

            # Clamp to image bounds
            cx = np.clip(cx, 0, w - 1)
            cy = np.clip(cy, 0, h - 1)

            # Get depth value at center pixel
            depth_value = self.depth_frame[cy, cx]

            # Handle depth formats
            if isinstance(depth_value, np.ndarray):
                depth_value = depth_value[0]

            label = f"Depth: {depth_value:.2f}" if np.issubdtype(type(depth_value), np.floating) else f"Depth: {depth_value}"

            # Draw bbox + center
            cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.circle(annotated, (cx, cy), 4, (0, 0, 255), -1)
            cv2.putText(
                annotated,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                2
            )

        cv2.imshow("YOLO + Depth", annotated)
        cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=args)
    node = YoloHumanDetectionNodeDepth()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()