from launch import LaunchDescription
from launch.actions import SetEnvironmentVariable, ExecuteProcess
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory
import os
from launch_ros.actions import Node

def generate_launch_description():

    # ✅ Dùng cho Python
    pkg = get_package_share_directory('robot_omni')

    urdf_file = os.path.join(pkg, 'urdf', 'omni_base.urdf')

    with open(urdf_file, 'r') as f:
        robot_description = f.read()

    # ✅ Dùng cho launch
    world_file = PathJoinSubstitution([
        FindPackageShare('robot_omni'),
        'worlds',
        'hospital_aws.world'
    ])

    model_path = os.path.expanduser(
        '~/ros2_ws/src/robot_omni/models'
    )

    return LaunchDescription([

        SetEnvironmentVariable(
            name='GZ_SIM_RESOURCE_PATH',
            value=f'{model_path}:${{GZ_SIM_RESOURCE_PATH}}'
        ),

        ExecuteProcess(
            cmd=['gz', 'sim', world_file],
            output='screen'
        ),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[
                {'robot_description': robot_description},
                {'use_sim_time': True}
            ],
            output='screen'
        ),

        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=[
                '-topic', 'robot_description',
                '-name', 'omni_base',
                '-z', '0.1',
                '-y', '1',
                '-x', '1'
            ],
            output='screen'
        ),
    ])