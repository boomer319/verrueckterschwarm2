#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist
from crazyflie_interfaces.srv import Takeoff, Land
from crazyflie_interfaces.msg import Hover
import time

HEIGHT = 0.3

class VelMux(Node):
    def __init__(self):
        super().__init__('vel_mux')
        self.declare_parameter('hover_height', 0.5)
        self.declare_parameter('robot_prefix', '/cf1')
        self.declare_parameter('incoming_twist_topic', '/cmd_vel')

        self.hover_height  = self.get_parameter('hover_height').value
        robot_prefix  = self.get_parameter('robot_prefix').value
        incoming_twist_topic  = self.get_parameter('incoming_twist_topic').value
        
        self.get_logger().info(f"Velocity Multiplexer set for {robot_prefix}"+
                               f" with height {self.hover_height} m using the {incoming_twist_topic} topic")

        print("PARAMETERS", self.hover_height, robot_prefix, incoming_twist_topic)

        self.subscription = self.create_subscription(
            Twist,
            incoming_twist_topic,
            self.cmd_vel_callback,
            10)
        self.msg_cmd_vel = Twist()
        self.received_first_cmd_vel = False
        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.take_off_client = self.create_client(Takeoff, robot_prefix + '/takeoff')
        self.publisher_hover = self.create_publisher(Hover, robot_prefix + '/cmd_hover', 10)
        self.land_client = self.create_client(Land, robot_prefix + '/land')
        self.cf_has_taken_off = False

    def cmd_vel_callback(self, msg):
        self.msg_cmd_vel = msg
        # This is to handle the zero twist messages from teleop twist keyboard closing
        # or else the crazyflie would constantly take off again.
        msg_is_zero = msg.linear.x == 0.0 and msg.linear.y == 0.0 and msg.angular.z == 0.0 and msg.linear.z == 0.0
        if  msg_is_zero is False and self.received_first_cmd_vel is False and msg.linear.z >= 0.0:
            self.received_first_cmd_vel = True
            print('takeoff')

    def timer_callback(self):
        if self.received_first_cmd_vel and self.cf_has_taken_off is False:
            req = Takeoff.Request()
            req.height = self.hover_height
            req.duration = rclpy.duration.Duration(seconds=2.0).to_msg()
            self.take_off_client.call_async(req)
            self.cf_has_taken_off = True
            time.sleep(2.0)        
        if self.received_first_cmd_vel and self.cf_has_taken_off:
            if self.msg_cmd_vel.linear.z >= 0:
                msg = Hover()
                msg.vx = self.msg_cmd_vel.linear.x
                msg.vy = self.msg_cmd_vel.linear.y
                msg.yaw_rate = self.msg_cmd_vel.angular.z
                msg.z_distance = HEIGHT
                self.publisher_hover.publish(msg)
            else:
                print('land')
                req = Land.Request()
                req.height = 0.1
                req.duration = rclpy.duration.Duration(seconds=2.0).to_msg()
                self.land_client.call_async(req)
                time.sleep(2.0)        
                self.cf_has_taken_off = False
                self.received_first_cmd_vel = False



def main(args=None):
    rclpy.init(args=args)

    vel_mux = VelMux()

    rclpy.spin(vel_mux)

    vel_mux.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()