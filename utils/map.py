'''
This script defines class Map.
The map is a matrix of size 32x32, where 1 denotes obstacle and 0 denote non-obstacle. Besides, there are "2" and "3" 
in the map matrix represent repository A and repository B respectively
'''
import matplotlib.pyplot as plt
import numpy as np
# from matplotlib.animation import FuncAnimation

from matplotlib.colors import ListedColormap
MAP_SIZE = (32, 32)
OBSTACLE_RATIO = 0.2
GOODS_NUM = 40


class Map():
    def __init__(self, map_size, obstacle_ratio, GOODS_NUM):
        np.random.seed(42)  # for test
        
        map_matrix = np.random.choice([0, 1], size = map_size, p = [1 - obstacle_ratio, obstacle_ratio])
        self.repo_pos1 = tuple(np.random.randint(0, map_size))
        self.repo_pos2 = tuple(np.random.randint(0, map_size))
        while abs(self.repo_pos2[0] - self.repo_pos1[0]) + abs(self.repo_pos2[1] - self.repo_pos1[1]) < 0.2 * map_size[0]:  # 本来我只设置了禁止两者位置相同，但是我发现两者位置太近也会导致奇奇怪怪的bug   
            self.repo_pos2 = tuple(np.random.randint(0, map_size))
        map_matrix[self.repo_pos1] = 2
        map_matrix[self.repo_pos2] = 3
        self.map_matrix = map_matrix
        self.goods_left = GOODS_NUM
    #def init_map(self):
    #    fig, ax = plt.subplots()
    #    im = ax.imshow(self.map_matrix, cmap='tab20c')
    #    return fig, ax, im

# for test
'''
colors = [(1, 1, 1), (0, 0, 0), (0.5, 0, 1), (1, 0, 0)] #white, black, purple, red
my_cmap = ListedColormap(colors)
bound = [0, 1, 2, 3]
map = Map(MAP_SIZE, OBSTACLE_RATIO, GOODS_NUM)
fig, ax = plt.subplots()
im = ax.imshow(map.map_matrix, cmap=my_cmap)
plt.show()
'''