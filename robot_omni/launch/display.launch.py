import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    # 1. Định nghĩa các đường dẫn (Path)
    pkg_path = get_package_share_directory('robot_omni')
    
    # Đường dẫn đến thư mục chứa file .lua của bạn
    # Hệ thống sẽ tìm trong: install/robot_omni/share/robot_omni/config/
    cartographer_config_dir = os.path.join(pkg_path, 'config')
    
    # Tên file lua chính xác trong thư mục config của bạn
    configuration_basename = 'robot_omni_lds_2d.lua'

    # 2. Các tham số cấu hình
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation (Gazebo) clock if true'),

        # Node Cartographer (Xử lý SLAM)
        Node(
            package='cartographer_ros',
            executable='cartographer_node',
            name='cartographer_node',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time}],
            arguments=[
                '-configuration_directory', cartographer_config_dir,
                '-configuration_basename', configuration_basename
            ],
            remappings=[
                # Khớp với bridge_config.yaml (2 Lidar)
                ('scan_1', '/scan_front_raw'),
                ('scan_2', '/scan_rear_raw'),
                ('odom', '/mobile_base_controller/odometry'),
            ]),

        # Node Occupancy Grid (Chuyển submap thành bản đồ 2D cho RViz)
        Node(
        package='cartographer_ros',
        executable='cartographer_occupancy_grid_node',  # 👈 Jazzy dùng tên này
        name='occupancy_grid_node',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}],
        ),

        # Node RViz2
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            parameters=[{'use_sim_time': use_sim_time}],
            #arguments=['-d', os.path.join(pkg_path, 'rviz', 'robot_omni_cartographer.rviz')]
        ),
    ])
