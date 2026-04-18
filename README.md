# Omni Robot Navigation (ROS2)

Members:
23134049 - Le Thanh Sang

23134002 - Bui Huynh Phuong Anh

23134054 - Pham Hoang Thong

23134058 - Vo Dai Tri



note: Before using, please update the file paths accordingly


## Setup

Copy the following folders into your workspace (place them inside ~/ros2_ws/src):
    nav2_simple_navigation
    robot_omni

---

## Run Simulation

### 1. Start Gazebo (Robot Simulation)

Open the **first terminal**:

cd ~/ros2_ws/src
colcon build
source install/setup.bash
ros2 launch robot_omni gazebo_control.launch.py

Note:
If the robot does not appear or Gazebo runs incorrectly, run the last command again. This may happen due to hardware performance issues.

---

### 2. Start Navigation (Nav2 + RViz)

Open the **second terminal**:

cd ~/ros2_ws/src
colcon build
source install/setup.bash
ros2 launch nav2_simple_navigation nav2_control_withmap.launch.py use_sim_time:=true

Note:
If the map does not appear in RViz, rerun the last command. This is usually due to RViz initialization delay.

Important (Localization Step):
In RViz, use "2D Pose Estimate"
Click on the map to set the initial position of the robot
Drag to set the orientation (heading)
-->This step is required so the robot knows its starting position before navigation.

---

### 3. Run Control Node

Open the **third terminal**:

cd ~/ros2_ws/src
colcon build
source install/setup.bash
ros2 run nav2_simple_navigation phong_muon_di

Usage:
Enter the room number (1 → 18) from the keyboard
The robot will navigate to the selected room
Enter `q` to finish selecting rooms

Notes:
Room indices are limited from 1 to 18
Duplicate room selections are not allowed
