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
from matplotlib.animation import FuncAnimation, writers
from matplotlib.colors import ListedColormap

AGENT_NUM = 20
GOODS_NUM = 200
MAP_SIZE = (128, 128)
OBSTACLE_RATIO = 0.2

colors = [(1, 1, 1), (0, 0, 0), (0.5, 0, 1), (1, 0, 0)] #white, black, purple, red
my_cmap = ListedColormap(colors)
bound = [0, 1, 2, 3]


def main():
    map = Map(MAP_SIZE, OBSTACLE_RATIO, GOODS_NUM)
    centre_control = CentreControl(AGENT_NUM, map)
    # for test
    # colors = [(1, 1, 1), (0, 0, 0), (0.5, 0, 1), (1, 0, 0)] #white, black, purple, red
    # my_cmap = ListedColormap(colors)
    # bound = [0, 1, 2, 3]
    # fig, ax = plt.subplots()
    # im = ax.imshow(map.map_matrix, cmap=my_cmap)
    # birth = [[agent.birth_place[0] for agent in centre_control.agents], [agent.birth_place[1] for agent in centre_control.agents]]
    # ax.scatter(birth[1], birth[0])
    # plt.show()
    
    Solution = centre_control.Solution_find(map)
    print("GOODS_LEFT", map.goods_left)
    print("found a solution!")
    print(Solution)
    # Visualization
    fig, ax = plt.subplots()
    im = ax.imshow(map.map_matrix, cmap = my_cmap)
    scatters = [ax.plot([], [], 'o', markersize = 1)[0] for _ in range(AGENT_NUM)]
    def init():
        ax.set_xlim(-0.5, MAP_SIZE[0] - 0.5)
        ax.set_ylim(-0.5, MAP_SIZE[1] - 0.5)
        for scatter in scatters:
            scatter.set_data([], [])
        return scatters
    def update(frame):
        for i, scatter in enumerate(scatters):
            x = Solution[i][int(frame // 10)][1] + (Solution[i][int((frame + 10) // 10)][1] - Solution[i][int(frame // 10)][1]) * (frame % 10) / 10
            y = Solution[i][int(frame // 10)][0] + (Solution[i][int((frame + 10) // 10)][0] - Solution[i][int(frame // 10)][0]) * (frame % 10) /10
            scatter.set_data(x, y)
            # scatter.set_data(Solution[i][frame / 10 + frame - ][1], Solution[i][frame / 10][0])   # discrete
        return scatters

    visualizer = FuncAnimation(fig, update, frames = 10 * (len(Solution[0]) - 1), init_func = init, interval = 2, blit = True)
    plt.show()
    visualizer.save('demo.gif', writer = 'ffmpeg')

    FFMpegWriter = writers['ffmpeg']
    writer = FFMpegWriter(fps=60, metadata=dict(title='demo video', artist='zzpku', comment="hope this work"), bitrate=1800)
    visualizer.save('demo.mp4', writer=writer)



if __name__ == "__main__":
    main()