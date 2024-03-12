#!/usr/bin/env python
# Script to get the sensor data from the tactile sensors (and save optionally)

import numpy as np
import rospy
import pickle
import sys
import signal
# import matplotlib

import matplotlib.pyplot as plt
import matplotlib

from xela_server.srv import XelaSensorXYZ
from xela_server.msg import xServerMsg


class XelaSaver:
    def __init__(self, topic_name, rate, total_num_taxels=None, num_sensors=15, num_taxels=16):
        self.rate = rospy.Rate(rate) 

        # Initialize the topic callback
        rospy.Subscriber(topic_name, xServerMsg, self.callback)

        self.sensor_msg = None
        if total_num_taxels is None:
            self.total_num_taxels = num_sensors * num_taxels
        else:
            self.total_num_taxels = total_num_taxels
        
        self.curr_sensor_values = np.zeros((total_num_taxels, 3))
        self.all_sensor_values = []

        signal.signal(signal.SIGINT, self.end_signal_handler) 

    def is_initialized(self):
        return self.sensor_msg is not None

    def callback(self, data):
        print('in the callback!')
        self.sensor_msg = data  

    # Function to run and get the data 
    def run(self):
        while not rospy.is_shutdown():
            if self.is_initialized():
                print('got the data')
                self.get_data()
                self.all_sensor_values.append(self.curr_sensor_values.copy())
                print('len(self.all_sensor_values): {}'.format(len(self.all_sensor_values)))
            self.rate.sleep()
    
    # Method to convert sensor msg to sensor values on numpy
    def get_data(self):
        for taxel_id in range(self.total_num_taxels):
            curr_sensor_msg = self.sensor_msg.points[taxel_id]
            curr_sensor_value = [
                curr_sensor_msg.point.x,
                curr_sensor_msg.point.y,
                curr_sensor_msg.point.z
            ]
            self.curr_sensor_values[taxel_id] = curr_sensor_value
            print('taxel_id: {} - curr_sensor_value: {}'.format(
                taxel_id, curr_sensor_value
            ))
        
        return self.curr_sensor_values

    def dump(self):
        with open('sensor_values.pkl', 'wb') as pkl: # NOTE: Since this is just a trial we're just going to dump the data right next to the script
            pickle.dump(self.all_sensor_values, pkl, pickle.HIGHEST_PROTOCOL)

    def end_signal_handler(self, signum, frame):
        self.dump()
        rospy.signal_shutdown('Ctrl C pressed')
        exit(1)

if __name__ == '__main__':
    rospy.init_node('xela_saver', disable_signals=True)
    topic_name = '/xServTopic'
    reader = XelaSaver(topic_name, total_num_taxels=368, rate=15)
    reader.run()