import rclpy
from rclpy.node import Node
from ros_robot_controller_msgs.msg import ServosPosition, ServoPosition

class ArmControlNode(Node):
    def __init__(self):

        # - super init
        super().__init__("arm_control_node")

         # - boolean so it is sent once
        self.sent = False

        # - make arm publisher
        self.arm_publisher = self.create_publisher(
            ServosPosition,
            "/ros_robot_controller/bus_servo/set_position",
            10
        )
        
        # - make timer to wait and the publish the command
        self.initial_timer = self.create_timer(0.5, self.move_arm_up)


    # - function to publish "up" command 
    def move_arm_up(self):
        if self.sent:
            return

        # Wait until controller is connected
        if self.arm_publisher.get_subscription_count() == 0:
            self.get_logger().info("Waiting for servo controller...")
            return

        self.get_logger().info("Sending arm UP command")

        msg = ServosPosition()
        msg.duration = 2.0
        msg.position = [
            ServoPosition(id=1, position=500),
            ServoPosition(id=2, position=500),
            ServoPosition(id=3, position=500),
            ServoPosition(id=4, position=200),
            ServoPosition(id=5, position=500),
        ]

        self.arm_publisher.publish(msg)

        self.sent = True
        self.initial_timer.cancel()

    # - function to publish "down" command
    def move_arm_down(self):
        # - making the message
        down_arm_msg = ServosPosition()

        # - populating the duration field
        down_arm_msg.duration = 2.0

        # - populating the rest of the message field
        down_arm_msg.position = [
            ServoPosition(id=1, position=500),
            ServoPosition(id=2, position=700),
            ServoPosition(id=3, position=100),
            ServoPosition(id=4, position=300),
            ServoPosition(id=5, position=100),
        ]

        # - publishing the mesage
        self.arm_publisher.publish(down_arm_msg)

def main(args=None):
    rclpy.init(args=args)
    node = ArmControlNode()

    try:
        rclpy.spin(node)  # - stay alive indefinitely
    except KeyboardInterrupt:
        pass
    finally:
        # - Send undo command before shutting down
        node.move_arm_down()
        node.destroy_node()
        rclpy.shutdown()

