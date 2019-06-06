#! /usr/bin/python
import rospy
import json
import PyKDL as kdl


from sensor_msgs.msg import *
from geometry_msgs.msg import *
from tf.transformations import *
import os

def callback(data):
    # <PyKDL.Chain object at 0x7f29da463640>
    kdlChain = kdl.Chain()  

    frame = kdl.Frame()

    poseR = PoseStamped()

    with open(os.path.dirname(os.path.realpath(__file__)) + '/in.json', 'r') as file:# we open our file and read parameters
        params = json.loads(file.read())

 
    fRow = params["firstRow"]
    sRow = params["secondRow"]
    tRow = params["thirdRow"]

	# json: 	a,	 d,	 alpha,	 theta
	# rame.DH:	a, 	alpha,	 d,	 theta


    kdlChain.addSegment(kdl.Segment(kdl.Joint(kdl.Joint.TransZ), frame.DH(sRow[0], 0, fRow[1], fRow[3])))
    kdlChain.addSegment(kdl.Segment(kdl.Joint(kdl.Joint.RotZ), frame.DH(tRow[0], 0, 0, sRow[3])))

    kdlChain.addSegment(kdl.Segment(kdl.Joint(kdl.Joint.RotZ), frame.DH(0.5, 0, 0, 0)))

    jointPos = kdl.JntArray(kdlChain.getNrOfJoints())
      
    jointPos[0] = data.position[0] 
    jointPos[1] = data.position[1]
    jointPos[2] = data.position[2]
    
    forvKin = kdl.ChainFkSolverPos_recursive(kdlChain)
    fframe = kdl.Frame() 
    forvKin.JntToCart(jointPos, fframe)

    quaternion = fframe.M.GetQuaternion()

    poseR.header.frame_id = 'base_link'
    poseR.header.stamp = rospy.Time.now()


    poseR.pose.position.x = fframe.p[0]
    poseR.pose.position.y = fframe.p[1]
    poseR.pose.position.z = fframe.p[2]

    poseR.pose.orientation.x = quaternion[0]
    poseR.pose.orientation.y = quaternion[1]
    poseR.pose.orientation.z = quaternion[2]
    poseR.pose.orientation.w = quaternion[3]

    publisher.publish(poseR)


def kdl_listener():
    rospy.init_node('KDL_DKIN', anonymous = False)

    rospy.Subscriber("joint_states", JointState , callback)

    rospy.spin()

if __name__ == '__main__':
    publisher = rospy.Publisher('kdl', PoseStamped, queue_size=10)

    try:
        kdl_listener()        
    except rospy.ROSInterruptException:
        pass
