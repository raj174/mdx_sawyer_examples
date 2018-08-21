#!/usr/bin/env python
import rospy
import intera_interface
from intera_interface import CHECK_VERSION

rospy.init_node('fk_ik')
rs = intera_interface.RobotEnable(CHECK_VERSION)
limb = intera_interface.Limb('right')

init_state = rs.state().enabled
limb.set_joint_position_speed(0.1)
limb.move_to_neutral_position()
current_position = limb.endpoint_pose()

go_to_position = Pose()
go_to_position.position.x = current_pose['position'].x
go_to_position.position.y = current_pose['position'].y + 0.5
go_to_position.position.z = current_pose['position'].z 
go_to_position.orientation.x = current_pose['orientation'].x
go_to_position.orientation.y = current_pose['orientation'].y
go_to_position.orientation.z = current_pose['orientation'].z
go_to_position.orientation.w = current_pose['orientation'].w

joint_angles = limb.ik_request(go_to_position, right_hand)
limb.move_to_joint_positions(joint_angles)
print limb.endpoint_pose()



''' terminal part'''
rosrun  intera_interface enable_robot.py -e

python

import rospy
import intera_interface

rospy.init_node('fk_ik_eg')
limb = intera_interface.Limb('right')

check about cartesin pose 
print limb.joint_angles_to_cartesian_pose(joint_angles)
print limb.endpoint_pose()

(lets say i want to move 50 cm horizontally)
limb.move_to_neutral_position()
angles = limb.joint_angles()
print angles
limb.move_to_joint_positions(copy and change angles)
limb.move_to_joint_positions(copy and change angles)
limb.move_to_joint_positions(copy and change angles)

now lets see the location
print limb.endpoint_pose()

after several tries you might get it to move more or less to the position wanted
limb.move_to_neutral_position()
current_position = limb.endpoint_pose()
current_position['position'].y = current_position['position'].y + 0.5
joint_angles = limb.ik_request(current_position, right_hand)
limb.move_to_joint_positions(joint_angles)
print limb.endpoint_pose()