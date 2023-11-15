#!/usr/bin/env python

import numpy as np
from crazyflie_py import *


def main():
    Z = 1.0
    T = 3
    T_move = 5
    
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs
    print("take off in")
    for t in range(3, 0, -1):
        print(t)
        timeHelper.sleep(1)
    print("we have liftoff")

    allcfs.takeoff(targetHeight=Z, duration=T)

    timeHelper.sleep(T)

    for cf in allcfs.crazyflies:
        pos_over_home = np.array(cf.initialPosition) + np.array([0, 0, Z])
        pos_goal = pos_over_home + np.array([-1, 1, 0])
        cf.goTo(pos_goal, 0, T_move)

    print("press button to hover over home")
    swarm.input.waitUntilButtonPressed()

    for cf in allcfs.crazyflies:
        pos_over_home = np.array(cf.initialPosition) + np.array([0, 0, Z])
        cf.goTo(pos_over_home, 0, T_move)

    timeHelper.sleep(T_move)

    print("press button to land")
    swarm.input.waitUntilButtonPressed()

    allcfs.land(targetHeight=0.02, duration=T)

    timeHelper.sleep(T)

if __name__ == "__main__":
    main()