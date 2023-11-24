#!/usr/bin/env python

#   █     █░ ▒█████   ██▀███   ██ ▄█▀    ██▓ ███▄    █     ██▓███   ██▀███   ▒█████    ▄████  ██▀███  ▓█████   ██████   ██████ 
#  ▓█░ █ ░█░▒██▒  ██▒▓██ ▒ ██▒ ██▄█▒    ▓██▒ ██ ▀█   █    ▓██░  ██▒▓██ ▒ ██▒▒██▒  ██▒ ██▒ ▀█▒▓██ ▒ ██▒▓█   ▀ ▒██    ▒ ▒██    ▒ 
#  ▒█░ █ ░█ ▒██░  ██▒▓██ ░▄█ ▒▓███▄░    ▒██▒▓██  ▀█ ██▒   ▓██░ ██▓▒▓██ ░▄█ ▒▒██░  ██▒▒██░▄▄▄░▓██ ░▄█ ▒▒███   ░ ▓██▄   ░ ▓██▄   
#  ░█░ █ ░█ ▒██   ██░▒██▀▀█▄  ▓██ █▄    ░██░▓██▒  ▐▌██▒   ▒██▄█▓▒ ▒▒██▀▀█▄  ▒██   ██░░▓█  ██▓▒██▀▀█▄  ▒▓█  ▄   ▒   ██▒  ▒   ██▒
#  ░░██▒██▓ ░ ████▓▒░░██▓ ▒██▒▒██▒ █▄   ░██░▒██░   ▓██░   ▒██▒ ░  ░░██▓ ▒██▒░ ████▓▒░░▒▓███▀▒░██▓ ▒██▒░▒████▒▒██████▒▒▒██████▒▒
#  ░ ▓░▒ ▒  ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░▒ ▒▒ ▓▒   ░▓  ░ ▒░   ▒ ▒    ▒▓▒░ ░  ░░ ▒▓ ░▒▓░░ ▒░▒░▒░  ░▒   ▒ ░ ▒▓ ░▒▓░░░ ▒░ ░▒ ▒▓▒ ▒ ░▒ ▒▓▒ ▒ ░
#    ▒ ░ ░    ░ ▒ ▒░   ░▒ ░ ▒░░ ░▒ ▒░    ▒ ░░ ░░   ░ ▒░   ░▒ ░       ░▒ ░ ▒░  ░ ▒ ▒░   ░   ░   ░▒ ░ ▒░ ░ ░  ░░ ░▒  ░ ░░ ░▒  ░ ░
#    ░   ░  ░ ░ ░ ▒    ░░   ░ ░ ░░ ░     ▒ ░   ░   ░ ░    ░░         ░░   ░ ░ ░ ░ ▒  ░ ░   ░   ░░   ░    ░   ░  ░  ░  ░  ░  ░  
#      ░        ░ ░     ░     ░  ░       ░           ░                ░         ░ ░        ░    ░        ░  ░      ░        ░  

import numpy as np
from pathlib import Path

from crazyflie_py import *
from crazyflie_py.uav_trajectory import Trajectory

def main():
    swarm = Crazyswarm()
    timeHelper = swarm.timeHelper
    allcfs = swarm.allcfs

    traj1 = Trajectory()
    traj1.loadcsv(Path(__file__).parent / "data/spiral_cf01.csv")

    traj2 = Trajectory()
    traj2.loadcsv(Path(__file__).parent / "data/spiral_cf02.csv")

    TIMESCALE = 0.5

    cf1 = allcfs.crazyflies[0]
    # cf2 = allcfs.crazyflies[1]

    cf1.uploadTrajectory(0, 0, traj2)
    # cf2.uploadTrajectory(0, 0, traj1)
    print("upload")

    cf1.takeoff(targetHeight=1.5, duration=3.0)
    # cf2.takeoff(targetHeight=1.5, duration=3.0)
    print("takeoff")

    timeHelper.sleep(5.0)

    # go home
    cf1 = allcfs.crazyflies[0]
    # cf2 = allcfs.crazyflies[1]

    pos1 = np.array(cf1.initialPosition) + np.array([0, 0, 0.5])
    cf1.goTo(pos1, 0, 5.0)

    # pos2 = np.array(cf2.initialPosition) + np.array([0, 0, 0.5])
    # cf2.goTo(pos2, 0, 5.0)

    timeHelper.sleep(5.0)

    # # assigning starting position & going there
    # number_of_drones = 2
    # elevation = 1.5
    # radius = 0.4 # radius of spiral in csv
    # start_pos = []
    # for drone_count in range(number_of_drones):
    #     delta_angle = (2 * np.pi) * (drone_count / number_of_drones)
    #     angle = 2 * np.pi + delta_angle
    #     x = 0.0
    #     y = radius * np.cos(angle)
    #     z = radius * np.sin(angle) + elevation
    #     start_pos.append(np.array([x, y, z]))
        
    #     print(f"coordinates of start for cf{drone_count+1} ",f"{x},{y},{z}")

    # # for cf in allcfs.crazyflies:
    # #     cf.goTo(start_pos[int(cf)-1], 0, 2.0)

    # cf1.goTo(start_pos[0], 0, 2.0)
    # cf1.goTo(start_pos[0], 0, 2.0)
    # print("going to starting position")
    
    # timeHelper.sleep(3.0)

    cf1.startTrajectory(0, timescale=TIMESCALE)
    # cf2.startTrajectory(0, timescale=TIMESCALE)
    print("start trajectory")

    timeHelper.sleep(traj1.duration * TIMESCALE + 10.0)

    # go home
    cf1 = allcfs.crazyflies[0]
    # cf2 = allcfs.crazyflies[1]

    pos1 = np.array(cf1.initialPosition) + np.array([0, 0, 0.5])
    cf1.goTo(pos1, 0, 5.0)

    # pos2 = np.array(cf2.initialPosition) + np.array([0, 0, 0.5])
    # cf2.goTo(pos2, 0, 5.0)

    timeHelper.sleep(5.0)

    cf1.land(targetHeight=0.06, duration=3.0)
    # cf2.land(targetHeight=0.06, duration=3.0)
    print("landing")
    timeHelper.sleep(3.0)


if __name__ == "__main__":
    main()
