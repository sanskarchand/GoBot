#!/usr/bin/env python

import Board, Graph
import random

def monteCarloTrain():

    first_state = Board.Board()
    black_idx = random.choice(list(range(first_state.size)))
    first_state.points[black_idx] = Board.STONE_BLACK

    search_graph = Graph.Graph()
    first_vert = Graph.Vertex(first_state, "initial")
    search_graph.setInitialVertex(first_vert)

    for white_idx in search_graph.initial_vertex.board_desc.getPossibleMoveList():
        
        child = search_graph.initial_vertex.getChildFromAction(white_idx)
        print("CHILD STATE: ", child.name)


monteCarloTrain()
