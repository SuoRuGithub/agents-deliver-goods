#coding=gbk
'''
This script defines class Agent
All agents can find their own optimal path with A* algorithm
Then, center control will find conflicts between paths and fix them
'''
# from utils.map import Map   # When you want to import this package to main, use this line
from map import Map       # When you want to write code in this file, use this line, don't ask me why, idk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
from queue import Queue
from matplotlib.colors import ListedColormap

class Node():
    '''
    Used for path finding algorithm. 
    - position: position of node
    - parent, child: parent node and child node
    - time: the dimension of time, in fact, it equals cost_so_far
    - cost_so_far: represent g(n)   (in our project, every step costs equally, say 1)
    - heuristic: represent h(n)     (we use Manhattan Distance for heuristic)
    - total cost: represent f(n) = g(n) + h(n)
    '''
    def __init__(self, position, parent, target, time):
        self.position = position
        self.target = target
        self.parent = parent
        self.cost_so_far = self.parent.cost_so_far + 1 if parent != None else 0 # in fact, this is cost of time, not distance, so cost++ even when agent just stay
        self.time = time
        self.heuristic = abs(position[0] - target[0]) + abs(position[1] - target[1])    
        self.total_cost = self.heuristic + self.cost_so_far
    
    def __lt__(self, other):
        '''
        we have to define __lt__ function such that we could use min funtion to find the top prior node
        '''
        if self.total_cost == other.total_cost:
            return self.heuristic < other.heuristic # I don't know why, but it works! without this line, this program will spend a looooooooooooooooooooooong time to run
        else:
            return self.total_cost < other.total_cost
    
    def find_neighbours(self, map_matrix, time, constraints, id):
        # traverse all 4 nodes around it, return a list of legal neighbours
        # I wrote a shit code to complete this function, luckily, ChatGLM help me improved it
        # ---
        # in STA* algorithm, we should take constraints into account, if all direction are blocked, 
        # we should return current node.
        t_constraint = []
        for constraint in constraints:
            if constraint[2] == time + 1 and constraint[1] == id:   
                t_constraint.append(constraint[2])  # t_constraint is a list of position that are forbidden **for this agent at next time t**, like: [(1, 2), ...]

        pos = self.position
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        neighbours = list()
        width = map_matrix.shape[0]
        height = map_matrix.shape[1]
        for dx, dy in directions:
            new_x = pos[0] + dx
            new_y = pos[1] + dy
            if 0 <= new_x < width \
                and 0 <= new_y < height \
                and map_matrix[new_x, new_y] != 1\
                and (new_x, new_y) not in t_constraint:    # could equal 0, 2, 3
                neighbours.append(Node((new_x, new_y), self, self.target, time + 1))
        # neighbours.append(self) # I don't know if it will work
        if neighbours:
            return neighbours
        else:
            return [self]    # if there are no neighbours, just stay.

def find_next(open_list):
    '''
    traverse all the nodes in the open_list, choose the top priority one, ~~and then remove it(nope)~~
    '''
    node = min(open_list)
    # open_list.remove(node)
    return node

class Agent():
    def __init__(self, game_map: Map, id = 0):  # I add id
        # random.seed(42)  # for test
        non_ob_pos = np.argwhere(game_map.map_matrix == 0)
        self.position = tuple(non_ob_pos[random.randint(0, len(non_ob_pos) - 1)])
        self.is_load = False
        self.target = game_map.repo_pos1    # Originally, agent is not loaded and target to repo A
        self.path = None
        self.id = id
    def update_state(self, game_map):
        '''
        This function change agent's target based on if it is loaded and how much goods left
        '''
        if self.is_load == True:
            self.target = game_map.repo_pos2
        elif game_map.goods_left != 0:
            self.target = game_map.repo_pos1
        elif game_map.goods_left == 0:
            self.target = game_map.repo_pos1    # we suppose, all agent should go to pos1 after the whole process

    def A_star_path_finding(self, game_map, constraints):   # id is the num the this agent
        '''
        This function return a shortest path from start to target
        the path is represent as a list of tuple.

        notes: in our algorithm, the matrix is dynamic based on the origin matrix and restraince
        ''' 

        if self.position == self.target:
            self.path = [self.position]    # this may happen when this agent's tasks conclued earlier than others
            return 

        open_list = list()
        time = 0      
        open_list.append(Node(self.position, None, self.target, time)) # plus a time dimension
        closed_list = list()
        end_node = None
        path = list()

        iter_for_test = 0
        while end_node == None and len(open_list) != 0 and iter_for_test < 500:
            node = find_next(open_list)     # you can easily choose your path-finding algorithm by modifying find_next function
            print(node.position)
            open_list.remove(node)
            closed_list.append(node.position)   # we cant append node, that will stuck in infinite loop
            neighbours = node.find_neighbours(game_map.map_matrix, time, constraints, self.id)
            for neighbour in neighbours:    # add neighbours to open list
                
                if neighbour.position == self.target:
                    end_node = neighbour
                    break
                # if  neighbour not in closed_list:       # what a piece of shit have u written? you should take position as creterion, not the position!
                if neighbour.position not in closed_list:
                
                    print("test")
                    open_list.append(neighbour)
            time += 1
            print(time)

        # for test
        if iter_for_test >= 500:
            print("卡死了")
        
        if end_node != None:
            # We can get path by trace back
            #print(end_node.position)
            #print(end_node.parent)
            node = end_node
            while node.parent != None:
                path.append(node.position)
                node = node.parent      # I forget this shit
            path.reverse()
        self.path = path     # steps是走多少步就走结束了，其实好像就是路径长度?你在想啥？


# for test
MAP_SIZE = (32, 32)
OBSTACLE_RATIO = 0.1
GOODS_NUM = 40
colors = [(1, 1, 1), (0, 0, 0), (0.5, 0, 1), (1, 0, 0)] #white, black, purple, red
my_cmap = ListedColormap(colors)
map = Map(MAP_SIZE, OBSTACLE_RATIO, GOODS_NUM)
agent1 = Agent(map)
agent1.A_star_path_finding(map, [])
path = agent1.path
steps = len(path)
print("Found Path: ",path)

fig, ax = plt.subplots()
im = ax.imshow(map.map_matrix, cmap = my_cmap)

x, y = path[0]
square, = ax.plot(y, x, 's', color = 'red', ) # What the fuck? which genius developer have the idea that in plt.imshow, y is ahead, but in plot, x is ahead??????? 

# plt.show()
def init():
    ax.set_xlim(0, MAP_SIZE[0])
    ax.set_ylim(0, MAP_SIZE[1])
    ax.set_label("Multiple Agent Path Finding")
    return 

def update(frame):
    """
    update our animation
    """
    global x, y
    if frame < len(path):
        x, y = path[frame][0], path[frame][1]
        square.set_data(y, x)
    return square,

visualizer = FuncAnimation(fig, update, frames = steps, interval = 500, blit = True)
plt.show()
