import launch
from launch.substitutions import Command, LaunchConfiguration
import launch_ros
import os

packageName='robotic_arm'

urdfRelativePath='urdf/robotic_arm.urdf'

rvizRelativePath='config/config.rviz'

def generate_launch_description():
    pkgPath = launch_ros.substitutions.FindPackageShare(package=packageName).find(packageName)
    urdfModelPath = os.path.join(pkgPath,urdfRelativePath)
    rvizConfigPath = os.path.join(pkgPath, rvizRelativePath)

    print(urdfModelPath)

    print(urdfModelPath)

    with open(urdfModelPath, 'r') as infp:
        robot_desc = infp.read()

        params = {'robot_description': robot_desc}

        robot_state_publisher_node = launch_ros.actions.Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[params],
            arguments=[urdfModelPath]
        )

        joint_state_publisher_gui_node = launch_ros.actions.Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui',
            name='joint_state_publisher_gui',
            arguments=[urdfModelPath],
            condition=launch.conditions.IfCondition(LaunchConfiguration('gui'))
        )

        rviz_node = launch_ros.actions.Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d', rvizConfigPath]

        )

        return launch.LaunchDescription([
            launch.actions.DeclareLaunchArgument(name='gui', default_value='True', description='This ia flag for joint_state_publisher_gui'),
            robot_state_publisher_node,
            joint_state_publisher_gui_node,
            rviz_node,
        ])
