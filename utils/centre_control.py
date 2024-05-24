#coding=gbk
'''
This script defines CentreControl class.
CentreControl knows everything happening in the field. It knows how much goods left, state of every agent,
path of every agent.
CentreControl should assign tasks, find conflicts among every path of each sigle agent, and try to find a solution of 
the global question.
'''
from utils.agent import Agent
# from agent import Agent   # Just in case that you want to test in this file
from utils.map import Map
# from map import Map
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import copy

'''
Here are three classes:
- Node: for CBS
- CBS: find Partial Solution of each step
- CentreControl: find Global Solution of the question
'''

# 有一个问题一直解决不了，我重新写一遍
# 这个Node是什么，Node应该是一个用来计算部分解的东西
# 我们在使用CBS寻找局部解的时候我们就类似与A*算法一样，从一个open_list里面找一个最小代价的Node
class Node():
    def __init__(self, constraints, agents, game_map):
        self.constraints = constraints
        self.agents = agents
        self.game_map = game_map

        self.solution = []
        self.cost = 0
        self.collision = []
        
        steps = []
        for agent in self.agents:
            agent.A_star_path_finding(self.game_map, constraints)
            path = agent.path
            step = len(path)
            self.solution.append(path)
            steps.append(step)
        self.cost = self.get_total_cost()

        min_steps = min(steps)
        self.solution = [path[:min_steps] for path in self.solution]

        self.collision, self.collision_type = self.get_first_collision()
        # 在这里我们不更新约束，更新约束并进行分叉是CBS的事情
    def get_total_cost(self):
        # 这个函数必须在对solution进行截断之前调用，
        # 我们定义总的代价是solution里所有path的长度之和
        cost = 0
        for path in self.solution:
            cost += len(path)
        return cost
    
    def get_first_collision(self):
        # 冲突有两种类型，一种就是两条路径在同一时刻重合在同一点了，另一种更复杂一点，也就是两个路径在一个相邻时刻交换了位置，我们先写好第一种测试一下
        # 冲突应该是这样表示的：(i, j, (x, y), t)
        for t in range(len(self.solution[0])):
            for i in range(len(self.solution) - 1):
                for j in range(i + 1, len(self.solution)):
                    if self.solution[i][t] == self.solution[j][t]:
                        return (i, j, self.solution[i][t], t), 0
        # 不是哥们，你在初始化的时候还得调用自己类里面的一个函数，这个函数还要返回一个值才能改变自己的属性，你不觉得自己很幽默吗？
        # 下面这个是一种更困难的collision：
        # agent1: (x, y) -> (x + 1, y); agent2: (x + 1, y) -> (x, y)
        # 我们需要返回:(1, (x + 1, y), t + 1)或者(2, (x, y), t + 1)理论上返回任意一种都是可以的
        for i in range(len(self.solution) - 1):
            for j in range(i + 1, len(self.solution)):
                for t in range(len(self.solution[0]) - 1):
                    if self.solution[i][t] == self.solution[j][t + 1] \
                        and self.solution[j][t] == self.solution[i][t + 1]:
                        return (i, j, self.solution[i][t], t), 1    # 后面如果是1就代表是相向而行了在这里我的意思是,i ,j在t时刻交换了位置
        # 史山真是越堆越高了，现在已经是头疼医头脚疼医脚了
        # print(len(self.solution))#我是傻逼
        if self.solution and len(self.solution[0]) == 1:
            # print("进来了")
            for i in range(len(self.solution) - 1):
                for j in range(i + 1, len(self.solution)):
                    if self.solution[i][0] == self.agents[j].position \
                        and self.solution[j][0] == self.agents[i].position:
                        # print("进来了")
                        return (i, j, self.solution[i][0], 0), 1
        return None, None

    def split(self):
        # 这个函数将node自己的collision产生一个包含两个约束条件的列表，供CBS生成子节点
        '''
        input: a collision(from function get_collision())
            (i, j, v, t)    # agent i and j at the same vetex at time t
        output: a list of two constraints
            [(i, v, t), (j, v, t)]
        '''
        if self.collision_type == 0:
            # print(self.collision)
            if self.collision:
                return [(self.collision[0], self.collision[2], self.collision[3]), 
                        (self.collision[1], self.collision[2], self.collision[3])]
        elif self.collision_type == 1:
            if self.collision:
                return [(self.collision[0], self.collision[2], self.collision[3])]  # 我觉得只约束一个可能比较好？    
    def __lt__(self, other):
        # 我们在CBS.findnext里要使用这个
        return self.cost < other.cost

