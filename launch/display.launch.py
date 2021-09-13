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
        launch.actions.DeclareLaunchArgument(
            name='gui',
            default_value='True',
            description='Use joint_state_publisher_gui.'
            ),
        launch.actions.DeclareLaunchArgument(
            name='head',
            default_value='True',
            description='Add the head in Reachy configuration.',
            ),
        launch.actions.DeclareLaunchArgument(
            name='right_arm',
            default_value='True',
            description='Add the right arm in Reachy configuration.',
            ),
        launch.actions.DeclareLaunchArgument(
            name='left_arm',
            default_value='True',
            description='Add the left arm in Reachy configuration.',
            ),
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            condition=launch.conditions.UnlessCondition(LaunchConfiguration('gui')),
        ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            condition=launch.conditions.IfCondition(LaunchConfiguration('gui')),
        ),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{
                'robot_description': Command([
                    'xacro ',
                    xacro_path,
                    ' head:=',
                    LaunchConfiguration('head'),
                    ' right_arm:=',
                    LaunchConfiguration('right_arm'),
                    ' left_arm:=',
                    LaunchConfiguration('left_arm'),
                ])}],
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            arguments=['-d'+rviz_config_path],
        ),
    ])
