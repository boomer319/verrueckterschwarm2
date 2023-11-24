#!/usr/bin/python
import numpy as np
from crazyflie_py import *

swarm = Crazyswarm()
timeHelper = swarm.timeHelper
allcfs = swarm.allcfs

class flying_utility:
    def __init__(self):
        # initiate array of swarm positions
        self.swarm_pos = np.zeros(3)
        # initiate array of drone positions
        self.cf_pos = np.zeros((len(allcfs.crazyflies), 3))
        for idx, cf in enumerate(allcfs.crazyflies):
            self.cf_pos[idx, :] = cf.initialPosition
            print(f"__init__: init cf0{idx+1}")

    def calculate_heading(self, pos1, pos2):
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

    def rotation_matrix(self, heading, pos):
        rotation_matrix_z = np.array([
                [np.cos(heading), -np.sin(heading), 0],
                [np.sin(heading),  np.cos(heading), 0],
                [0, 0, 1]
            ])
        positions_aligned_with_heading = np.dot(rotation_matrix_z, pos)

        return positions_aligned_with_heading
        
    def fly(self, desired_pos, time):
        print(f"fly: swarm_pos: {self.swarm_pos} and desired_pos: {desired_pos}")
        heading = self.calculate_heading(self.swarm_pos, desired_pos) # calculate the heading from momentary position to desired position
        for idx, cf in enumerate(allcfs.crazyflies):
            self.cf_pos[idx] = self.rotation_matrix(heading, self.cf_pos[idx])
            self.cf_pos[idx] += desired_pos # add desired pos or rather: overwritten swarm position to each cf
            cf.goTo(self.cf_pos[idx], heading, time)
            print(f"fly: cf0{idx+1} going to {desired_pos}")
        self.swarm_pos = desired_pos # overwrite swarm position (middle of swarm)
        print(f"fly: wating for {time}")
        timeHelper.sleep(time)

def main():
    fly_util = flying_utility()
    
    # waypoints
    home_hover = np.array([0, 0, 0.5])
    start = np.array([-1, 0, 1])
    pos1 = np.array([0, 1, 1.75])
    pos2 = np.array([0, -1, 0.5])
    end = np.array([1, 0, 1])
    # print(f"main: waypoint mission through {home_hover, start, pos1, pos2, end, home_hover}")

    # time
    time = 20
    time_fly = 20
    
    # takeoff
    height = 0.5
    allcfs.takeoff(targetHeight = height, duration = time)
    fly_util.swarm_pos[2] = height
    print("main: takeoff")
    timeHelper.sleep(time)

    # go hover over home
    fly_util.fly(home_hover, time_fly)
    fly_util.fly(start, time_fly)
    fly_util.fly(pos1, time_fly)

    # land
    allcfs.land(targetHeight = 0.02, duration = time)
    print("main: land")
    timeHelper.sleep(time)

if __name__ == "__main__":
    main()