# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 12:52:54 2025

@author: Rohan
"""

import numpy as np
import pandas as pd
import rospy
from geometry_msgs.msg import Twist, Vector3

pub = None
current_yaw = None
target_angle = None

def yaw_callback(msg):
    global current_yaw, target_angle
    current_yaw = msg.z
    if target_angle is not None:
        angular_velocity = compute_turn_velocity(target_angle)
        twist_msg = Twist()
        twist_msg.angular.z = angular_velocity
        pub.publish(twist_msg)


def fetch_target_position():
    data = pd.read_csv("FilteredData.csv")
    locations, object_names = np.array(data.iloc[:, 0]), np.array(data.iloc[:, 1])
    total_objects = len(object_names)
    print(object_names)
    print(f"Total objects found: {total_objects}")

    requested_item = input("Enter the object name:\n")
    item_locations = [location for i, location in enumerate(locations) if object_names[i] == requested_item]
    
    average_location = sum(item_locations) / len(item_locations) if item_locations else 0
    print(f"Average location: {average_location}")
    return average_location


def compute_turn_velocity(target_angle):
    global current_yaw
    angle_diff = target_angle - current_yaw
    if angle_diff >= 0.11:
        velocity = 0.25
    elif angle_diff <= -0.11:
        velocity = -0.25
    else:
        velocity = 0
    print(f"Yaw error: {angle_diff}")
    return velocity


def main():
    global pub, target_angle
    rospy.init_node('robot_orientation', anonymous=True)
    target_angle = fetch_target_position()

    rospy.Subscriber("/rpy_angles", Vector3, yaw_callback)
    pub = rospy.Publisher("/robot/commands/velocity", Twist, queue_size=10)
    
    rospy.spin()


if __name__ == '__main__':
    main()
