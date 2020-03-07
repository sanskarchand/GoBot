#!/usr/bin/env python

import util

STONE_WHITE = "<white>"
STONE_BLACK = "<black>"
POINT_EMPTY = "<empty>"

'''
class Point:
    def __init__(self):
        self.val = EMPTY
'''

def predicateWhiteOrEmpty(point):
    return point == STONE_WHITE or point == POINT_EMPTY
def predicateBlackOrEmpty(point):
    return point == STONE_BLACK or point == POINT_EMPTY



# This acts as the state
class  Board:

    def __init__(self):
        self.size = 9
        self.num_points = (self.size)**2
        self.points = []
        self.territory = []
        self.resetBoard()

    def resetBoard(self):
        self.points = []
        self.territory = []
        for p in range(self.num_points):
            self.points.append(POINT_EMPTY)
            self.territory.append('o')
    
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

        obviously only applicable to terminal states
        """

        # current: evaluate territory ( naive function )
        white_territory = 0
        black_territory = 0
        points_white = 0
        points_black = 0

        for idx, ep in enumerate(self.points):

            if ep != POINT_EMPTY:
                continue
            res = self.returnSurrounded(idx)

            if res == STONE_BLACK:
                black_territory += 1
                self.territory[idx] = 'b'
            elif res == STONE_WHITE:
                white_territory += 1
                self.territory[idx] = 'w'
        
        points_white = white_territory
        points_black = black_territory

        return (points_white, points_black)
        
    # note: implement this in a separate Game class; does not belong here
    #   as we need info about player turns and passes
    def isGameOver(self):
        pass
    
    def returnSurrounded(self, index):
        # spread forth in all four directions until we hit
        # a stone or an edge
        # inefficient; need to use something like flood fill, dude9.cc(oldproj)
        up_list = []
        down_list = []
        right_list = []
        left_list = []
        
        up_ind = index - self.size
        while util.is_valid_index(self.size, up_ind):
            up_list.append(self.points[up_ind])
            
            # of course, break after hitting first stone
            if self.points[up_ind] != POINT_EMPTY:
                break
            
            up_ind -= self.size


        down_ind = index + self.size
        while util.is_valid_index(self.size, down_ind):
            down_list.append(self.points[down_ind])

            if self.points[down_ind] != POINT_EMPTY:
                break

            down_ind += self.size

        right_ind = index + 1
        while util.is_valid_index(self.size, right_ind):

            # if we have switched rows, stop immediately
            if index // self.size != right_ind // self.size:
                break

            right_list.append(self.points[right_ind])

            if self.points[right_ind] != POINT_EMPTY:
                break
            
            right_ind += 1

        left_ind = index - 1
        while util.is_valid_index(self.size, left_ind):

            # same check as for right
            if index // self.size != left_ind // self.size:
                break

            left_list.append(self.points[left_ind])

            if self.points[left_ind] != POINT_EMPTY:
                break

            left_ind -= 1

        # HOWEVER, if the given position is at an edge, override
        if util.is_left_edge(self.size, index):
            left_list = [POINT_EMPTY]
        if util.is_right_edge(self.size, index):
            right_list = [POINT_EMPTY]
        if util.is_upper_edge(self.size, index):
            up_list = [POINT_EMPTY]
        if util.is_lower_edge(self.size, index):
            down_list = [POINT_EMPTY]

        up_black = list(map(predicateBlackOrEmpty, up_list))
        down_black = list(map(predicateBlackOrEmpty, down_list))
        right_black = list(map(predicateBlackOrEmpty, right_list))
        left_black = list(map(predicateBlackOrEmpty, left_list))
        
        up_white = list(map(predicateWhiteOrEmpty, up_list))
        down_white = list(map(predicateWhiteOrEmpty, down_list))
        right_white = list(map(predicateWhiteOrEmpty, right_list))
        left_white = list(map(predicateWhiteOrEmpty, left_list))

        print("FOR INDEX ", index)
        print("UP WHITE: ", up_white)
        print("DOWN WHITE: ", down_white)
        print("RIGHT WHITE: ", right_white)
        print("LEFT_WHITE: ", left_white)

        if all(up_black) and all(down_black) and all(right_black) and all(left_black):
            return STONE_BLACK
        if all(up_white) and all(down_white) and all(right_white) and all(left_white):
            return STONE_WHITE
        
        return POINT_EMPTY # belongs to no territory

        
    def isSurroundedBy(self, i, j):
        # i = 0, j = 0 is the top left point
        # returns STONE_WHITE or STONE_BLACK

        arr_index = i * self.size + j

    def __copy__(self):
        
        cls = self.__class__
        result = cls.__new__(cls)
        result.size = self.size
        result.num_points = self.num_points
        result.points = self.points.copy()
        result.territory = self.territory.copy()
        
        return result
