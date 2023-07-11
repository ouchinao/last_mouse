#台形制御
#色の占有率を%で受け取る
#このままだと前進しかしないので条件をより厳しくするか見直す
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import math
import numpy as np

import time
import sys

filename_motoren = "/dev/rtmotoren0"
filename_motor_r = "/dev/rtmotor_raw_r0"
filename_motor_l = "/dev/rtmotor_raw_l0"
filename_motor = "/dev/rtmotor0"

SPEED = "10"
TIME_MS = "500"

def motor_drive(freq_l="0", freq_r="0"):
    with open(filename_motor_l, 'w') as f:
        f.write(freq_l)
    with open(filename_motor_r, 'w') as f:
        f.write(freq_r)

print("Motor On")
with open(filename_motoren, 'w') as f:
    f.write("1")
time.sleep(0.5)

class MouseSubscriber(Node):
    def __init__(self):
        super().__init__('mouse_controll')
        self.speed_value = 0
        self.speed_per1_right = "0"
        #self.speed_per2_right = "0"
        self.speed_per1_left = "0"
        #self.speed_per2_left = "0"
        self.mode_1 = ""
        self.mode_2 = ""
        self.subscription=self.create_subscription(
            String ,
            'camera_right_topic',
            self.listener_callback_1 ,
            10)
        self.subscription=self.create_subscription(
            String ,
            'camera_left_topic',
            self.listener_callback_2 ,
            10)

        self.publisher1 = self.create_publisher(String, 'mouse_controll_topic', 10)
        self.publisher2 = self.create_publisher(String, 'mouse_controll_topic2', 10)
        timer_period = 0.1
        self.timer = self.create_timer(timer_period,self.speed_controll)


    def speed_controll(self):
        print(self.speed_per1_left, " ", self.speed_per1_right)
        print(int(self.speed_per1_left) + int(self.speed_per1_right))

        self.speed = String()

        sum_camera = int(self.speed_per1_left) + int(self.speed_per1_right) + 1
        
        if(int(self.speed_per1_right) * (24/math.sqrt(sum_camera)) < int(self.speed_per1_left)):
            self.mode_2 = "a"
        elif(int(self.speed_per1_left) * (24/math.sqrt(sum_camera)) < int(self.speed_per1_right)):
            self.mode_2 = "d"
        elif(sum_camera  <= 80):
            self.mode_2= "w"
        elif(sum_camera >=150):
            self.mode_2 = "s"
        else:
            self.mode_2 = "p"

        print("mode：",self.mode_2)

    
        if(self.mode_1 == ""):
            self.mode_1 = self.mode_2
        elif (self.mode_1 != self.mode_2):
            print("gensoku")
            while(1):
                time.sleep(0.2)
                if(self.speed_value <= 0):
                    self.speed_value = 0
                    break
                self.speed_value -= 20
                if (self.mode_1 == "w"):
                    print("w_gensoku")
                    self.speed.data = str(self.speed_value)
                    self.publisher1.publish(self.speed)
                    self.speed.data = str(self.speed_value)
                    self.publisher2.publish(self.speed)
                elif (self.mode_1 == "a"):
                    self.speed_value = 0
                    self.speed.data = str(self.speed_value) #-
                    self.publisher1.publish(self.speed)
                    self.speed.data = str(self.speed_value)
                    self.publisher2.publish(self.speed)
                elif (self.mode_1 == "s"):
                    self.speed.data = "-" + str(self.speed_value) #-
                    self.publisher1.publish(self.speed)
                    self.speed.data = "-" + str(self.speed_value) #-
                    self.publisher2.publish(self.speed)
                elif (self.mode_1 == "d"):
                    self.speed_value = 0
                    self.speed.data = str(self.speed_value)
                    self.publisher1.publish(self.speed)
                    self.speed.data = str(self.speed_value) #-
                    self.publisher2.publish(self.speed)
            self.mode_1 = self.mode_2
            print("mode_1：", self.mode_1)


                #kasuku
        if(self.mode_2 == "a"):
            self.speed_value = 30
            self.speed.data = "-" + str(self.speed_value) #-
            self.publisher1.publish(self.speed)
            self.speed.data = str(self.speed_value)
            self.publisher2.publish(self.speed)
        elif(self.mode_2 == "d"):
            self.speed_value = 30
            self.speed.data = str(self.speed_value)
            self.publisher1.publish(self.speed)
            self.speed.data = "-" + str(self.speed_value) #-
            self.publisher2.publish(self.speed)
        elif(self.mode_2 == "w"):
            if (self.speed_value < 200):
                self.speed_value += 20
            self.speed.data = str(self.speed_value)
            self.publisher1.publish(self.speed)
            self.speed.data = str(self.speed_value)
            self.publisher2.publish(self.speed)
        elif(self.mode_2 == "s"):
            print("ushiro")
            if (self.speed_value < 200):
                print("OK kasoku")
                self.speed_value += 20
            self.speed.data = "-" + str(self.speed_value)
            self.publisher1.publish(self.speed)
            self.speed.data = "-" + str(self.speed_value)
            self.publisher2.publish(self.speed)
        else:
            self.speed_value = 0
            self.speed.data = str(self.speed_value)
            self.publisher1.publish(self.speed)
            self.speed.data = str(self.speed_value)
            self.publisher2.publish(self.speed)
            

    def listener_callback_1(self, msg):
        self.speed_per1_right = msg.data
        #print(self.speed_per1_right)
        #self.speed_controll()
    
    def listener_callback_2(self, msg):
        self.speed_per1_left = msg.data
        #print(self.speed_per1_left)


def main():
    rclpy.init()
    node = MouseSubscriber()
    rclpy.spin(node)
    rclpy.destroy_node()
    rclpy.shutdown()
if __name__ == "__main__":
    main ()