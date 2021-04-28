from datetime import datetime
import rospy
from std_msgs.msg import String

if __name__ == '__main__':
    rospy.init_node("pub")
    pub = rospy.Publisher("/chatter1", String, queue_size=10)
    rate = rospy.Rate(1)

    while not rospy.is_shutdown():
        msg = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        pub.publish(str(msg))
        rate.sleep()
