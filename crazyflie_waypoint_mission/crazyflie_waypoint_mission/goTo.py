#!/usr/bin/python
import numpy as np
from crazyflie_py import *

swarm = Crazyswarm()
timeHelper = swarm.timeHelper
allcfs = swarm.allcfs

class flying_utility:
    def __init__(self):
        self.time_fly = 0.0
        # initiate array of swarm positions
        self.swarm_pos = np.zeros(3)
        self.heading = 0.0
        # initiate array of drone positions
        self.cf_pos = np.zeros((len(allcfs.crazyflies), 3))
        for idx, cf in enumerate(allcfs.crazyflies):
            self.cf_pos[idx, :] = cf.initialPosition
            print(f"__init__: init cf0{idx+1}")

    def calculate_heading(self, pos1, pos2):
        angle = np.zeros(2)
        x1 = pos1[0]
        y1 = pos1[1]
        x2 = pos2[0]
        y2 = pos2[1]
        dx = x2 - x1
        dy = y2 - y1
        angle = np.arctan2(dy, dx)
        if angle < 0:
            angle += 2 * np.pi
        print(f"calculate_heading: new yaw is {angle}")
        
        return angle
    
    def rotation_matrix(self, angle, pos):
        relative_pos = pos - self.swarm_pos  # Calculate relative position to the rotation point
        rotation_matrix_z = np.array([
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1]
        ])
        rotated_relative_pos = np.dot(rotation_matrix_z, relative_pos)
        rotated_pos = rotated_relative_pos + self.swarm_pos  # Translate back to the absolute position

        return rotated_pos
    
    def turn_swarm_in_place_left(self, desired_heading, step_size, time_per_step):
        print("turn_swarm_in_place_left: turn left / counterclockwise")
        for temporary_heading in np.arange(self.heading, (desired_heading + step_size), step_size):
            for idx, cf in enumerate(allcfs.crazyflies):
                self.cf_pos[idx] = self.rotation_matrix(step_size, self.cf_pos[idx])
                cf.goTo(self.cf_pos[idx], temporary_heading, time_per_step)
            timeHelper.sleep(time_per_step)

    def turn_swarm_in_place_right(self, desired_heading, step_size, time_per_step):
        print("turn_swarm_in_place_right: turn right / clockwise")
        for temporary_heading in np.arange(self.heading, (desired_heading - step_size), -step_size):
            for idx, cf in enumerate(allcfs.crazyflies):
                self.cf_pos[idx] = self.rotation_matrix(-step_size, self.cf_pos[idx])
                cf.goTo(self.cf_pos[idx], temporary_heading, time_per_step)
            timeHelper.sleep(time_per_step)

    def turn_swarm_in_place(self, desired_heading):
        step_size = 0.1 #rad per time_per_step
        time_per_step = self.time_fly * step_size * 0.3
        if desired_heading < self.heading and (desired_heading < np.pi and self.heading > np.pi):
            print("turn_swarm_in_place: entered case 1 special")
            desired_heading += (2 * np.pi)
            self.turn_swarm_in_place_left(desired_heading, step_size, time_per_step)
        elif desired_heading > self.heading and (desired_heading > np.pi and self.heading < np.pi):
            print("turn_swarm_in_place: entered case 2 special")
            desired_heading -= (2 * np.pi)
            self.turn_swarm_in_place_right(desired_heading, step_size, time_per_step)
        elif desired_heading > self.heading:
            print("turn_swarm_in_place: entered case 1")
            self.turn_swarm_in_place_left(desired_heading, step_size, time_per_step)
        elif desired_heading < self.heading:
            print("turn_swarm_in_place: entered case 2")
            self.turn_swarm_in_place_right(desired_heading, step_size, time_per_step)
        
    def fly(self, desired_swarm_pos):
        print(f"fly: swarm_pos: {self.swarm_pos} and desired_swarm_pos: {desired_swarm_pos}")
        desired_heading = self.calculate_heading(self.swarm_pos, desired_swarm_pos) # calculate the heading from momentary position to desired position
        vector_to_desired_swarm_pos_x = desired_swarm_pos[0] - self.swarm_pos[0]
        vector_to_desired_swarm_pos_y = desired_swarm_pos[1] - self.swarm_pos[1]
        vector_to_desired_swarm_pos = np.array([vector_to_desired_swarm_pos_x, vector_to_desired_swarm_pos_y, 0])
        self.turn_swarm_in_place(desired_heading)
        for idx, cf in enumerate(allcfs.crazyflies):
            self.cf_pos[idx] += vector_to_desired_swarm_pos
            self.cf_pos[idx][2] = desired_swarm_pos[2]
            cf.goTo(self.cf_pos[idx], desired_heading, self.time_fly)
            print(f"fly: cf0{idx+1} going to {desired_swarm_pos}")
        self.swarm_pos = desired_swarm_pos # overwrite swarm position after arriving (middle of swarm)
        self.heading = desired_heading # overwrite heading of swarm after arriving (angle the swarm as a whole is pointing at)
        print(f"fly: wating for {self.time_fly}")
        timeHelper.sleep(self.time_fly)

def main():
    fly_util = flying_utility()
    
    # waypoints
    home_hover = np.array([0, 0, 0.5])
    start = np.array([-1, 0, 1])
    pos1 = np.array([0, 1, 1.2])
    pos2 = np.array([0, -1, 0.5])
    end = np.array([1, 0, 1])

    # time
    time = 4
    fly_util.time_fly = 5

    timeHelper.sleep(10)

    # takeoff
    height = 0.5
    allcfs.takeoff(targetHeight = height, duration = time)
    fly_util.swarm_pos[2] = height
    print("main: takeoff")
    timeHelper.sleep(time)

    # mission
    fly_util.fly(home_hover)
    fly_util.fly(start)
    # fly_util.fly(pos1)
    # fly_util.fly(pos2)
    fly_util.fly(end)

    # prepare to land
    fly_util.fly(home_hover)
    for idx, cf in enumerate(allcfs.crazyflies):
            fly_util.cf_pos[idx] = cf.initialPosition
            fly_util.cf_pos[idx][2] = 0.5
            cf.goTo(fly_util.cf_pos[idx], 0, time)
            print(f"preparing to land: cf0{idx+1} going to {fly_util.cf_pos[idx]}")
    timeHelper.sleep(time)

    # land
    allcfs.land(targetHeight = 0.02, duration = time)
    print("main: land")
    timeHelper.sleep(time)

if __name__ == "__main__":
    main()