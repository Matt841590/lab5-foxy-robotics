import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist   # ✅ FIXED IMPORT
from cv_bridge import CvBridge

from ultralytics import YOLO
import cv2
import numpy as np

from pydub import AudioSegment
from pydub.playback import play
from io import BytesIO


class YoloHumanDetectionNodeDepth(Node):
    def __init__(self):
        super().__init__('yolo_human_detection_depth')

        # read in audio
        self.audio = AudioSegment.from_file("/home/ubuntu/lab5-foxy-robotics/cv/cv/scream.mp3")

        self.played = False


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

        # Publisher to the wheels
        self.drive_publisher = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        # PD controller variables
        self.kp = 0.01

        self.get_logger().info("YOLO Human Detection Node Started")


    def depth_callback(self, msg):
        """Store latest depth frame"""
        try:
            depth_img = self.bridge.imgmsg_to_cv2(msg)
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

        # ✅ FIX: handle missing depth safely
        if self.depth_frame is None:
            self.get_logger().warn("No depth frame yet")
            cv2.imshow("YOLO + Depth", annotated)
            cv2.waitKey(1)
            return

        # Ensure detections exist
        if results.boxes is None or len(results.boxes) == 0:
            self.get_logger().warn("No detections")
            cv2.imshow("YOLO + Depth", annotated)
            cv2.waitKey(1)
            return

        h, w = frame.shape[:2]

        closest_box = None
        closest_depth = float('inf')
        closest_center = (0, 0)

        for box in results.boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)

            cx = int((x1 + x2) / 2)
            cy = int((y1 + y2) / 2)

            cx = np.clip(cx, 0, w - 1)
            cy = np.clip(cy, 0, h - 1)

            depth_value = self.depth_frame[cy, cx]

            if isinstance(depth_value, np.ndarray):
                depth_value = depth_value[0]

            # Skip invalid depth values
            if depth_value == 0 or np.isnan(depth_value):
                continue

            # Find closest object
            if depth_value < closest_depth:
                closest_depth = depth_value
                closest_box = (x1, y1, x2, y2)
                closest_center = (cx, cy)

        # If no valid depth found
        if closest_box is None:
            self.get_logger().warn("No valid depth for any detection")
            cv2.imshow("YOLO + Depth", annotated)
            cv2.waitKey(1)
            return

        # Draw ONLY the closest box
        x1, y1, x2, y2 = closest_box
        cx, cy = closest_center

        label = f"({cx}, {cy}) Depth: {closest_depth:.2f}" if isinstance(closest_depth, float) else f"({cx}, {cy}) Depth: {closest_depth}"

        cv2.rectangle(annotated, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.circle(annotated, (cx, cy), 5, (0, 0, 255), -1)

        cv2.putText(
            annotated,
            label,
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            2
        )

        self.get_logger().info(f"CLOSEST center: {cx},{cy} depth: {closest_depth}")

        # - publisher publishing drive commands
        twist = Twist()

        # forward speed (you can also make this depth-based later)
        if closest_depth < 1000:
            twist.linear.x = 0.0

            if self.played:
                self.played = True
                # Play
                play(self.audio)


        else:
            self.played = False
            twist.linear.x = self.kp * closest_depth

        # P-controller for steering
        error = (w // 2) - cx
        twist.angular.z = 0.002 * error

        self.drive_publisher.publish(twist)

        cv2.imshow("YOLO + Depth", annotated)
        cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=args)
    node = YoloHumanDetectionNodeDepth()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()