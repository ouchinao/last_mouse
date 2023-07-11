#motor
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

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
        motor_drive(str(0), str(0))
        super().__init__('mouse_subscriber')
        self.speed = ["",""]
        self.subscription=self.create_subscription(
            String ,
            'mouse_controll_topic',
            self.listener_callback ,
            10)
        self.subscription=self.create_subscription(
            String ,
            'mouse_controll_topic2',
            self.listener_callback2 ,
            10)

    def listener_callback(self, msg):
        self.speed[0] = msg.data


       
    def listener_callback2(self, msg):
        self.speed[1] = msg.data
        print(self.speed[0],self.speed[1])
        #motor_drive("0", "0")
        #time.sleep(0.5)
        motor_drive(self.speed[0],self.speed[1])
        
           
def main():
    rclpy.init()
    node = MouseSubscriber()
    rclpy.spin(node)
    rclpy.destroy_node()
    rclpy.shutdown()
if __name__ == "__main__":
    main ()