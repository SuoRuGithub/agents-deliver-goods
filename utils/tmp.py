#coding=gbk
'''
This script defines class Agent
All agents can find their own optimal path with A* algorithm
Then, center control will find conflicts between paths and fix them
'''
from utils.map import Map   # When you want to import this package to main, use this line
#from map import Map       # When you want to write code in this file, use this line, don't ask me why, idk
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
    - cost_so_far: represent g(n)   (in our project, every step costs equally, say 1)
    - heuristic: represent h(n)     (we use Manhattan Distance for heuristic)
    - total cost: represent f(n) = g(n) + h(n)
    '''
    def __init__(self, position, parent, target):
        self.position = position
        self.target = target
        self.parent = parent
        self.cost_so_far = self.parent.cost_so_far + 1 if parent != None else 0 # in fact, this is cost of time, not distance, so cost++ even when agent just stay
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
        # neighbours.append(self) # I don't know if it will work
        return neighbours

def find_next(open_list, constraints_table):
    '''
    traverse all the nodes in the open_list, choose the top priority one, ~~and then remove it(nope)~~
    '''
    # 我们首先还是要去把冲突的结点移出去（但是注意，不可以移动到Closed——list里面，因为以后也许还可以走）
    '''for node in open_list:  
        t = node.cost_so_far
        for key in constraints_table:
            if t == key:
                t_constraints = constraints_table[key]
                for pos in t_constraints:
                    if node.position == pos:
                        open_list.pop(node)'''
    node = min(open_list)
    # open_list.remove(node)
    return node

class Agent():
    def __init__(self, game_map: Map, id):
        # random.seed(42)  # for test
        non_ob_pos = np.argwhere(game_map.map_matrix == 0)
        self.position = tuple(non_ob_pos[random.randint(0, len(non_ob_pos) - 1)])
        self.is_load = False
        self.target = game_map.repo_pos1    # Originally, agent is not loaded and target to repo A
        self.path = None
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
    def make_constraints_table(self, constraints, id):
        '''
        This function will take all constraints in consider and make a contraints table
        this table tell the agent when it could not stay in what place
        constraints_table: {
            t_1: vetex_1,
            t_2: vetex_2,
            ...
        }
        p.s. constraint like: (i, (x, y), t)
        '''
        constraints_table = dict()
        if not constraints:
            return constraints_table
        for constraint in constraints:
            timestep = constraint[2]    # Go fuck yourself, how dare you spell constraint as constraints?
            t_constraint = []
            if timestep in constraints_table:
                t_constraint = constraints_table[timestep]
            
            if id == constraint[0]:
                t_constraint.append(constraint[1])
                constraints_table[timestep] = t_constraint
        return constraints_table

    def A_star_path_finding(self, game_map, constraints, id):   # id is the num the this agent
        '''
        This function return a shortest path from start to target
        the path is represent as a list of tuple.

        notes: in our algorithm, the matrix is dynamic based on the origin matrix and restraince
        ''' 
        constraints_table = self.make_constraints_table(constraints, id)


        if self.position == self.target:
            self.path = None    # this may happen when this agent's tasks conclued earlier than others
            return 
        open_list = list()      
        open_list.append(Node(self.position, None, self.target))
        closed_list = list()
        end_node = None
        path = list()
        while end_node == None and len(open_list) != 0:
            node = find_next(open_list, constraints_table)     # you can easily choose your path-finding algorithm by modifying find_next function
            open_list.remove(node)
            closed_list.append(node)
            neighbours = node.find_neighbours(game_map.map_matrix)
            for neighbour in neighbours:    # add neighbours to open list
                if neighbour.position == self.target:
                    end_node = neighbour
                    break
                # if  neighbour not in closed_list:       # what a piece of shit have u written? you should take position as creterion, not the position!
                if not any(node.position == neighbour.position for node in closed_list):
                    open_list.append(neighbour)
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
'''
MAP_SIZE = (40, 40)
OBSTACLE_RATIO = 0.1
GOODS_NUM = 40
colors = [(1, 1, 1), (0, 0, 0), (0.5, 0, 1), (1, 0, 0)] #white, black, purple, red
my_cmap = ListedColormap(colors)
map = Map(MAP_SIZE, OBSTACLE_RATIO, GOODS_NUM)
agent1 = Agent(map)
agent1.A_star_path_finding(map, [], 0)
path = agent1.path
steps = len(path)
print("Found Path: ",path)



fig, ax = plt.subplots()
im = ax.imshow(map.map_matrix, cmap = my_cmap)

x, y = path[0]
square, = ax.plot(y, x, 's', color = 'red', ) # What the fuck? which genius developer have the idea that in plt.imshow, y is ahead, but in plot, x is ahead??????? 

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
'''