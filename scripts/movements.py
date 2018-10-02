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

def _guarded_move_to_joint_position(self, joint_angles, timeout=10.0):
		if rospy.is_shutdown():
			return
		if joint_angles:
			self._limb.move_to_joint_positions(joint_angles,timeout=timeout)
			#print (self._limb.endpoint_pose())
		else:
			rospy.logerr("No Joint Angles provided for move_to_joint_positions. Staying put.")


def _guarded_move_to_joint_position_two(limb, set_joint_angles, speed_ratio = 0.4, accel_ratio = 0.2, timeout = 10.0):
		try:
			traj = MotionTrajectory(limb = limb)
			wpt_opts = MotionWaypointOptions(max_joint_speed_ratio=speed_ratio,
			                                 max_joint_accel=accel_ratio)
			waypoint = MotionWaypoint(options = wpt_opts.to_msg(), limb = limb)

			joint_angles = limb.joint_ordered_angles()

			waypoint.set_joint_angles(joint_angles = joint_angles)
			traj.append_waypoint(waypoint.to_msg())
			if len(set_joint_angles) != len(joint_angles):
			 	rospy.logerr('The number of joint_angles must be %d', len(joint_angles))
			 	return None

			waypoint.set_joint_angles(joint_angles = set_joint_angles)
			traj.append_waypoint(waypoint.to_msg())

			result = traj.send_trajectory(timeout= timeout)
			if result is None:
				rospy.logerr('Trajectory FAILED to send')
				return

			if result.result:
				rospy.loginfo('Motion controller successfully finished the trajectory!')
			else:
				rospy.logerr('Motion controller failed to complete the trajectory with error %s',
				result.errorId)
		except rospy.ROSInterruptException:
			rospy.logerr('Keyboard interrupt detected from the user. Exiting before trajectory completion.')


			
def linear_movement(self,position, linear_speed = 0.2, linear_accel = 0.2, rotational_speed = 0.1, rotational_accel = 0.1):
	   	try:
			traj_options = TrajectoryOptions()
			traj_options.interpolation_type = TrajectoryOptions.CARTESIAN
			traj = MotionTrajectory(trajectory_options = traj_options, limb = self._limb)

			wpt_opts = MotionWaypointOptions(max_linear_speed=linear_speed,
			                                 max_linear_accel=linear_accel,
			                                 max_rotational_speed=rotational_speed,
			                                 max_rotational_accel=rotational_accel,
			                                 max_joint_speed_ratio=0.2)
			waypoint = MotionWaypoint(options = wpt_opts.to_msg(), limb = self._limb)
			poseStamped = PoseStamped()
			poseStamped.pose = position
			waypoint.set_cartesian_pose(poseStamped, self._tip_name)

			rospy.loginfo('Sending waypoint: \n%s', waypoint.to_string())

			traj.append_waypoint(waypoint.to_msg())

			result = traj.send_trajectory(timeout=5.0)
			if result is None:
			    rospy.logerr('Trajectory FAILED to send')
			    return

			if result.result:
			    rospy.loginfo('Motion controller successfully finished the trajectory!')
			else:
			    rospy.logerr('Motion controller failed to complete the trajectory with error %s',
			                 result.errorId)
		except rospy.ROSInterruptException:
			rospy.logerr('Keyboard interrupt detected from the user. Exiting before trajectory completion.')


rospy.init_node('fk_ik')
rs = intera_interface.RobotEnable(CHECK_VERSION)
limb = intera_interface.Limb('right')

rs.enable
limb.set_joint_position_speed(0.1)
limb.move_to_neutral()



