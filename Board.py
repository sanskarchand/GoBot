#!/usr/bin/env python

STONE_WHITE = "<white>"
STONE_BLACK = "<black>"
POINT_EMPTY = "<empty>"

'''
class Point:
    def __init__(self):
        self.val = EMPTY
'''

# This acts as the state
class  Board:

    def __init__(self):
        self.size = 9
        self.num_points = (self.size + 1)**2
        self.points = []
        self.resetBoard()

    def resetBoard(self):
        self.points = []
        for p in range(self.num_points):
            self.points.append(POINT_EMPTY)
    
    # possible moves for white
    def getPossibleMoveList(self):
        move_list = []
        for idx, point in enumerate(self.points):
            if point == POINT_EMPTY:
                move_list.append(idx)
        
        return move_list

    def evaluateBoardState(self):
        """
        evaluateBoardState: 
            returns a tuple of (points_white, points_black)
        """

        pass
    
    def isGameOver(self):
        pass
    
    def isSurroundedBy(self, i, j):
        # i = 0, j = 0 is the top left point
        # returns STONE_WHITE or STONE_BLACK

        arr_index = i * self.size + j
