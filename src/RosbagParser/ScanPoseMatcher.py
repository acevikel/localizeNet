import rosbag
import tf
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Point, Pose, Quaternion, Twist, Vector3
import rospy
import numpy as np
import math

def vectorizeScan(scanmsg):
    rx = scanmsg.ranges
    rx = [0.0 if x==float("inf") else x for x in rx]
    res = np.array(rx)/scanmsg.range_max
    return res

def vectorizePose(pose):
    yaw=tf.transformations.euler_from_quaternion(pose[1])[2]
    yaw =  int((math.degrees(yaw)+180.0)/4)
    x = int(pose[0][0])
    y= int(pose[0][1])
    return ("x"+str(x),"y"+str(y),"w"+str(yaw))

"""
Class for matching scan data with respective position at that time.
Input : A bag file containing tf and scan topics 
Output : A list of matched scan,pose tuples as vectorsd
"""

class ScanPoseMatcher(object):

    def __init__(self,scan_topic="/scan",tf_topic="/tf",global_frame="map",target_frame="base_footprint"):
        self.scan_topic = scan_topic
        self.tf_topic = tf_topic
        self.global_frame = global_frame
        self.target_frame =  target_frame

    
    """
    Loops over bag file and if the message is tf, updates transform buffer, if its scan, gets scan
    position if possible and adds it to result.     
    """
    def getPairs(self,bagfile):
        result = []
        tfr = tf.Transformer(True,rospy.Duration(1))
        for topic, msg, t in rosbag.Bag(bagfile).read_messages(): 
            if (topic == self.tf_topic):
                for tfs in msg.transforms:
                    tfr.setTransform(tfs)
            
            elif (topic==self.scan_topic):
                if tfr.canTransform(self.global_frame,self.target_frame,rospy.Time(0)):
                    pose = tfr.lookupTransform(self.global_frame,self.target_frame,rospy.Time(0))
                    result.append((vectorizeScan(msg),vectorizePose(pose)))
        
        print "Extracted {0} pairs from file : {1}".format(len(result),bagfile)
        cols = zip(*result)
        return np.column_stack(cols[0]),np.column_stack(cols[1])

                    
    

if __name__ == "__main__":
    sm = ScanPoseMatcher()
    X,Y =sm.getPairs("/home/acevikel/localizenet/RosbagParser/test.bag")
    np.save("/home/acevikel/localizenet/RosbagParser/X_train",X)
    np.save("/home/acevikel/localizenet/RosbagParser/Y_train",Y)
