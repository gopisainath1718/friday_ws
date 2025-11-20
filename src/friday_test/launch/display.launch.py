#!/usr/bin/env python3

import os
from launch import LaunchDescription
from launch_ros.actions import Node
import launch_ros
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_share = launch_ros.substitutions.FindPackageShare(package="champ_description").find("champ_description")
    urdf_path = os.path.join(pkg_share, 'urdf/friday.urdf')

    with open(urdf_path, 'r') as f:
        robot_description = f.read()

    robot_state_publisher_node = Node(
            package = 'robot_state_publisher',
            executable = 'robot_state_publisher',
            name = 'robot_state_publishe',
            output = 'screen',
            parameters = [{'robot_description': robot_description},
                          {"publish_frequency": 200.0}],
            )

    joint_state_publisher_gui_node = Node(
            package = 'joint_state_publisher_gui',
            executable ='joint_state_publisher_gui',
            name = 'joint_state_publisher_gui',
            output = 'screen',
            )
    rviz2_node = Node(
            package = 'rviz2',
            executable ='rviz2',
            name = 'rviz2',
            )

    return LaunchDescription([robot_state_publisher_node, joint_state_publisher_gui_node, rviz2_node])