class CBS():
    def __init__(self, agents, game_map):
        '''
        class CBS is used for find partial solution using CBS algorithm.
        '''
        self.agents = agents
        self.game_map = game_map
        self.open_list = list()
    
    def find_next(self):
        return min(self.open_list)

    def find_partial_solution(self):
        '''
        find a partial solution, move all agents from starts to targets without conflict
        '''
        self.open_list = [] # 这个其实是重要的, in case you forgot it
        root = Node([], self.agents, self.game_map)
        self.open_list.append(root)
        iter_for_test = 0
        while len(self.open_list) > 0 and iter_for_test < 500:
            node = self.find_next() # 获取代价最小的值
            self.open_list.remove(node)  
            if not node.collision:  # 如果没有冲突，那们就说明已经找到了
                #print(node.solution)
                #time.sleep(8)
                return node.solution
            else:
                constraints_list = node.split() # 获得约束，这个约束应该是两个列表，每个列表都是一套约束，这一套约束由继承父节点和新增约束两部分构成
                for constraints in constraints_list:
                    
                    if node.constraints:
                        new_constraints = copy.deepcopy(node.constraints)
                        new_constraints.append(constraints)
                        new_node = Node(new_constraints, self.agents, self.game_map)
                        self.open_list.append(new_node)
                    else:
                        new_constraints = [copy.deepcopy(constraints)]
                        new_node = Node(new_constraints, self.agents, self.game_map)
                        self.open_list.append(new_node)
                        
            iter_for_test += 1
            if iter_for_test > 500:
                print("卡住了")
                return node.solution
            
        return None
    
class CentreControl():
    def __init__(self, agent_num, goods_num, game_map):
        '''
        A CentreControl should maintain a list of all agents, maintain a tree to find a solution
        '''
        self.agents = [Agent(game_map, i, i) for i in range(agent_num)]
        # for test
        for i in range(agent_num):
            print("agent", i, "position", self.agents[i].position)
        time.sleep(5)
        # self.conflicts = None
        #se"Constraints": [], "Solution": [], Cost}
        # self.goods_left = goods_num   # this shit I complete in map
    def state_update(self, game_map: Map, Partial_Solution):
        '''
        After caculate partial solution, we'll call this function to change states below:
        - current position of each agent (they will be move to the last position of Partail Solution)
        - target position of each agent
        - is_load argument of each agent
        - goods_left argument of the map
        This function move all agents to the state where the partial solution has taken places, and change their target position at the same time 
        '''
        steps = len(Partial_Solution[0])   # step is the columns of Partial_Solution
        goods_cnt = 0                       # caculate how much goods were taken by agents
        for i, agent in enumerate(self.agents):
            agent.position = Partial_Solution[i][steps - 1] # change current position
            if agent.position == game_map.repo_pos1:
                goods_cnt += 1
                agent.is_load = True    # loading
            elif agent.position == game_map.repo_pos2:
                agent.is_load = False   # unloading
            agent.update_state(game_map)                # change target position
            
        game_map.goods_left -= goods_cnt
    def is_concluded(self, game_map: Map):
        '''
        To analyse if each agent is ready to go home:
        1. goods_left is 0
        2. no agents loading goods now
        '''
        if game_map.goods_left != 0:
            return False
        for agent in self.agents:
            if agent.is_load == True:
                return False
        return True
    def Solution_find(self, game_map: Map): 
        Global_Solution = None
        iter_for_test = 0
        while self.is_concluded(game_map) == False:
            Searcher = CBS(self.agents, game_map)  # when self.agents update, CSB.agents will also update (?)
            Partial_Solution = Searcher.find_partial_solution()    # Caculate partial solution based on current state
            
            # HOW DARE YOU WRITE SHIT LIKE BELOW??
            if Global_Solution == None:
                Global_Solution = Partial_Solution
            else:
                if Partial_Solution:
                    Global_Solution = [x + y for x, y in zip(Global_Solution, Partial_Solution)]
                else:
                    break
            self.state_update(game_map, Partial_Solution) # update all states
            print("剩余货物: ", game_map.goods_left)


            # iter_for_test += 1
            # if iter_for_test > 20:
            #     print("出错了")
            #     break
        print("最后剩余的货物：", game_map.goods_left)

        return Global_Solution
