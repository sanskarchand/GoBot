#!/usr/bin/env python

class Vertex:
    
    def __init__(self, board_desc=None):
        self.name = None
        self.board_desc = board_desc
        self.parent = None
        self.children = []
    
    # double entendre not intended
    def getChildFromAction(self, action):
        
        #apply action to get new board state
        #action can be obtained by calling Board.getPossibleMoveList
        new_state = self.board_desc
        new_state.points[action] = Board.STONE_WHITE
        
        child = Vertex(new_state)
        child.parent = self
        child.name = self.name + "_" + str(action)

        self.children.append(child)
        
        return child




# Graph for MCTS with UCT
class Graph:

    def __init__(self):
        self.vertex_set = set()
        self.adjacency_dict = dict()


    
    def addVertex(self, vertex_from, vertex_to):
        if vertex_from not in self.adjacency_dict.keys():
            self.adjacency_dict[vertex_from] = [vertex_to]
        else:
            self.adjacency_dict[vertex_from].append(vertex_to)

        self.vertex_set.add(vertex_from)
        self.vertex_set.add(vertex_to)


    def monteCarloWithUCTSearch(self, start_vertex):
        

        # get best child of current root(start_vertex)
        # visit it the most
        # get best move
