#!/usr/bin/env python

"""
Modified Joint Position Example: keyboard
Has feature to change the increment value
"""
import argparse

import rospy

import intera_interface
import intera_external_devices

from intera_interface import CHECK_VERSION

def constrain(self, x, min_x, max_x):
        return min(max_x, max(x, min_x))

def map_keyboard(side):
    limb = intera_interface.Limb(side)

    try:
        gripper = intera_interface.Gripper(side + '_gripper')
    except:
        has_gripper = False
        rospy.loginfo("The electric gripper is not detected on the robot.")
    else:
        has_gripper = True

    joints = limb.joint_names()
    increment = 0.1

    def set_j(limb, joint_name, delta):
        current_position = limb.joint_angle(joint_name)
        joint_command = {joint_name: current_position + delta}
        limb.set_joint_positions(joint_command)

    def set_g(action):
        if has_gripper:
            if action == "close":
                gripper.close()
            elif action == "open":
                gripper.open()
            elif action == "calibrate":
                gripper.calibrate()

    def set_bindings():
        bindings = {
            '1': (set_j, [limb, joints[0], increment], joints[0]+" increase"),
            'q': (set_j, [limb, joints[0], -increment], joints[0]+" decrease"),
            '2': (set_j, [limb, joints[1], increment], joints[1]+" increase"),
            'w': (set_j, [limb, joints[1], -increment], joints[1]+" decrease"),
            '3': (set_j, [limb, joints[2], increment], joints[2]+" increase"),
            'e': (set_j, [limb, joints[2], -increment], joints[2]+" decrease"),
            '4': (set_j, [limb, joints[3], increment], joints[3]+" increase"),
            'r': (set_j, [limb, joints[3], -increment], joints[3]+" decrease"),
            '5': (set_j, [limb, joints[4], increment], joints[4]+" increase"),
            't': (set_j, [limb, joints[4], -increment], joints[4]+" decrease"),
            '6': (set_j, [limb, joints[5], increment], joints[5]+" increase"),
            'y': (set_j, [limb, joints[5], -increment], joints[5]+" decrease"),
            '7': (set_j, [limb, joints[6], increment], joints[6]+" increase"),
            'u': (set_j, [limb, joints[6], -increment], joints[6]+" decrease")
         }
        if has_gripper:
            bindings.update({
            '8': (set_g, "close", side+" gripper close"),
            'i': (set_g, "open", side+" gripper open"),
            '9': (set_g, "calibrate", side+" gripper calibrate")
            })

    set_bindings()
    done = False
    print("Controlling joints. Press ? for help, Esc to quit.")
    while not done and not rospy.is_shutdown():
        c = intera_external_devices.getch()
        if c:
            #catch Esc or ctrl-c
            if c in ['\x1b', '\x03']:
                done = True
                rospy.signal_shutdown("Example finished.")
            elif c in bindings:
                cmd = bindings[c]
                if c == '8' or c == 'i' or c == '9':
                    cmd[0](cmd[1])
                    print("command: %s" % (cmd[2],))
                else:
                    #expand binding to something like "set_j(right, 'j0', 0.1)"
                    cmd[0](*cmd[1])
                    print("command: %s" % (cmd[2],))
            elif c == 'n':
                increment_val = "Increment value (0.0 : 0.4) : "
                increment = constrain(float(raw_input(increment_val).lower()),0.0,0.4)
                set_bindings()
            else:
                print("key bindings: ")
                print("  Esc: Quit")
                print("  ?: Help")
                print("  n: Change increment value")
                for key, val in sorted(bindings.items(),
                                       key=lambda x: x[1][2]):
                    print("  %s: %s" % (key, val[2]))

def main():
    """RSDK Joint Position Example: Keyboard Control

    Use your dev machine's keyboard to control joint positions.

    Each key corresponds to increasing or decreasing the angle
    of a joint on Sawyer's arm. The increasing and descreasing
    are represented by number key and letter key next to the number.
    """
    epilog = """
See help inside the example with the '?' key for key bindings.
    """
    rp = intera_interface.RobotParams()
    valid_limbs = rp.get_limb_names()
    if not valid_limbs:
        rp.log_message(("Cannot detect any limb parameters on this robot. "
                        "Exiting."), "ERROR")
        return
    arg_fmt = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=arg_fmt,
                                     description=main.__doc__,
                                     epilog=epilog)
    parser.add_argument(
        "-l", "--limb", dest="limb", default=valid_limbs[0],
        choices=valid_limbs,
        help="Limb on which to run the joint position keyboard example"
    )
    args = parser.parse_args(rospy.myargv()[1:])

    print("Initializing node... ")
    rospy.init_node("sdk_joint_position_keyboard")
    print("Getting robot state... ")
    rs = intera_interface.RobotEnable(CHECK_VERSION)
    init_state = rs.state().enabled

    def clean_shutdown():
        print("\nExiting example.")

    rospy.on_shutdown(clean_shutdown)

    rospy.loginfo("Enabling robot...")
    rs.enable()
    map_keyboard(args.limb)
    print("Done.")


if __name__ == '__main__':
    main()
