#!/usr/bin/python
import numpy as np
from crazyflie_py import *

def main():
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    initial_pos = np.array([0, 0, 0.5])
    start = np.array([-1, 0, 1])
    left = np.array([0, 1, 1.75])
    right = np.array([0, -1, 0.5])
    end = np.array([1, 0, 1])

    # takeoff
    allcfs.takeoff(targetHeight=0.5, duration=3.0)
    timeHelper.sleep(3.0)

    # go to initial positions
    for cf in allcfs.crazyflies:
        pos = np.array(cf.initialPosition) + initial_pos
        cf.goTo(pos, 0, 3.0)
    timeHelper.sleep(3.0)

    # go to start of course
    cf1 = allcfs.crazyflies[0]
    cf2 = allcfs.crazyflies[1]

    pos1 = np.array(cf1.initialPosition) + start
    cf1.goTo(pos1, 0, 5.0)

    pos2 = np.array(cf2.initialPosition) + start
    cf2.goTo(pos2, 0, 5.0)

    timeHelper.sleep(5.0)

    # go to left
    cf1 = allcfs.crazyflies[0]
    cf2 = allcfs.crazyflies[1]

    pos1 = np.array(cf1.initialPosition) + left
    cf1.goTo(pos1, 0, 5.0)

    pos2 = np.array(cf2.initialPosition) + left
    cf2.goTo(pos2, 0, 5.0)

    timeHelper.sleep(5.0)

    # go to right
    cf1 = allcfs.crazyflies[0]
    cf2 = allcfs.crazyflies[1]

    pos1 = np.array(cf1.initialPosition) + right
    cf1.goTo(pos1, 0, 5.0)

    pos2 = np.array(cf2.initialPosition) + right
    cf2.goTo(pos2, 0, 5.0)

    timeHelper.sleep(5.0)

    # go to end of course
    cf1 = allcfs.crazyflies[0]
    cf2 = allcfs.crazyflies[1]

    pos1 = np.array(cf1.initialPosition) + end
    cf1.goTo(pos1, 0, 5.0)

    pos2 = np.array(cf2.initialPosition) + end
    cf2.goTo(pos2, 0, 5.0)

    timeHelper.sleep(5.0)

    # go home
    cf1 = allcfs.crazyflies[0]
    cf2 = allcfs.crazyflies[1]

    pos1 = np.array(cf1.initialPosition) + initial_pos
    cf1.goTo(pos1, 0, 5.0)

    pos2 = np.array(cf2.initialPosition) + initial_pos
    cf2.goTo(pos2, 0, 5.0)

    timeHelper.sleep(5.0)

    # land
    allcfs.land(targetHeight=0.02, duration=3.0)
    timeHelper.sleep(3.0)

if __name__ == "__main__":
    main()