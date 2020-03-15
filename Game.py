#!/usr/bin/env python

import Board
import copy
import random
import time

TURN_BLACK = 0
TURN_WHITE = 1


class Game:

    def __init__(self, m_board):

        self.board_desc = m_board   # current state
        self.turn = TURN_BLACK

        self.black_points = 0
        self.white_points = 0

        self.step = 0
        self.game_ended = False
    
    def evalPrisoners(self):
        # Evaluate prisoners
        self.board_desc.prisoners = []
        self.board_desc.group_imprisoned_points = []

        for idx, point in enumerate(self.board_desc.points):
            if point != Board.POINT_EMPTY:
                if self.board_desc.checkIfPrisoner(idx,point):

                    if point == Board.STONE_WHITE:
                        col = 'w'
                        self.black_points += 1
                    else:
                        col = 'b'
                        self.white_points += 1

                    #col = 'w' if point == Board.STONE_WHITE else 'b'
                    #self.board_desc.prisoners[idx] = col
                    self.board_desc.points[idx] = Board.POINT_EMPTY
    

    # NOTABENE: biggest cause of slowdown
    # need a proper way to decide if a game has ended
    def checkTerminal(self):
        free_points = []
        for i,p in enumerate(self.board_desc.points):
            if p == Board.POINT_EMPTY:
                free_points.append(i)
    
        if self.step > 79 or len(free_points) == 0:
            self.game_ended = True
            self.board_desc.is_terminal = True
            print("<<REACHED TERMINAL STATE>>")
            return

    def takeTurn(self, action):
        
        t1 = time.time()
        self.checkTerminal()
        self.step += 1
        self.board_desc.points[action] = Board.STONE_WHITE
        
        # Evaluate prisoners
        self.evalPrisoners()

        
        t2 = time.time()
        #print("\t\t\Total takeTurn time = ", t2 - t1)
    
    def takeTurnBlack(self, action):
        
        self.checkTerminal()
        #act = random.choice(free_points)
        self.board_desc.points[action] = Board.STONE_BLACK

        # eval prisoners
        self.evalPrisoners()

    
    def update(self):
        self.step += 1

    def getUtility(self):
        p_w, p_b, pri_w, pri_b = self.board_desc.evaluateBoardState()
        #p_w += self.white_points
        #p_b += self.black_points
        #p_w += pri_w
        #p_b += pri_b
        
        p_w += pri_w
        p_b += pri_b
        #print("BLACK's prisoners: ", self.black_points)
        #print("WHITE's prisones: ", self.white_points)

        diff = (p_w - p_b)/(p_w + p_b + 2)
        
        '''
        if diff > 0.3:
            return 1
        
        return 0
        '''

        return diff




    def __copy__(self):
        
        cls = self.__class__
        result = cls.__new__(cls)
        
        result.board_desc = copy.copy(self.board_desc)
        result.turn = self.turn
        result.black_points = self.black_points
        result.white_points = self.white_points
        result.step = self.step
        result.game_ended = self.game_ended

        return result




    
