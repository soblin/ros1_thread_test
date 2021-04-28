import rospy
from datetime import datetime
import std_msgs


def cb(msg):
    t1 = rospy.Time.now().to_sec()
    arr = [0 for i in range(10)]
    # heavy process
    for i in range(1, 10000):
        for j in range(1, 10000):
            arr[(i+j) % 10] = i+j

    t2 = rospy.Time.now().to_sec()
    duration = t2 - t1
    rospy.loginfo("From /chatter1 at" + datetime.now().strftime("%d/%m/%Y %H:%M:%S") +
                  ", received " + msg.data + ", proc-time was " + str(duration))


if __name__ == '__main__':
    rospy.init_node("test")

    sub = rospy.Subscriber("/chatter1", std_msgs.msg.String, cb)
    pub = rospy.Publisher("/chatter2", std_msgs.msg.String, queue_size=10)
    rate = rospy.Rate(1)

    while not rospy.is_shutdown():
        msg = "published to /chatter2 at " + \
            datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        pub.publish(msg)
        rospy.loginfo(msg)
        rate.sleep()
