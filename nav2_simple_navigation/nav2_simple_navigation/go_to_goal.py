import rclpy
from nav2_simple_commander.robot_navigator import BasicNavigator
from geometry_msgs.msg import PoseStamped
import math

def main():
    rclpy.init()
    nav = BasicNavigator()

    # Wait for Nav2
    nav.waitUntilNav2Active(localizer='bt_navigator')


    goal_pose = PoseStamped()
    goal_pose.header.frame_id = 'map'
    goal_pose.header.stamp = nav.get_clock().now().to_msg()
    goal_pose.pose.position.x = 5.0
    goal_pose.pose.position.y = -5.0
    
    # Simple orientation: face the next point
    yaw = -(math.pi)/2 
    goal_pose.pose.orientation.z = math.sin(yaw / 2)
    goal_pose.pose.orientation.w = math.cos(yaw / 2)
    # Use goToPose instead of followWaypoints
    nav.goToPose(goal_pose)

    # Wait until the robot reaches this specific point
    while not nav.isTaskComplete():
        pass 
                   
    rclpy.shutdown()