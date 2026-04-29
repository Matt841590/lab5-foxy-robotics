to do library installs
# LOCAL
mkdir yolo_packages && cd yolo_packages
pip download ultralytics

scp -r yolo_packages user@remote:/tmp/

# REMOTE
cd /tmp/yolo_packages
pip install *.whl


ros2 topic pub /ros_robot_controller/bus_servo/set_position ros_robot_controller_msgs/msg/ServosPosition "{
  duration: 2.0,
  position: [
    {id: 1, position: 520},
    {id: 2, position: 600},
    {id: 3, position: 400},
    {id: 4, position: 300},
    {id: 5, position: 500}
  ]
}" --once

run bash to swap to bash

Presumably, everything is 0-1000.
DO NOT PUSH 0, EPECIALLY TO id 1
The ids are sorted bottom servo to top