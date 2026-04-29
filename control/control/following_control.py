import rclpy
from rclpy.node import Node

class FollowingControlNode(Node):
    def __init__(self):
        super().__init__("following_control_node")
