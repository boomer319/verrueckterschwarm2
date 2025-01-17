#!/usr/bin/python
import numpy as np
from crazyflie_py import *
# import subprocess 
# import shutil
# import os

def main():
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    # allcfs.setParam("colAv.enable", 1)

    # allcfs.setParam("colAv.ellipsoidX", 0.10)
    # allcfs.setParam("colAv.ellipsoidY", 0.10)
    # allcfs.setParam("colAv.ellipsoidZ", 0.3)

    # timeHelper.sleep(10.0)

    # for the flight part
    allcfs.takeoff(targetHeight=0.5, duration=3.0)
    print("takeoff")
    timeHelper.sleep(3.0)

    # go to initial positions
    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([0, 0, 0.5])
        cf.goTo(pos, 0, 5.0)
    print("going over home")
    timeHelper.sleep(5.0)

    # swap positions
    cf1 = allcfs.crazyflies[0]
    cf2 = allcfs.crazyflies[1]

    pos1 = np.array(cf2.initialPosition) + np.array([0, 0, 0.5])
    cf1.goTo(pos1, 0, 5.0)

    pos2 = np.array(cf1.initialPosition) + np.array([0, 0, 0.5])
    cf2.goTo(pos2, 0, 5.0)

    print("swapping positions")

    timeHelper.sleep(8.0)

    # # swap positions (again)
    # cf1 = allcfs.crazyflies[0]
    # cf2 = allcfs.crazyflies[1]

    # pos1 = np.array(cf1.initialPosition) + np.array([0, 0, 0.5])
    # cf1.goTo(pos1, 0, 5.0)

    # pos2 = np.array(cf2.initialPosition) + np.array([0, 0, 0.5])
    # cf2.goTo(pos2, 0, 5.0)

    # print("move 2")

    # timeHelper.sleep(8.0)

    # # meet at one point
    # cf1 = allcfs.crazyflies[0]
    # cf2 = allcfs.crazyflies[1]

    # pos1 = np.array(cf1.initialPosition) + np.array([-2, 0, 0.5])
    # cf1.goTo(pos1, 0, 5.0)

    # pos2 = pos1
    # cf2.goTo(pos2, 0, 5.0)

    # print("move 3")

    # timeHelper.sleep(8.0)

    # go home
    cf1 = allcfs.crazyflies[0]
    cf2 = allcfs.crazyflies[1]

    pos1 = np.array(cf1.initialPosition) + np.array([0, 0, 0.5])
    cf1.goTo(pos1, 0, 5.0)

    pos2 = np.array(cf2.initialPosition) + np.array([0, 0, 0.5])
    cf2.goTo(pos2, 0, 5.0)

    timeHelper.sleep(5.0)
    
    # # moving cf2 into cf1
    # cf1 = allcfs.crazyflies[0]
    # cf2 = allcfs.crazyflies[1]

    # pos1 = np.array(cf1.initialPosition) + np.array([0, 0, 0.5])
    # cf1.goTo(pos1, 0, 5.0)

    # pos2 = pos1
    # cf2.goTo(pos2, 0, 5.0)

    # timeHelper.sleep(8.0)

    allcfs.land(targetHeight=0.02, duration=3.0)
    timeHelper.sleep(3.0)

if __name__ == "__main__":
    main()

# as seen on: https://github.com/IMRCLab/crazyswarm2/discussions/357#discussioncomment-7580976