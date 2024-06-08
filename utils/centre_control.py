#coding=gbk
'''
This script defines CBS class and CentreControl class.
CBS class is used for find Partial Solution and CentrControl class is used for find Global Solution
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
import random

'''
Here are three classes:
- Node: for CBS
- CBS: find Partial Solution of each step
- CentreControl: find Global Solution of the question
'''

# class Node is used to find Partial Solution, test collision, generate constraints
# class CBS maintain a open list of nodes.
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
        for path in self.solution:
            self.cost += len(path)

        min_steps = min(steps)
        self.solution = [path[:min_steps] for path in self.solution]

        self.collision, self.collision_type = self.get_first_collision()    # type 0: two agents in one positon at a time; type 1: two agent exchange their position

    def get_first_collision(self):
        '''
        This function will return the first collision and its collision type
        collision is represented as (i, j, (x, y), t)
        collision type 0 represents two agents occuopied the same position at a time, and type 1 represents two agents exchange their position at a time.
        '''
        # type 0
        for t in range(len(self.solution[0])):
            for i in range(len(self.solution) - 1):
                for j in range(i + 1, len(self.solution)):
                    if self.solution[i][t] == self.solution[j][t]:
                        return (i, j, self.solution[i][t], t), 0
        
        # type 1
        # agent1: (x, y) -> (x + 1, y); agent2: (x + 1, y) -> (x, y)
        # we will return (1, (x + 1, y), t + 1)
        for i in range(len(self.solution) - 1):
            for j in range(i + 1, len(self.solution)):
                for t in range(len(self.solution[0]) - 1):
                    if self.solution[i][t] == self.solution[j][t + 1] \
                        and self.solution[j][t] == self.solution[i][t + 1]:
                        return (i, j, self.solution[i][t], self.solution[j][t], t), 1    # ���������1�ʹ���������������������ҵ���˼��,i ,j��tʱ�̽�����λ��
        # avoid a special situation, that two agents exchange their position between two Partial Solution
        # ���ǵ�·�����ǲ�������ʼ��λ�����������Ǿͻ����ж�Ŀǰ��λ�úͿ�ʼ�ĵ�һ��λ��֮���Ƿ��г�ͻ 
        '''step = len(self.solution[0])
        for i in range(len(self.solution) - 1):
            for j in range(i + 1, len(self.solution)):
                if self.solution[i][step - 1] == self.agents[j].position \
                    and self.solution[j][step - 1] == self.agents[i].position:
                    return (i, j, self.solution[i][step - 1], 0), 1'''
        for i in range(len(self.solution) - 1):
            for j in range(i + 1, len(self.solution)):
                if self.agents[i].position == self.solution[j][0] \
                    and self.agents[j].position == self.solution[i][0]:
                    #return (i, j, self.solution[i][0], t), 1    # I write solution[i] as solution[j], and spend a week to find this.
                    return (i, j, self.solution[i][0], self.solution[j][0], 0), 1   # ����ʱ����0����֮ǰд��t���˷��˺ܶ�ʱ��

        if self.solution and len(self.solution[0]) == 1:
            for i in range(len(self.solution) - 1):
                for j in range(i + 1, len(self.solution)):
                    if self.solution[i][0] == self.agents[j].position \
                        and self.solution[j][0] == self.agents[i].position:
                        # return (i, j, self.solution[i][0], 0), 1
                        return (i, j, self.solution[i][0], self.solution[j][0], 0), 1
                    

        return None, None

    def split(self):
        '''
        input: a collision(from function get_collision())
            (i, j, v, t)    # agent i and j at the same vetex at time t
        output: a list of two constraints
            [(i, v, t), (j, v, t)] if collision type is 0
        '''
        if self.collision_type == 0:
            # print(self.collision)
            # ���ڵ������������������л��ﶼ�������
            if self.collision:
                magical_trick = np.random.random()
                print(magical_trick)
                if magical_trick <= 0.4:
                    return [(self.collision[0], self.collision[2], self.collision[3])]
                elif magical_trick <= 0.8:
                    return [(self.collision[1], self.collision[2], self.collision[3])]
                elif magical_trick > 0.8:
                    return [(self.collision[0], self.collision[2], self.collision[3]), 
                            (self.collision[1], self.collision[2], self.collision[3])] 
                # return [(self.collision[0], self.collision[2], self.collision[3]), 
                        # (self.collision[1], self.collision[2], self.collision[3])]
        elif self.collision_type == 1:
            if self.collision:
                # �˴�����Ҫ����һ������ԣ������������ѭ��
                magical_trick = np.random.random()
                print(magical_trick)
                if magical_trick <= 0.4:
                    return [(self.collision[0], self.collision[2], self.collision[4])]
                elif magical_trick <= 0.8:
                    return [(self.collision[1], self.collision[3], self.collision[4])]
                elif magical_trick > 0.8:
                    return [(self.collision[0], self.collision[2], self.collision[4]), 
                            (self.collision[1], self.collision[3], self.collision[4])]  # this piece of shiiiiiiiiiiiiiiiiiiiiiit slow me down a lot. Is coding so hard when people are toung, or always?
            
    def __lt__(self, other):
        # CBS.find_next() function will compare two nodes
        # ʵ�ʲ������ҷ����������ܿ��ܻᵼ����ѭ������Ϊcost�ƺ��ǲ��ġ���
        # �������cost��ͬ���ͷ���costС����һ���������������cost��ͬ�����Ƿ����ȱ��Ž�ȥ����һ����Ҳ����˵���ڱ���Լ������ʱ������Ҫ�����ܱ�֤�ǲ���ر����ģ�������ܻ���һ����֧����̫��
        # �ⲿ��������Ҫ��CBS��find_next��������ʵ��
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
        # for node in self.open_list:   # �������뷵�����ŵģ�����һ��˴�֮����ۼ����������֣���������ܵ�����ѭ���������ж���û���޳�ͻӦ����ǰ
            # if node.collision == None:
                # return node
        # �ʼ��ֻ��cost�Ƚϣ�������ѭ������������collision�жϣ�Ҳ����ѭ������Ϊ�˴˸���һ���϶���û�г�ͻ�ģ������ٽ�һ���ͻص���ԭ�㣩
        # �����Ҵ��������ж�cost��Ȼ���ж�������Լ�����е���ȣ������������������
        # min_node = None
        # min_idx = -1 
        # min_cost = int(25536)
        # for idx, node in enumerate(self.open_list):
            # if node.cost < min_cost:
                # min_node = node
                # min_idx = idx
                # min_cost = node.cost
            # elif node.cost == min_cost:
                # print("test")
                # if idx < min_idx:
                    # min_node = node
                    # min_idx = idx
                    # min_cost = node.cost
            # else:
                # pass 
        # return min(self.open_list)

        # ���˸��ַ����������ܽ����ѭ�������⣬���������ֱ�����ѡȡ
        node = random.choice(self.open_list)        # �ɹ������
        return node

    def find_partial_solution(self):
        '''
        find a partial solution, move all agents from starts to targets without conflict
        '''
        self.open_list = [] # ?
        root = Node([], self.agents, self.game_map)
        self.open_list.append(root)
        trick = 0

        while len(self.open_list) > 0 and trick < 400:
            print(len(self.open_list))
            node = self.find_next()
            # for test
            
            solution = node.solution
            # test end
            self.open_list.remove(node)  
            if not node.collision:  # if no collision, then we have found the solution.
                return node.solution
            else:
                constraints_list = node.split()
                for constraints in constraints_list:
                    # new contraints = constraints from parent node + cnstraint.
                    if node.constraints:
                        if constraints in node.constraints:
                            break   # ����һ��ͷ��ҽͷ�������������ظ���ĳЩԼ���Ž�ȥ��������ѭ��
                        new_constraints = copy.deepcopy(node.constraints)
                        new_constraints.append(constraints)
                        new_node = Node(new_constraints, self.agents, self.game_map)
                        self.open_list.append(new_node)
                    else:
                        new_constraints = [copy.deepcopy(constraints)]
                        new_node = Node(new_constraints, self.agents, self.game_map)
                        self.open_list.append(new_node)
            
            trick += 1
        if trick > 400:
            print("error")
        return [[agent.position] for agent in self.agents]
    
class CentreControl():
    def __init__(self, agent_num, game_map):
        '''
        A CentreControl should maintain a list of all agents, maintain a tree to find a solution
        '''
        self.agents = [Agent(game_map, i, i) for i in range(agent_num)] # agents shouldn't at the same position at the beginning.
        # for test
        #for i in range(agent_num):
        #    print("agent", i, "position", self.agents[i].position)
        #time.sleep(5)
    
    def state_update(self, game_map: Map, Partial_Solution):
        '''
        After caculate partial solution, we'll call this function to change states below:
        - current position of each agent (they will be move to the last position of Partail Solution)
        - target position of each agent
        - is_load argument of each agent
        - goods_left argument of the map
        This function move all agents to the state where the partial solution has taken places, and change their target position at the same time 
        '''
        if Partial_Solution == None:
            return
        steps = len(Partial_Solution[0])   # step is the columns of Partial_Solution
        goods_cnt = 0                       # caculate how much goods were taken by agents
        for i, agent in enumerate(self.agents):
            agent.position = Partial_Solution[i][steps - 1] # change current position
            if agent.position == game_map.repo_pos1 and agent.is_load == False:
                goods_cnt += 1
                agent.is_load = True    # loading
            elif agent.position == game_map.repo_pos2 and agent.is_load == True:
                agent.is_load = False   # unloading
            agent.update_state(game_map)                # change target position
            
        game_map.goods_left -= goods_cnt
        # this is just a small trick.
        if game_map.goods_left < 0:
            game_map.goods_left = 0
    
    def is_concluded(self, game_map: Map):
        '''
        To analyse if each agent is ready to go home:
        1. goods_left is 0
        2. no agents loading goods now
        '''
        # a small trick
        if game_map.goods_left < 0:
            game_map.goods_left = 0

        if game_map.goods_left != 0:
            return False
        for agent in self.agents:
            if agent.is_load == True:
                return False
            if agent.position != agent.birth_place:
                return False
        return True
    
    def Solution_find(self, game_map: Map): 
        Global_Solution = None
        i = 0

        trick = 0
        goods_left = game_map.goods_left
        while self.is_concluded(game_map) == False and i < 50:
            # for test
            if goods_left == game_map.goods_left:
                trick += 1
            else:
                trick = 0
                goods_left = game_map.goods_left
            # test end
            
            Searcher = CBS(self.agents, game_map)  # when self.agents update, CSB.agents will also update (?)
            Partial_Solution = Searcher.find_partial_solution()    # Caculate partial solution based on current state
            
            # HOW DARE YOU WRITE SHIT LIKE BELOW??
            if Global_Solution == None:
                Global_Solution = Partial_Solution
            else:
                if Partial_Solution:
                    Global_Solution = [x + y for x, y in zip(Global_Solution, Partial_Solution)]
                else:
                    return Global_Solution
                    pass    # shit code!
            self.state_update(game_map, Partial_Solution)
            print("goods left: ", game_map.goods_left)
            # i += 1

        print("GOODS LEFT: ", game_map.goods_left)

        return Global_Solution
