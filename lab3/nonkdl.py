#! /usr/bin/python
import rospy
import json
import os
from sensor_msgs.msg import *
from geometry_msgs.msg import *
from tf.transformations import *

# osie
xaxis, yaxis, zaxis = (1, 0, 0), (0, 1, 0), (0, 0, 1)

# dlugosc koncowki
end_len=0.5
# macierze do translacji koncowki
tz = translation_matrix((0, 0, 0))
rz = rotation_matrix(0, zaxis)
tx = translation_matrix((end_len, 0, 0))
rx = rotation_matrix(0, xaxis)
end_matrice = concatenate_matrices(tx, rx, tz, rz)


def callback(data):
    mainMatrix = translation_matrix((0, 0, 0))

    # odczyt parametrow dh
    with open(os.path.dirname(os.path.realpath(__file__)) + '/in.json', 'r') as file:
        params = json.loads(file.read())
	matrices = {}
        for key in params.keys():
            a, d, al, th = params[key]
            al, a, d, th = float(al), float(a), float(d), float(th)

            # update od joint state'a
            if key == 'firstRow':
                tz = translation_matrix((0, 0, d+data.position[0]))
                rz = rotation_matrix(th, zaxis)
            
	    if key == 'secondRow':
                tz = translation_matrix((0, 0, d))
                rz = rotation_matrix(th+data.position[1], zaxis)
            if key == 'thirdRow' :
                tz = translation_matrix((0, 0, d))
                rz = rotation_matrix(th+data.position[2], zaxis)

	    
            tx = translation_matrix((a, 0, 0))
            rx = rotation_matrix(al, xaxis)
            matrices[key] = concatenate_matrices(tx, rx, tz, rz)
    
    #mnozenie kolejnych macierzy
    for key in sorted(params.keys()):
	mainMatrix = concatenate_matrices(mainMatrix,matrices[key])

    mainMatrix = concatenate_matrices(mainMatrix,end_matrice)
     
    # odczyt pozycji z macierzy wynikowej
    x , y , z = translation_from_matrix(mainMatrix)
    
    poseR = PoseStamped()           #wiadomosc z pozycja na temat (do rviza)
    poseR.header.frame_id = "base_link"
    poseR.header.stamp = rospy.Time.now()
    poseR.pose.position.x = x
    poseR.pose.position.y = y
    poseR.pose.position.z = z
    
    xq, yq, zq, wq = quaternion_from_matrix(mainMatrix)     #odczyt orientacji

    poseR.pose.orientation.x = xq   #wiadomosc z orientacja na temat (do rviza)
    poseR.pose.orientation.y = yq
    poseR.pose.orientation.z = zq
    poseR.pose.orientation.w = wq

    # publish na temat
    publisher.publish(poseR)


def listen():      

    rospy.init_node('NONKDL_DKIN', anonymous = False)

    rospy.Subscriber("joint_states", JointState , callback)

    rospy.spin()

if __name__ == '__main__':

    publisher = rospy.Publisher('nonkdl', PoseStamped, queue_size=10)

    try:
	    listen()        
    except rospy.ROSInterruptException:
	pass
