#!/usr/bin/env python
import rospy
import intera_interface
from intera_interface import CHECK_VERSION

from geometry_msgs.msg import (
    PoseStamped,
    Pose,
    Point,
    Quaternion,
)

rospy.init_node('fk_ik')
rs = intera_interface.RobotEnable(CHECK_VERSION)
limb = intera_interface.Limb('right')

rs.enable
limb.set_joint_position_speed(0.1)
limb.move_to_neutral()
current_pose = limb.endpoint_pose()
go_to_position = Pose()
go_to_position.position.x = current_pose['position'].x
go_to_position.position.y = current_pose['position'].y + 0.5
go_to_position.position.z = current_pose['position'].z 
go_to_position.orientation.x = current_pose['orientation'].x
go_to_position.orientation.y = current_pose['orientation'].y
go_to_position.orientation.z = current_pose['orientation'].z
go_to_position.orientation.w = current_pose['orientation'].w


joint_angles = limb.ik_request(go_to_position, 'right_hand')
limb.move_to_joint_positions(joint_angles)
print limb.endpoint_pose()




