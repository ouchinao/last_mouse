import rclpy
from rclpy.node import Node
from std_msgs.msg import String

import cv2
import numpy as np
import time


capture = cv2.VideoCapture(0)

class MousePublisher(Node):
    def __init__(self):
        super().__init__('mouse_publisher')
        self.publisher1 = self.create_publisher(String, 'camera_left_topic', 10)
        self.publisher2 = self.create_publisher(String, 'camera_right_topic', 10)
        timer_period = 0.1
        self.timer = self.create_timer(timer_period,self.getrate)
    
    def red_detect(self, img):
        #HSV色空間に変換
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        #オレンジ色のHSVの値域
        hsv_min = np.array([85,120,100])
        hsv_max = np.array([130,255,255])
        mask1 = cv2.inRange(hsv, hsv_min, hsv_max)
    
        return mask1


    def findContours(self, mask, frame, left_right, height, width):
        rectangle_area = height * width
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if(contours):
            max_contours = max(contours, key=lambda x: cv2.contourArea(x))
            rate = cv2.contourArea(max_contours) / (rectangle_area/2) * 100
            '''
            cv2.putText(frame, str(format(rate, '2.1f').rstrip('0')), org=(int(left_right * width/2 + 5), int(height - 5)),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1.0,
                color=(255, 255, 255),
                thickness=3,
                lineType=cv2.LINE_4)
            cv2.putText(mask, str(format(rate, '2.1f').rstrip('0')), org=(int(5), int(height - 5)),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=1.0,
                color=(255, 255, 255),
                thickness=3,
                lineType=cv2.LINE_4)
            '''
        else:
            rate = 0
        
        return int(rate)

    def drawContours(self, mask, frame):
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if(contours):
            max_contours = max(contours, key=lambda x: cv2.contourArea(x))
            cv2.drawContours(frame, max_contours, -1, color=(0, 0, 255), thickness=5)

    def getrate(self):
        #time.sleep(1)

        ret, frame = capture.read()

        height, width, channels = frame.shape
        clp1 = frame[0:height, 0:width//2]
        clp2 = frame[0:height, width//2:width]

        #色抽出
        mask = self.red_detect(frame)
        mask1 = self.red_detect(clp1)
        mask2 = self.red_detect(clp2)

        #割合
        rate_left = self.findContours(mask1, frame, 0, height, width)
        rate_right = self.findContours(mask2, frame, 1, height, width)
        
        print('left: ' + format(rate_left, '2.1f').rstrip('0') + ' right ' + format(rate_right, '2.1f').rstrip('0'))
        #self.drawContours(mask, frame)

        #画面表示
        '''
        cv2.imshow("Mask1", mask1)
        cv2.imshow("Mask2", mask2)
        cv2.imshow("Frame", frame)
        '''
        
        key = String()
        key.data = str(rate_left)
        self.publisher1.publish(key)
        key.data = str(rate_right)
        self.publisher2.publish(key)
    
def main():
    rclpy.init()
    node = MousePublisher()
    rclpy.spin(node)
    capture.release()
    cv2.destroyAllWindows()
    rclpy.destroy_node()
    rclpy.shutdown()
if __name__ == "__main__":
    
    main ()