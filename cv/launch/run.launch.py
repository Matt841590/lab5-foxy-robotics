from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='cv',
            executable='yolo_depth_node',
        ),

        Node(
            package='control',
            executable='arm_node',
        ),
    ])