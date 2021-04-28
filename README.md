## subscriber_heavy_delay

Run

```shell
$ python sub.py
$ python pub.py
```

at the same time.

The calllback function of subscriber is really heavy.

```
+-----------+ /chatter1  +----------+ /chatter2
| pub(1Hz)  | =========> | sub(1Hz) | =========>
+-----------+          | +----------+
                       |==> (callback, 6sec!) ==> loginfo(...)
```

Since the spin loop is 1Hz, publication to `/chatter2` is processed nearly abut 1Hz.

```python
rate = rospy.Rate(1)
while not rospy.is_shutdown():
    msg = "published to /chatter2 at " + \
        datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    pub.publish(msg)
    rospy.loginfo(msg)
    rate.sleep()
```

But when the subscriber received data from `/chatter1` the callback returns after about 6 seconds.

```python
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
```

The published data is queued (somewhere), so even after you **stopped `pub.py` with Ctrl-C**, the subscriber continues to `rospy.loginfo()` until it consumes all published data.
