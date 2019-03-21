#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

def move():
	rospy.init_node('steer', anonymous=True)
	vel_pub = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=10)
	vel_msg = Twist()
	
	print("what")
	lol = input("how much")
	
	vel_msg.linear.x=0

	while not rospy.is_shutdown():
	
		#move here

		vel_pub.publish(vel_msg)

if __name__ == '__main__':
	try:
		move()
	except rospy.ROSInterruptException: pass
	