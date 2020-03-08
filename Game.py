#!/usr/bin/env python

import Board
import copy
import random

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
        for idx, point in enumerate(self.board_desc.points):
            if point != Board.POINT_EMPTY:
                if self.board_desc.checkIfPrisoner(idx,point):
                    col = 'w' if point == Board.STONE_WHITE else 'b'
                    self.board_desc.prisoners[idx] = col
    
    def checkTerminal(self):
        free_points = []
        for i,p in enumerate(self.board_desc.points):
            if p == Board.POINT_EMPTY:
                free_points.append(i)

        if self.step > 79 or len(free_points) == 0:
            self.game_ended = True
            self.board_desc.is_terminal = True
            return

    def takeTurn(self, action):
        
        self.checkTerminal()
        self.step += 1
        self.board_desc.points[action] = Board.STONE_WHITE
        
        # Evaluate prisoners
        self.evalPrisoners()

        for idx, val in enumerate(self.board_desc.prisoners):
            if val == 'o':
                continue

            if val == 'w':
                self.black_points += 1
            elif val == 'b':
                self.white_points += 1

            self.board_desc.points[idx] = Board.POINT_EMPTY
            self.board_desc.prisoners[idx] = 'o'

    
    def takeTurnBlack(self, action):
        
        self.checkTerminal()
        #act = random.choice(free_points)
        self.board_desc.points[action] = Board.STONE_BLACK

        # eval prisoners
        self.evalPrisoners()

        for idx, val in enumerate(self.board_desc.prisoners):
            if val == 'o':
                continue
            if val == 'w':
                self.black_points += 1
            elif val == 'b':
                self.white_points += 1
            self.board_desc.points[idx] = Board.POINT_EMPTY
            self.board_desc.prisoners[idx] = 'o'

    
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




    
