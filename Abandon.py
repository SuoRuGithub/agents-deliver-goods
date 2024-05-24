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
import heapq

def get_collision(solution):
    '''
    Given a Solution S, this function will find **the first** collision, 
    -> (a_i, a_j, v, t)
    '''
    # ���Ǹ��������������ͬһ���Ƿ���������ͬ��λ��
    # HOW DARE U WRITE SHIT BELOW?
    for i in range(len(solution[0])):   # the same column
        for j in range(len(solution) - 1):  # use two-layer loop compare each two in the same column
            for k in range(j + 1, len(solution)):
                if solution[j][i] == solution[k][i]:
                    return (j, k, solution[j][i], i)
    return ()

def get_total_cost(solution):
    '''
    Given a Solution S, this function will find total cost.
    ���ˣ����Ǵ˴���solution�ǽضϵģ���ͳ��cost�ƺ�����ô�ʺ�
    ���ˣ����ȼٶ�Լ���������ȵ����agent����ԭ����һ��������ʱ���մ�ͳ�ļ���
    '''
    return len(solution[0]) if solution else 0

def split(collision):
    '''
    input: a collision(from function get_collision())
        (i, j, v, t)    # agent i and j at the same vetex at time t
    output: a list of two constraints
        [(i, v, t), (j, v, t)]
    '''
    print(collision)
    if collision:
        return [(collision[0], collision[2], collision[3]), 
                (collision[1], collision[2], collision[3])]

'''
Here are two classes:
- CSB: find Partial Solution of each step
- CentreControl: find Global Solution of the question
'''

# ��һ������һֱ������ˣ�������дһ��
class Node():
    def __init__(self, ):

class CSB():
    def __init__(self, agents, game_map):
        '''
        agents: come from CentreControl, a list of all agents
        game_map: list of obstacle positions
        starts: current positions of all agents
        targets: target positions of all agents

        open_list: list of all nodes, in order of cost.
        '''
        
        self.agents = agents
        self.game_map = game_map
        #self.starts = starts
        #self.targets = targets
        self.num_of_agents = len(agents)
        self.open_list = []
    
    def push_node(self, node):
        print("cost of node: ", node["Cost"])
        heapq.heappush(self.open_list, (node['Cost'], node))    # open list is a min heap
    def pop_node(self):
        _, node = heapq.heappop(self.open_list)
        return node
    def create_node(self, constraints):
        '''
        This function will return a node

        �������Ҫ��ʲô�أ�
        ���ﱾ���е�ǰλ�á�Ŀ�ĵء���ͼ��Ϣ���Ҹ���һ��Լ�����������Ӧ��������һ��
        Ӧ���������Լ����Լ���������֣�һ�����ǴӸ��ڵ�̳����ģ���һ�����Ǹ���collision split�����ģ� 
        - �ȸ�Լ����ֵ
        - �ȸ��ݸ�����Լ������Solution�������ļ򵥼Ӻͣ�����һ������Ҫ������С���裬���������Agent�����������
        - ����cost
        - �����һ����ͻ
        '''
        node = {
            "Constraints": [],
            # "min_steps": 0,   cross the river, destory the bridge
            "Solution": [],
            "Cost": 0,
            "Collision": []
            }
        node["Constraints"] = constraints

        # ��������ȼ���agent.A_start_path_finding�����᷵��һ��·�����������С����
        steps = []
        for i, agent in enumerate(self.agents):
            agent.A_star_path_finding(self.game_map, constraints)
            path = agent.path
            step = len(path)
            node["Solution"].append(path)
            steps.append(step)
        # �˴���һ�����⣬�������������õ���SolutionӦ���ǽض��أ����ǲ��ض��أ�
        # �Ҿ��ýض�Ӧ��Ҳ�ǿ��Եģ���Ϊ�п�������ֻ��Ҫ�������ѣ��������������ض�һ��
        # node["min_steps"] = min(steps)    cross the river, destory the bridge
        min_steps = min(steps)
        node["Solution"] = [path[:min_steps] for path in node["Solution"]]
        node["Cost"] = get_total_cost(node["Solution"])
        node["Collision"] = get_collision(node["Solution"])
        return node

    def find_partial_solution(self):
        '''
        This function should return two things:
        - Solution: a list of all paths
        - min_step: total steps taken by the agent who reaches its target first
        (min_step is important, in tranditional CSB, agents just stay and wait when they reached their own target,
        but in our project, when a agent reaches its target, we should update states, and caculate the next Partial Solution)
        '''
        root = self.create_node([])
        self.push_node(root)

        while len(self.open_list) > 0:
            node = self.pop_node()
            if not node["Collision"]:
                return node["Solution"] 
            constraints = split(node["Collision"])  # �˴�constraints Ӧ��������Լ�����б�
            
            if constraints:
                for constraint in constraints:
                    if node["Constraints"]:
                        child_node = self.create_node(node["Constraints"].append(constraint))
                    else:
                        child_node = self.create_node([constraint])
                    self.push_node(child_node)
        return None

class CentreControl():
    def __init__(self, agent_num, goods_num, game_map):
        '''
        A CentreControl should maintain a list of all agents, maintain a tree to find a solution
        '''
        self.agents = [Agent(game_map, i) for i in range(agent_num)]
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
        Searcher = CSB(self.agents, game_map)  # when self.agents update, CSB.agents will also update (?)
        Global_Solution = None
        while self.is_concluded(game_map) == False:
            Partial_Solution = Searcher.find_partial_solution()    # Caculate partial solution based on current state
            
            # HOW DARE YOU WRITE SHIT LIKE BELOW??
            if Global_Solution == None:
                Global_Solution = Partial_Solution
            else:
                Global_Solution = [x + y for x, y in zip(Global_Solution, Partial_Solution)]
            
            self.state_update(game_map, Partial_Solution) # update all states

        return Global_Solution
