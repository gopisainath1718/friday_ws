
# import os

# import launch_ros
# from launch_ros.actions import Node

# from launch import LaunchDescription
# from launch.actions import DeclareLaunchArgument
# from launch.substitutions import Command, LaunchConfiguration


# def generate_launch_description():

#     use_sim_time = LaunchConfiguration("use_sim_time")
#     description_path = LaunchConfiguration("description_path")

#     declare_use_sim_time = DeclareLaunchArgument("use_sim_time", default_value="false", description="Use simulation (Gazebo) clock if true")

#     pkg_share = launch_ros.substitutions.FindPackageShare(package="champ_description").find("champ_description")
#     default_model_path = os.path.join(pkg_share, "urdf/champ.urdf.xacro")

#     declare_description_path = DeclareLaunchArgument(name="description_path", default_value=default_model_path, description="Absolute path to robot urdf file")

#     robot_state_publisher_node = Node(
#         package="robot_state_publisher",
#         executable="robot_state_publisher",
        
#         parameters=[
#             {"robot_description": Command(["xacro ", description_path])},
#             {"use_tf_static": False},
#             {"publish_frequency": 200.0},
#             {"ignore_timestamp": True},
#             {'use_sim_time': use_sim_time}
#             ],
#         # remappings=(("robot_description", "robot_description")),
#     )

#     return LaunchDescription(
#         [
#             declare_description_path,
#             declare_use_sim_time,
#             robot_state_publisher_node,
#         ]
#     )
    
    
    
import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    use_sim_time = LaunchConfiguration("use_sim_time")

    # Declare sim time argument
    declare_use_sim_time = DeclareLaunchArgument(
        "use_sim_time",
        default_value="false",
        description="Use simulation time if true",
    )

    # Locate the package and URDF file
    pkg_share = FindPackageShare(package="champ_description").find("champ_description")
    urdf_path = os.path.join(pkg_share, "urdf", "friday.urdf")

    # Read the URDF file
    with open(urdf_path, "r") as urdf_file:
        robot_description_xml = urdf_file.read()

    # Robot State Publisher
    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[
            {"robot_description": robot_description_xml},
            {"use_tf_static": False},
            {"publish_frequency": 200.0},
            {"ignore_timestamp": True},
            {"use_sim_time": use_sim_time},
        ],
    )

    return LaunchDescription(
        [
            declare_use_sim_time,
            robot_state_publisher_node,
        ]
    )

