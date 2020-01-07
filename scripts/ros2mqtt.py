#!/usr/bin/python
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32
from rosbridge_library.internal import message_conversion
import rostopic
# import context  # Ensures paho is in PYTHONPATH
# import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

def get_keys(begin_path, d, pool):
    # if len(d.keys()) == 1:
    #     if type(d[d.keys()[0]]) is not dict and d.keys()[0] == "data":
    #         pool.append({"topic": ".", "payload": d[d.keys()[0]]})
    #         return

    for key in d.keys():
        if type(d[key]) is dict:
            # return get_keys(d[key])
            get_keys(begin_path + "/" + key, d[key], pool)
        else:
            pool.append({"topic": begin_path + "/" + key, "payload": d[key]})


def get_subtopics(msg, begin_path=""):
    message_dict = message_conversion.extract_values(msg)
    pool = []
    get_keys(begin_path, message_dict, pool)
    pool_filter = [x for x in pool if x["topic"].strip() != ""]
    return pool_filter
    


class MqttBridgeNode(object):

    def __init__(self):
        self.topic_prefix = rospy.get_param("~topic_prefix", default="/turquoise/")
        self.hostname = rospy.get_param("~hostname", default="localhost")
        self.port = rospy.get_param("~port", default=1883)
        self.keepalive = rospy.get_param("~keepalive", default=60)

        self.rate = rospy.Rate(2)

        self.mqttc = mqtt.Client()
        self.mqttc.connect(self.hostname, self.port, self.keepalive)
        self.mqttc.loop_start()

        self.subs = []
        self.update_topics()

    def update_topics(self):
        all_topics = [x[0] for x in rospy.get_published_topics(self.topic_prefix)]
        topic_pool = []
        for topic in all_topics:
            cl = rostopic.get_topic_class(topic)[0]
            topic_pool.append({"topic": topic, "class": cl})
        for topic in topic_pool:
            name = topic["topic"]
            cl = topic["class"]
            if not name in [x["topic"] for x in self.subs]:
                rospy.loginfo("Adding new topic, {}".format(name))
                self.subs.append({"sub": rospy.Subscriber(name, cl, self.ros_callback, callback_args=name), "topic": name})
                

    def ros_callback(self, data, topic):
        pool = get_subtopics(data, begin_path=topic)
        for x in pool:
            if type(x['payload']) in [int, float, bytearray, str]:
                self.mqttc.publish(x["topic"], x["payload"], qos=0)


    def spin(self):
        while not rospy.is_shutdown():
            self.update_topics()
            self.rate.sleep()





if __name__ == "__main__":
    rospy.init_node("mqtt_topic_conv_node")
    node = MqttBridgeNode()
    node.spin()