#!/usr/bin/env python

TURN_BLACK = 0
TURN_WHITE = 1

class Game:

    def __init__(self, m_board):

        self.board = m_board
        self.turn = TURN_BLACK

        self.black_points = 0
        self.white_points = 0

    def successorFunc(self):
        pass
