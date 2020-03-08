#!/usr/bin/env python

import Board
import copy
import math
import random
import Display
import time

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

        self.C = 0.3
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
            print("most visited") 
            best_child = self.getBestChild(start_vertex)

        return best_child.move
    
    def getBestChild(self, root_vertex):
        
        #for i in range(root_vertex.getNumAllowedMoves()):
        st = time.process_time()
        while self.checkWithinTimeLimit(st):
            new_vert = self.ultimateExpansion(root_vertex)
            utility = self.getFinalUtility(new_vert.game_state) # game state
            self.backPropagate(new_vert, utility)


        best_child = self.getBestOfAllChildren(root_vertex)
        return best_child


    def _UCB1_value(self, parent_vert, child_vert):
        v_i = child_vert.utility/child_vert.num_visited
        N = parent_vert.num_visited
        n_i = child_vert.num_visited

        return v_i + self.C * math.sqrt( math.log(N)/n_i  )
            

    def getBestOfAllChildren(self, vertex):

        if len(vertex.children) == 0:
            return
        
        # NOTABENE: assumption of constant order
        value_list = []
        for child in vertex.children:
            value_list.append( self._UCB1_value(vertex, child) )
        
        maximum = max(value_list)
        max_ind = value_list.index(maximum)

        return vertex.children[max_ind]

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
    
    def getFinalUtility(self, vert_game_state):

        while not vert_game_state.game_ended:
            if not vert_game_state.board_desc.getPossibleMoveList():
                break
            action = random.choice(vert_game_state.board_desc.getPossibleMoveList())
            vert_game_state =  copy.copy(vert_game_state)
            vert_game_state.takeTurn(action)
            #self.gui.board_desc = vert_game_state.board_desc
            #self.board_steps.append(vert_game_state.board_desc)
            #RECORD

        
        print("UTILITY is: ", vert_game_state.getUtility())
        return vert_game_state.getUtility()
    
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
        return elapsed_time < 10

