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

    # takeoff
    allcfs.takeoff(targetHeight=0.5, duration=3.0)
    timeHelper.sleep(3.0)

    # go to initial positions
    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + np.array([0, 0, 0.5])
        cf.goTo(pos, 0, 3.0)
    timeHelper.sleep(3.0)

    # go to start of course
    cf1 = allcfs.crazyflies[0]
    cf2 = allcfs.crazyflies[1]

    pos1 = np.array(cf1.initialPosition) + np.array([-1, 0, 1])
    cf1.goTo(pos1, 0, 5.0)

    pos2 = np.array(cf2.initialPosition) + np.array([-1, 0, 1])
    cf2.goTo(pos2, 0, 5.0)

    timeHelper.sleep(5.0)

    # go to end of course
    cf1 = allcfs.crazyflies[0]
    cf2 = allcfs.crazyflies[1]

    pos1 = np.array(cf1.initialPosition) + np.array([1, 0, 1])
    cf1.goTo(pos1, np.pi, 5.0)

    pos2 = np.array(cf2.initialPosition) + np.array([1, 0, 1])
    cf2.goTo(pos2, np.pi, 5.0)

    timeHelper.sleep(5.0)

    # go home
    cf1 = allcfs.crazyflies[0]
    cf2 = allcfs.crazyflies[1]

    pos1 = np.array(cf1.initialPosition) + np.array([0, 0, 0.5])
    cf1.goTo(pos1, 0, 5.0)

    pos2 = np.array(cf2.initialPosition) + np.array([0, 0, 0.5])
    cf2.goTo(pos2, 0, 5.0)

    timeHelper.sleep(5.0)

    # land
    allcfs.land(targetHeight=0.02, duration=3.0)
    timeHelper.sleep(3.0)

if __name__ == "__main__":
    main()

# as seen on: https://github.com/IMRCLab/crazyswarm2/discussions/357#discussioncomment-7580976