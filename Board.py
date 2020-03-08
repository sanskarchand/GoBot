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
class Board:

    def __init__(self):
        self.size = 9
        self.num_points = (self.size)**2
        self.points = []
        self.territory = []
        self.prisoners = []
        self.is_terminal = False # set by Game
        self.resetBoard()

    def resetBoard(self):
        self.points = []
        self.territory = []
        for p in range(self.num_points):
            self.points.append(POINT_EMPTY)
            self.territory.append('o')
            self.prisoners.append('o')
    
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
        
        ->points = territory 
        ->does not count prisoners, as this class is only a state representation
        ->obviously only applicable to terminal states
        """

        # current: evaluate territory ( naive function )
        white_territory = 0
        black_territory = 0
        points_white = 0
        points_black = 0
        prisoners_of_white = 0
        prisoners_of_black = 0
    

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
        
        #Only for checking, currently
        for idx, ep in enumerate(self.points):
            if ep == POINT_EMPTY:
                continue
            
            if self.checkIfPrisoner(idx, ep):
                val = 'w' if ep == STONE_WHITE else 'b'
                
                if val == 'w':
                    prisoners_of_white += 1
                else:
                    prisoners_of_black += 1

                self.prisoners[idx] = val
        
        points_white = white_territory
        points_black = black_territory
    
        print("ROOOOOOOOOOOOOOOOT", points_white,points_black, prisoners_of_white, prisoners_of_black)
        return points_white, points_black, prisoners_of_white, prisoners_of_black
        
    # note: implement this in a separate Game class; does not belong here
    #   as we need info about player turns and passes
    def isGameOver(self):
        pass
    

    def returnSurrounded(self, index):
        blank_list = [index]
        self.getEmptyGroupIndices(index, blank_list)
        
        nb = nw = 0

        for blank in blank_list:
            num_black, num_white = self.getStoneCountAroundEmpty(blank)
            nb += num_black
            nw += num_white

        if nb == 0:
            return STONE_WHITE
        elif nw == 0:
            return STONE_BLACK
        
        return POINT_EMPTY
    
    def getStoneCountAroundEmpty(self, blank_index):
        valid_indices = self.getValidSurroundingIndices(blank_index)
        good_indices = [i for i in valid_indices if i is not None]
        
        nb = nw = 0
        for ind in good_indices:
            if self.points[ind] == STONE_BLACK:
                nb += 1
            elif self.points[ind] == STONE_WHITE:
                nw += 1

        return (nb, nw)


    def getEmptyGroupIndices(self, index, group_list):
        valid_indices = self.getValidSurroundingIndices(index)
        good_indices = [i for i in valid_indices if i is not None]

        for ind in good_indices:
            if self.points[ind] == POINT_EMPTY and ind not in group_list:
                group_list.append(ind)
                self.getEmptyGroupIndices(ind, group_list) # thank god for mutable containers

        return group_list
    
    def getValidSurroundingIndices(self, index):
        # Invalid if corresponding edge
        # invalid if other row
        # invalid if out of range
        l = r = u = d = None
        
        l = index - 1
        if util.is_left_edge(self.size, index) or (l // self.size != index // self.size) or not util.is_valid_index(self.size, l):
            l = None

        r = index + 1
        if util.is_right_edge(self.size, index) or (r // self.size != index // self.size) or not util.is_valid_index(self.size, r):
            r = None

        u = index - self.size
        if util.is_upper_edge(self.size, index) or not util.is_valid_index(self.size, u):
            u = None

        d = index + self.size
        if util.is_lower_edge(self.size, index) or not util.is_valid_index(self.size, d):
            d = None
    
        return (l,r,u,d)



    def getSingleLiberties(self, index):
        """
        Up, Right, Left, Down.
        """
        up_ind = index - self.size
        down_ind = index + self.size
        left_ind = index - 1
        right_ind = index + 1

        lib = 0

        if util.is_valid_index(self.size, left_ind) and not util.is_left_edge(self.size, index):
            if (left_ind // self.size == index // self.size) and self.points[left_ind] == POINT_EMPTY:
                lib += 1

        if util.is_valid_index(self.size, right_ind) and not util.is_right_edge(self.size, index):
            if (right_ind // self.size == index // self.size) and self.points[right_ind] == POINT_EMPTY:
                lib += 1

        if util.is_valid_index(self.size, up_ind) and not util.is_upper_edge(self.size, index):
            if self.points[up_ind] == POINT_EMPTY:
                lib += 1

        if util.is_valid_index(self.size, down_ind) and not util.is_lower_edge(self.size, index):
            if self.points[down_ind] == POINT_EMPTY:
                lib += 1

        return lib
    

    def getGroupIndices(self, index, stone_color, group_list):
        
        valid_surrounding_indices = self.getValidSurroundingIndices(index)
        valid_inds = [i for i in valid_surrounding_indices if i is not None]
        for sur_ind in valid_inds:
            if self.points[sur_ind] == stone_color and sur_ind not in group_list:
                group_list.append(sur_ind)
                self.getGroupIndices(sur_ind, stone_color, group_list)

        return group_list


    def checkIfPrisoner(self, index, stone_color):
        """
        Board.checkIfPrisoner
            args:
                index
                stone_color
            
            return value:
                True if the stone of color stone_color at index index is a prisoner
        """
        
        # Obtain the chain that index is part of, if any
        group_list = [index]
        group_indices = self.getGroupIndices(index, stone_color, group_list)
        
        total_libs = 0
        for ind in group_indices:
            total_libs += self.getSingleLiberties(ind)


        return total_libs == 0
    
    def isTerminalState(self):
        return self.terminal

    def __copy__(self):
        
        cls = self.__class__
        result = cls.__new__(cls)
        result.size = self.size
        result.num_points = self.num_points
        result.points = self.points.copy()
        result.territory = self.territory.copy()
        result.prisoners = self.prisoners.copy()
        result.is_terminal = self.is_terminal
        
        return result
