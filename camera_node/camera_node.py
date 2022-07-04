# Import the necessary libraries
from copyreg import pickle
import socket
from time import sleep
from unittest.result import failfast
import rclpy # Python Client Library for ROS 2
from rclpy.node import Node # Handles the creation of nodes
from sensor_msgs.msg import Image # Image is the message type
from cv_bridge import CvBridge # Package to convert between ROS and OpenCV Images
import cv2 # OpenCV library
import sys
from torch import hub # Hub contains other models like FasterRCNN
import struct
import pickle

thres = 0.45 # Threshold to detect object

classFile = 'coco.names'
with open(classFile,'rt') as f:
  classNames = f.read().rstrip('\n').split('\n')

configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'


net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)
   
 
class ImagePublisher(Node):
  """
  Create an ImagePublisher class, which is a subclass of the Node class.
  """
  def __init__(self):
    """
    Class constructor to set up the node
    """
    # Initiate the Node class's constructor and give it a name
    super().__init__('image_publisher')

    self.br = CvBridge()
      
    # Create the publisher. This publisher will publish an Image
    # to the video_frames topic. The queue size is 10 messages.
    self.publisher_ = self.create_publisher(Image, 'video_frames', 10)

    self.subscription = self.create_subscription(Image, '/camera/image_raw', self.listener_callback, 10)
    self.subscription


  def listener_callback(self, msg:Image):
    #self.get_logger().info('I heard: "%s"' % msg.data)
    self.get_logger().info('Mensaje leido"')
    
    current_frame = self.br.imgmsg_to_cv2(msg)
   
      # Publish the image.
      # The 'cv2_to_imgmsg' method converts an OpenCV
      # image to a ROS 2 image message
    classIds, confs, bbox = net.detect(current_frame,confThreshold=thres)
    #print("eh", classIds,bbox)
    self.get_logger().info('Detectado')

    if len(classIds) != 0:
      for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
          cv2.rectangle(current_frame,box,color=(0,255,0),thickness=2)
          cv2.putText(current_frame,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
          cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
          cv2.putText(current_frame,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
          cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
          print(current_frame,classNames[classId-1].upper())
    
    self.get_logger().info('Pintado')
    # Display image
      #cv2.imshow("camera", current_frame)
    
    self.publisher_.publish(self.br.cv2_to_imgmsg(current_frame, encoding=msg.encoding))

    cv2.imwrite('img.jpg', current_frame)

    self.get_logger().info('Publicado')

    sleep(1)
    
  
def main(args=None):
  
  # Initialize the rclpy library
  rclpy.init(args=args)
  
  # Create the node
  image_publisher = ImagePublisher()
  
  # Spin the node so the callback function is called.
  rclpy.spin(image_publisher)


  
  # Destroy the node explicitly
  # (optional - otherwise it will be done automatically
  # when the garbage collector destroys the node object)
  image_publisher.destroy_node()

  
  # Shutdown the ROS client library for Python
  rclpy.shutdown()
  
if __name__ == '__main__':
  main()
