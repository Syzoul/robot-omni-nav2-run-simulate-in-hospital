from launch import LaunchDescription
from launch.actions import TimerAction
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():

    # Get package path
    pkg_share = get_package_share_directory('nav2_simple_navigation')
    # robot_omni = get_package_share_directory('robot_omni')
    # map_yaml_file = os.path.join(robot_omni, 'map', 'my_map.yaml')

    # Config files
    ekf_config = os.path.join(pkg_share, 'config', 'ekf.yaml')
    nav2_config = os.path.join(pkg_share, 'config', 'nav2_params_hospital_omni_robot.yaml')

    # -------------------------
    # EKF node
    # -------------------------
    ekf_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[ekf_config, {'use_sim_time': True}]
    )

    # -------------------------
    # Nav2 nodes
    # -------------------------
    planner_node = Node(
        package='nav2_planner',
        executable='planner_server',
        name='planner_server',
        output='screen',
        parameters=[nav2_config]
    )
    map_server = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        output='screen',
        parameters=[nav2_config],
    )
    delayed_map_server = TimerAction(
        period= 5.0,
        actions=[map_server]
    )
    amcl = Node(
        package='nav2_amcl',
        executable='amcl',
        name='amcl',
        output='screen',
        parameters=[nav2_config],
    )

    controller_node = Node(
        package='nav2_controller',
        executable='controller_server',
        name='controller_server',
        output='screen',
        parameters=[nav2_config],
        remappings=[('/cmd_vel', '/mobile_base_controller/reference')]
    )

    recoveries_node = Node(
        package='nav2_behaviors',
        executable='behavior_server',
        name='recoveries_server',
        output='screen',
        parameters=[nav2_config]
    )

    bt_navigator_node = Node(
        package='nav2_bt_navigator',
        executable='bt_navigator',
        name='bt_navigator',
        output='screen',
        parameters=[nav2_config]
    )

    nav2_behaviors_node =Node(
        package='nav2_behaviors',
        executable='behavior_server',
        name='behavior_server',
        output='screen',
        parameters=[nav2_config],
        remappings=[('/cmd_vel', '/mobile_base_controller/reference')]

    )

    lifecycle_manager_node = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_navigation',
        output='screen',
        parameters=[{
            'use_sim_time': True,
            'autostart': True,
            'node_names': [
                'map_server',
                'amcl',
                'planner_server',
                'controller_server',
                'recoveries_server',
                'bt_navigator',
                'behavior_server',
            ],

            'bond_timeout': 10.0,

            'attempt_respawn_reconnection': True,
            'bond_respawn_max_duration': 10.0
        }]
    )
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        parameters=[{'use_sim_time': True}],
        output='screen'
    )
    

    return LaunchDescription([
        ekf_node,
        delayed_map_server,
        amcl,
        planner_node,
        controller_node,
        recoveries_node,
        bt_navigator_node,
        nav2_behaviors_node,
        lifecycle_manager_node,
        rviz,
    ])