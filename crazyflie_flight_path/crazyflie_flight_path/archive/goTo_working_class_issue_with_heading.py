#!/usr/bin/python
import numpy as np
from crazyflie_py import *

swarm = Crazyswarm()
timeHelper = swarm.timeHelper
allcfs = swarm.allcfs

class flying_utility:
    def __init__(self):
        # initiate array of drone positions
        self.pos = np.zeros((len(allcfs.crazyflies), 3))
        self.pos_saved = np.zeros((len(allcfs.crazyflies), 3))
        for idx, cf in enumerate(allcfs.crazyflies):
            self.pos[idx, :] = cf.initialPosition
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
        for idx, cf in enumerate(allcfs.crazyflies):
            self.swarm_pos_saved[idx] = self.swarm_pos[idx] # saving the momentary position
            heading = self.calculate_heading(self.pos_saved[idx], self.pos[idx]) # calculate the heading from momentary position to desired position
            self.pos[idx] = self.rotation_matrix(heading, self.pos[idx])
            self.pos[idx] += desired_pos
            cf.goTo(self.pos[idx], heading, time)
            print(f"fly: cf0{idx+1} going to {desired_pos}")
        print(f"fly: wating for {time}")
        timeHelper.sleep(time*10)

def main():
    fly_util = flying_utility()
    
    # waypoints
    home_hover = np.array([0, 0, 0.5])
    start = np.array([-1, 0, 1])
    pos1 = np.array([0, 1, 1.75])
    pos2 = np.array([0, -1, 0.5])
    end = np.array([1, 0, 1])
    print(f"main: waypoint mission through {home_hover, start, pos1, pos2, end, home_hover}")

    
    # takeoff
    allcfs.takeoff(targetHeight=0.5, duration=1.0)
    print("main: takeoff")
    timeHelper.sleep(20.0)

    # go hover over home
    fly_util.fly(home_hover, 3.0)
    fly_util.fly(start, 3.0)
    fly_util.fly(pos1, 3.0)

    # land
    allcfs.land(targetHeight=0.02, duration=1.0)
    print("main: land")
    timeHelper.sleep(20.0)

if __name__ == "__main__":
    main()