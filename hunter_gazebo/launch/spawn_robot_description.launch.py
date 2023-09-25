#!/usr/bin/python3
# -*- coding: utf-8 -*-
import random
from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription, RegisterEventHandler
from launch.event_handlers import OnProcessExit


# this is the function launch  system will look for

def generate_launch_description():

    # Position and orientation
    # [X, Y, Z]
    position = [0.0, 0.0, 0.2]
    # [Roll, Pitch, Yaw]
    orientation = [0.0, 0.0, 0.0]
    # Base Name or robot
    robot_base_name = "hunter"

    entity_name = robot_base_name+"-"+str(int(random.random()*100000))

    # Spawn ROBOT Set Gazebo
    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_entity',
        output='screen',
        arguments=['-entity',
                   entity_name,
                   '-x', str(position[0]), '-y', str(position[1]
                                                     ), '-z', str(position[2]),
                   '-R', str(orientation[0]), '-P', str(orientation[1]
                                                        ), '-Y', str(orientation[2]),
                   '-topic', '/robot_description'
                   ]
    )

    load_joint_state_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'joint_state_broadcaster'],
        output='screen'
    )

    load_ackermann_steering_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
             'ackermann_steering_controller'],
        output='screen'
    )

    # create and return launch description object
    return LaunchDescription(
        [
        RegisterEventHandler(
            event_handler=OnProcessExit(
            target_action=spawn_robot,
            on_exit=[load_joint_state_controller],
            )),
        RegisterEventHandler(
            event_handler=OnProcessExit(
            target_action=load_joint_state_controller,
            on_exit=[load_ackermann_steering_controller],
            )),
        spawn_robot
        ]
    )