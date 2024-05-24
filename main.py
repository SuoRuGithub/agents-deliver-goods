'''
In this script, we init the game at first (generate a map, generate some agents)
then, we'll call centre control and find the solution
at last, we visualize that
'''
from utils.map import Map
from utils.agent import Agent
from utils.centre_control import CentreControl
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap

AGENT_NUM = 3
GOODS_NUM = 10

MAP_SIZE = (13, 13)
OBSTACLE_RATIO = 0.1

colors = [(1, 1, 1), (0, 0, 0), (0.5, 0, 1), (1, 0, 0)] #white, black, purple, red
my_cmap = ListedColormap(colors)
bound = [0, 1, 2, 3]

def main():
    map = Map(MAP_SIZE, OBSTACLE_RATIO, GOODS_NUM)
    centre_control = CentreControl(AGENT_NUM, GOODS_NUM, map)
    Solution = centre_control.Solution_find(map)
    print("found a solution!")
    print(Solution)
    # Visualization
    # this random Solution is used for test
    #STEPS = 50
    #Solution = np.random.rand(AGENT_NUM, STEPS, 2) * MAP_SIZE[0]

    fig, ax = plt.subplots()
    im = ax.imshow(map.map_matrix, cmap = my_cmap)
    scatters = [ax.plot([], [], 'o')[0] for _ in range(AGENT_NUM)]
    def init():
        ax.set_xlim(-0.5, MAP_SIZE[0] - 0.5)
        ax.set_ylim(-0.5, MAP_SIZE[1] - 0.5)
        for scatter in scatters:
            scatter.set_data([], [])
        return scatters
    def update(frame):
        for i, scatter in enumerate(scatters):
            scatter.set_data(Solution[i][frame][1], Solution[i][frame][0])
        return scatters

    visualizer = FuncAnimation(fig, update, frames = len(Solution[0]), init_func = init, interval = 1000, blit = True)
    plt.show()
    visualizer.save('demo.gif', writer = 'ffmpeg')

if __name__ == "__main__":
    main()