#!/usr/bin/env python
import rospy
import intera_interface
from intera_interface import CHECK_VERSION

rospy.init_node('Home_neutral_shipping', anonymous = True)
rs = intera_interface.RobotEnable(CHECK_VERSION)
limb_mv = intera_interface.Limb('right')
head = intera_interface.Head()

init_state = rs.state().enabled
limb_mv.set_joint_position_speed(0.1)
current_pose = limb_mv.endpoint_pose() 
print (current_pose)

home_position = {'right_j6': 0.0, 'right_j5': 0.0, 'right_j4': 0.0, 'right_j3': 0.0, 'right_j2': 0.0, 'right_j1': -1.6, 'right_j0': -0.0}
shipping_position = {'right_j6' : 0.00, 'right_j5' : -1.57, 'right_j4' : 0.00, 'right_j3' : 2.79, 'right_j2' : 0.00, 'right_j1' : -2.79, 'right_j0' : 3.3161}

question = "What position do you want to go to n, h or s? "
chosen_position = raw_input(question).lower()

if chosen_position == "n":
    limb_mv.move_to_neutral()
    print (limb_mv.joint_angles())
    current_pose = limb_mv.endpoint_pose() 
    print current_pose 
    rospy.sleep(0.5)

elif chosen_position == "h":
    limb_mv.move_to_joint_positions(home_position)
    print (limb_mv.joint_angles())
    current_pose = limb_mv.endpoint_pose() 
    print current_pose 
    rospy.sleep(0.5)

elif chosen_position == "s":
    head.set_pan(-3.14)
    rospy.sleep(0.5)
    limb_mv.move_to_joint_positions(shipping_position)
    print (limb_mv.joint_angles())
    current_pose = limb_mv.endpoint_pose() 
    print current_pose 
    rospy.sleep(0.5)