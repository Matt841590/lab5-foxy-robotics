# lab5-foxy-robotics - Robot 12!

Manual Pages: https://docs.hiwonder.com/projects/JetRover/en/jetson-orin-nano/docs/1.Quick_Start_Guide.html

Our robot's IP(?): 192.168.149.1 (we got this via NoMachine)

Startup + Connection Procedure (using NoMachine):
-turn robot on (switch is the silver button on the chassis)
-connect to hotspot (working is HW25029764, pw: hiwonder)
  - TODO: find a way to change this to HW12 or something? 
-open your NoMachine client (install from https://www.nomachine.com/)
-select your client from the listed, login (un:ubuntu, pw: ubuntu)
  - Note: You can only hvae one client connected!
  - Note: You have a couple seconds latency(?)
-You now should have windowed access!

Startup + conneciton Procedure (ssh)
-turn robot on (switch is the silver button on the chassis)
-connect to hotspot (working is HW25029764, pw: hiwonder)
  - TODO: find a way to change this to HW12 or something?
-open a command line interface (powershell work on windows, bash on linux)
-run the command "ssh ubuntu@<your_ip>" and when asked for the password enter "ubuntu"
-You are now shelled in!


To get into ROS2 Workspace
-cd into "ros2_workspace" from