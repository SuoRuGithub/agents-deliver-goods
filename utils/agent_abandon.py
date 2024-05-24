'''
This script defines class Agent
All agents can find their own optimal path with A* algorithm
Then, center control will find conflicts between paths and fix them
'''
from map import Map
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
from queue import Queue

class Node():
    '''
    Used for path finding algorithm. 
    - position: position of node
    - parent, child: parent node and child node
    - cost_so_far: represent g(n)   (in our project, every step costs equally, say 1)
    - heuristic: represent h(n)     (we use Manhattan Distance for heuristic)
    - total cost: represent f(n) = g(n) + h(n)
    '''
    def __init__(self, position, parent, target):
        self.position = position
        self.target = target
        self.parent = parent
        self.cost_so_far = self.parent.cost_so_far + 1 if parent != None else 0
        self.heuristic = abs(position[0] - target[0]) + abs(position[1] - target[1])
        self.total_cost = self.cost_so_far + self.heuristic
    
    def __lt__(self, other):
        '''
        we have to define __lt__ function such that we could use min funtion to find the top prior node
        '''
        return self.total_cost < other.total_cost
    
    def find_neighbours(self, map_matrix):
        # traverse all 4 nodes around it, return a list of legal neighbours
        # I wrote a shit code to complete this function, luckily, ChatGLM help me improved it
        pos = self.position
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        neighbours = list()
        width = map_matrix.shape[0]
        height = map_matrix.shape[1]
        for dx, dy in directions:
            new_x = pos[0] + dx
            new_y = pos[1] + dy
            if 0 <= new_x < width and 0 <= new_y < height and map_matrix[new_x, new_y] != 1:    # could equal 0, 2, 3
                neighbours.append(Node((new_x, new_y), self, self.target))
        return neighbours

def find_next(open_list):
    '''
    traverse all the nodes in the open_list, choose the top priority one, ~~and then remove it(nope)~~
    '''
    node = min(open_list)
    # open_list.remove(node)
    return node

def A_star_path_finding(game_map, start, target):
    '''
    This function return a shortest path from start to target
    the path is represent as a list of tuple.

    notes: in our algorithm, the matrix is dynamic based on the origin matrix and restraince
    ''' 
    open_list = list()      
    open_list.append(Node(start, None, target))
    closed_list = list()
    end_node = None
    path = list()
    while end_node == None and len(open_list) != 0:
        # print(len(open_list))
        node = find_next(open_list)     # you can easily choose your path-finding algorithm by modifying find_next function
        open_list.remove(node)
        closed_list.append(node)
        neighbours = node.find_neighbours(game_map.map_matrix)
        for neighbour in neighbours:    # add neighbours to open list
            if neighbour.position == target:
                end_node = neighbour
                break
            # if  neighbour not in closed_list:       # what a piece of shit have u written? you should take position as creterion, not the position!
            if not any(node.position == neighbour.position for node in closed_list):
                open_list.append(neighbour)
    if end_node != None:
        # We can get path by trace back
        print(end_node.position)
        print(end_node.parent)
        node = end_node
        while node.parent != None:
            path.append(node.position)
            node = node.parent      # I forget this shit
        path.reverse()
    return path

class Agent():
    def __init__(self, game_map):
        # random.seed(42)  # for test
        non_ob_pos = np.argwhere(map.map_matrix == 0)
        self.position = tuple(non_ob_pos[random.randint(0, len(non_ob_pos))])
        self.is_load = False

# for test

MAP_SIZE = (32, 32)
OBSTACLE_RATIO = 0.2
map = Map(MAP_SIZE, OBSTACLE_RATIO)
agent1 = Agent(map)
path = A_star_path_finding(map, agent1.position, map.repo_pos1)
fig, ax, im= map.init_map()

x, y = path[0]
square, = ax.plot(y, x, 's', color = 'red', ) # What the fuck? which genius developer have the idea that in plt.imshow, y is ahead, but in plot, x is ahead??????? 

def init():
    ax.set_xlim(0, 32)
    ax.set_ylim(0, 32)
    ax.set_label("Multiple Agent Path Finding")
    return 

def update(frame):
    '''
    update our animation
    '''
    global x, y
    if frame < len(path):
        x, y = path[frame][0], path[frame][1]
        square.set_data(y, x)
    return square,

visualizer = FuncAnimation(fig, update, frames = 1000, interval = 500, blit = True)
plt.show()



