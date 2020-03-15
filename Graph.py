#!/usr/bin/env python

import Board
import copy
import math
import random
import Display
import time

DEBUG = True


"""
[src:http://u.cs.biu.ac.il/~sarit/advai2018/MCTS.pdf]

UCB: Multi-bandit problem
    Pick each arm which maximizes
        v_i + C * sqrt(ln(N)/n_i),
            where   v_i = value estimate
                    C   = tunable param
                    N   = total number of trials
                    n_i = number of trials for arm i

    In this case:
        v_i => 
"""
class Vertex:
    
    def __init__(self, game_state=None, name=None):
        self.name = name
        self.game_state = game_state 
        self.parent = None
        self.children = []
        self.actions_taken = []
        self.utility = 0 # merit
        self.num_visited = 0
        self.move = None
    
    # double entendre not intended
    def getChildFromAction(self, action):
        
        #apply action to get new board state
        #action can be obtained by calling Board.getPossibleMoveList
        new_state = copy.copy(self.game_state)
        new_state.takeTurn(action)
        #new_state.board_desc.points[action] = Board.STONE_WHITE
        
        child = Vertex(new_state)
        child.parent = self
        child.name = self.name + "[" + str(action) + "]"
        child.move = action

        self.children.append(child)
        self.actions_taken.append(action)
        
        return child
    
    def getNumAllowedMoves(self):
        # NOTABENE: need to add rule to prevent infinite loops
        return self.game_state.board_desc.points.count(Board.POINT_EMPTY)
    
    def expand(self):


        actions_left = []
        for idx, point in enumerate(self.game_state.board_desc.points):
            if point == Board.POINT_EMPTY and point not in self.actions_taken:
                actions_left.append(idx)

        chosen_action = random.choice(actions_left)
        print("EXPAND child with move = ", chosen_action)
        child_vertex = self.getChildFromAction(chosen_action)
        return child_vertex




# Graph for MCTS with UCT
class Graph:

    def __init__(self):
        self.vertex_set = set()
        self.adjacency_dict = dict()
        self.initial_vertex = None

        self.C = 1.44
        self.board_steps = []

    
    def setInitialVertex(self, vert):
        self.vertex_set.add(vert)
        self.initial_vertex = vert

    def addEdge(self, vertex_from, vertex_to):
        if vertex_from not in self.adjacency_dict.keys():
            self.adjacency_dict[vertex_from] = [vertex_to]
        else:
            self.adjacency_dict[vertex_from].append(vertex_to)

        self.vertex_set.add(vertex_from)
        self.vertex_set.add(vertex_to)


    def monteCarloWithUCTSearch(self, start_vertex):
        """
        monteCarloWithUCTSearch=>
            gives the best move to take (for white) at start_vertex
        """
        
        best_child = self.getBestChild(start_vertex)
        while self.checkChildNotMostVisited(best_child, start_vertex):
            print("[NOT_MOST_VISITED]") 
            best_child = self.getBestChild(start_vertex)

        return best_child.move
    
    def getBestChild(self, root_vertex):
        
        #for i in range(root_vertex.getNumAllowedMoves()):
        st = time.process_time()
        while self.checkWithinTimeLimit(st):
            t1 = time.time()

            t_exp_1 = time.time()
            new_vert = self.ultimateExpansion(root_vertex) # TREEPOLICY
            t_exp_2 = time.time()
            #print("\t\tultimate expansion time: ", t_exp_2 - t_exp_1) # highest time

            t_util_1 = time.time()
            utility = self.getFinalUtility(new_vert.game_state) # game state #DEFAULTPOLICY
            t_util_2 = time.time()
            #print("\t\tfinal utility time: ", t_util_2 - t_util_1)

            t_bp_1 = time.time()
            self.backPropagate(new_vert, utility)
            t_bp_2 = time.time()

            #print("\t\tback propagation time: ", t_bp_2 - t_bp_1)
            t2 = time.time()
            #print("^\t\t\toverall time = ", t2 - t1)


        best_child = self.getBestOfAllChildren(root_vertex)
        return best_child


    def _UCB1_value(self, parent_vert, child_vert):
        v_i = child_vert.utility/child_vert.num_visited
        N = parent_vert.num_visited
        n_i = child_vert.num_visited

        return v_i + self.C * math.sqrt( math.log(N)/n_i  )
            

    def getBestOfAllChildren(self, vertex):

        assert(len( vertex.children ) != 0)
        print(" No of children for {} =".format((vertex.name)), len(vertex.children))

        # NOTABENE: assumption of constant order
        value_list = []
        for child in vertex.children:
            val = self._UCB1_value(vertex, child)
            print("\t\t\t\tutility value of {} = ".format(child.name), val)
            value_list.append(val)

        maximum = max(value_list)
        max_ind = value_list.index(maximum)

        return vertex.children[max_ind]
    

    ## Tree policy
    def ultimateExpansion(self, vertex):
        # C = ?
        while not vertex.game_state.board_desc.is_terminal:

            num_allowed = vertex.getNumAllowedMoves()
            if num_allowed != len(vertex.children):
                # not all children have been expanded
                return vertex.expand()
            else:
                #NOTABENE probable future error location
                vertex = self.getBestOfAllChildren(vertex)

        return vertex
    
    # default policy
    def getFinalUtility(self, vert_game_state):
        
        if DEBUG:
            print("\t\t\tgetFinalUtility called")

        while not vert_game_state.game_ended:

            t1 = time.time()
            if not vert_game_state.board_desc.getPossibleMoveList():
                break
            action = random.choice(vert_game_state.board_desc.getPossibleMoveList())
            if DEBUG:
                print("\t\t\t[gfu]takeTurn ", action)

            vert_game_state =  copy.copy(vert_game_state)
            vert_game_state.takeTurn(action)

            # take a random black turn
            free_moves = []
            for i, p in enumerate(vert_game_state.board_desc.points):
                if p == Board.POINT_EMPTY:
                    free_moves.append(i)

            p_choice = random.choice(free_moves)
            
            vert_game_state = copy.copy(vert_game_state)
            vert_game_state.takeTurnBlack(p_choice)

            t2 = time.time()
            #print("\t\t\tgetFinalUtility total time = ", t2 - t1)

            #self.gui.board_desc = vert_game_state.board_desc
            #self.board_steps.append(vert_game_state.board_desc)
            #RECORD
        util_val = vert_game_state.getUtility() 
        return util_val 

    def backPropagate(self, vertex, utility):
        while vertex is not None:
            vertex.num_visited += 1
            vertex.utility += utility
            vertex = vertex.parent

    def checkChildNotMostVisited(self, child, root_vert):
        children = root_vert.children
        for c in children:
            if c is not child:
                if c.num_visited> child.num_visited:
                    return True
        return False
    
    def checkWithinTimeLimit(self, start):
        elapsed_time = time.process_time() - start
        return elapsed_time < 30

