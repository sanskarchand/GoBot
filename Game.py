#!/usr/bin/env python

import Board

TURN_BLACK = 0
TURN_WHITE = 1


class Game:

    def __init__(self, m_board):

        self.board = m_board   # current state
        self.turn = TURN_BLACK

        self.black_points = 0
        self.white_points = 0
    
