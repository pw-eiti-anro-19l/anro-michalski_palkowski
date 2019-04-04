#!/usr/bin/env python
import sys
import rospy
import tty
import termios
from geometry_msgs.msg import Twist

def get_key():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(fd)
		ch = sys.stdin.read(1)
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch


def move():
	rospy.init_node('steer', anonymous=True)
	vel_pub = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=10)
	vel_msg = Twist()
	
	forward = rospy.get_param("steer/forward")
	backward = rospy.get_param("steer/backward")
	left = rospy.get_param("steer/rot_left")
	right = rospy.get_param("steer/rot_right")
	

	while not rospy.is_shutdown():
		key = get_key()
		
		if key == 'q':
			raise KeyboardInterrupt
		
		vel = Twist()
		
		if key == forward:
			vel.linear.x = 1.0
		elif key == backward:
			vel.linear.x = -1.0
		elif key == left:
			vel.angular.z = 1.0
		elif key == right:
			vel.angular.z = -1.0
		else:
			continue
			
		vel_pub.publish(vel)

if __name__ == '__main__':
	try:
		move()
	except (rospy.ROSInterruptException, KeyboardInterrupt): pass
	