import os
from ament_index_python.packages import get_package_share_directory
import launch
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import Command, LaunchConfiguration


def generate_launch_description():

    xacro_path = os.path.join(
        get_package_share_directory('reachy_description_ros2'),
        'urdf/reachy.URDF.xacro',
    )

    rviz_config_path = os.path.join(
        get_package_share_directory('reachy_description_ros2'),
        'rviz/reachy.rviz',
    )

    return LaunchDescription([

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{
                'robot_description': Command([
                    'xacro ',
                    xacro_path
                ])}],
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d'+rviz_config_path],
        ),
    ])
