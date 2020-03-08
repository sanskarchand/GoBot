#!/usr/bin/env python

import Board, Graph, Game
import random
import copy
import Display

def monteCarloTrain():

    first_state = Board.Board()
    black_idx = random.choice(list(range(first_state.size)))
    first_state.points[black_idx] = Board.STONE_BLACK
    
    game = Game.Game(first_state)
    search_graph = Graph.Graph()
    first_vert = Graph.Vertex(game, "initial")
    search_graph.setInitialVertex(first_vert)
    

    m = search_graph.monteCarloWithUCTSearch( search_graph.initial_vertex )
    for c in search_graph.initial_vertex.children:
        print(c.move)
    print("Best move = ", m)

    g = Display.GoGUI(first_state)
    g.statelist = search_graph.board_steps
    g.mainLoop()


monteCarloTrain()
