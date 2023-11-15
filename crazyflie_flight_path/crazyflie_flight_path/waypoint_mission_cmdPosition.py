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
        pos_goal = np.array([-1.0, 1.0, 0.1])
        cf.cmdPosition(pos_goal, 0.0)

    # drone falls out of the air after reaching position...
        
    # # possibility to do an emergency glide to the ground after command is sent
    # print("press button in the next 5 seconds to declare emergency")
    # for t in range(1, T_move+1):
    #     print(t)
    #     if swarm.input.checkIfButtonIsPressed():
    #         cf.emergency()
    #     timeHelper.sleep(1)

    print("press button to go home")
    swarm.input.waitUntilButtonPressed()

    for cf in allcfs.crazyflies:
        pos_over_home = np.array(cf.initialPosition) + np.array([0, 0, 0.1])
        cf.cmdPosition(pos_over_home, 0.0)

    # # # possibility to do an emergency glide to the ground after command is sent
    # # print("press button in the next 5 seconds to declare emergency")
    # # for t in range(1, T_move+1):
    # #     print(t)
    # #     if swarm.input.checkIfButtonIsPressed():
    # #         cf.emergency()
    # #     timeHelper.sleep(1)

    # print("press button to land")
    # swarm.input.waitUntilButtonPressed()

    # allcfs.land(targetHeight=0.02, duration=T)

    # timeHelper.sleep(T)

if __name__ == "__main__":
    main()