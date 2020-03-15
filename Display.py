import pygame as pg
import Board, Game, Graph
import time
import os

IMAGE_DIR = "GAME_SEQUENCE"
WIDTH = 640
HEIGHT = 640

BOARD_SIZE = 480

WHITE = ( 255, 255, 255 )
BLACK = ( 0, 0, 0 )
BROWN_1 = ( 215, 165, 7 )
BLUE_1 = ( 182, 233, 237 )
BLUE_D = ( 49, 45, 169 ) # darker
RED_1 = ( 148, 16, 16 )
PINK_1 = ( 212, 32, 164 )

class GoGUI:

    def __init__(self, board_desc):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT)) 

        self.board_desc = board_desc

        self.cell_size = (int)(BOARD_SIZE/(self.board_desc.size+1))
        self.startx = WIDTH/2 - BOARD_SIZE/2
        self.starty = WIDTH/2 - BOARD_SIZE/2
        self.stone_rad = 20
        self.draw_territory = True
        self.draw_prisoners = True
        self.statelist = []
        self.collide_rects = []
    
    def drawGrid(self):
        self.cell_size = (int)(BOARD_SIZE / (self.board_desc.size+1))

        curr_x =  self.startx
        curr_y = self.starty
        pad_x = self.cell_size
        pad_y = self.cell_size
        
        # Draw brown rect

        self.cell_fullsize = (self.board_desc.size-1)*self.cell_size
        self.board_rect = pg.Rect(self.startx, self.starty, self.cell_fullsize, self.cell_fullsize)
        pg.draw.rect( self.screen, BROWN_1, self.board_rect )

        # horizontal lines
        # 9x9 grid, so 8x8 boxes/cells
        for i in range(self.board_desc.size):
            point_from = (curr_x, curr_y)
            point_to = (curr_x + self.cell_fullsize, curr_y)
            
            pg.draw.line( self.screen, BLACK, point_from, point_to, 2 )
                            
            curr_y += pad_y

        curr_y = self.starty
        # vertical lines
        for i in range(self.board_desc.size):
            point_from = (curr_x, curr_y)
            point_to = (curr_x, curr_y + self.cell_fullsize)
            
            pg.draw.line( self.screen, BLACK, point_from, point_to, 2 )
                            
            curr_x += pad_x

    def debugDrawRects(self):
        for rect in self.collide_rects:
            pg.draw.rect(self.screen, RED_1, rect)

    def placeCollideRects(self):
        
        pad_x = pad_y = self.cell_size

        for idx, point in enumerate(self.board_desc.points):
            
            required_dy = idx // (self.board_desc.size)
            required_dx = idx % (self.board_desc.size)


            p_x = int(self.startx + required_dx * pad_x)
            p_y = int(self.starty + required_dy * pad_y)


            # center is p_x, p_y
            rect_size = 6
            
            rect = pg.Rect(p_x - rect_size , p_y -rect_size, rect_size*2, rect_size*2)
            self.collide_rects.append(rect)
    
    def drawStones(self):

        pad_x = pad_y = self.cell_size

        for idx, point in enumerate(self.board_desc.points):

            if point == Board.POINT_EMPTY:
                continue

            required_dy = idx // (self.board_desc.size)
            required_dx = idx % (self.board_desc.size)

            stone_col = WHITE if point == Board.STONE_WHITE else BLACK

            p_x = int(self.startx + required_dx * pad_x)
            p_y = int(self.starty + required_dy * pad_y)
            
            pg.draw.circle(self.screen, stone_col, (p_x,p_y), self.stone_rad, 0) # width 0, fill
            
            '''
            if self.draw_prisoners:
                val = self.board_desc.prisoners[idx]
                if val != 'o':
                    pg.draw.circle(self.screen, PINK_1, (p_x, p_y), self.stone_rad-10, 0)
            '''
    
    def drawTerritory(self):

        pad_x = pad_y = self.cell_size

        for idx, point in enumerate(self.board_desc.territory):

            if point == 'o':
                continue

            required_dy = idx // (self.board_desc.size)
            required_dx = idx % (self.board_desc.size)

            area_col = BLUE_D if point == 'w' else RED_1

            p_x = int(self.startx + required_dx * pad_x)
            p_y = int(self.starty + required_dy * pad_y)
            
            pg.draw.circle(self.screen, area_col, (p_x,p_y), self.stone_rad-10, 1) # width 0, fill

    def getBlackAction(self, button_pressed, mouse_pos):
        if not button_pressed:
            return
        
        for idx, rect in enumerate(self.collide_rects):
            if rect.collidepoint(mouse_pos):
                return idx
        return None
    
    def scoreGame(self, board_desc):
        wt, bt, wp, bp = board_desc.evaluateBoardState()
        self.board_desc = board_desc
        print("END OF GAME")
        print("Prisoners of White: ", wp)
        print("Prisoners of Black: ", bp)
        print("Territory of White: ", wt)
        print("Territory of Black: ", bt)
        self.draw_territory = True

    def updateAndSave(self, seq_no):
        self.screen.fill(BLUE_1)
        self.drawGrid()
        self.debugDrawRects()
        self.drawStones()
        if self.draw_territory:
            self.drawTerritory()
        pg.display.flip()

        pg.image.save(self.screen, "GAME_SEQUENCE/" + str(seq_no) + ".jpg")


    def mainLoop(self):
        i = 0
        x = 0       # counter to generate gameplay images
        #Initialization of game
        first_state = self.board_desc
        game = Game.Game(first_state)
        search_graph = Graph.Graph()
        root_vertex = Graph.Vertex(game, "root")
    
        self.placeCollideRects()
        
        # dir for saving image sequence
        if not os.path.exists(IMAGE_DIR):
            os.mkdir(IMAGE_DIR)

        # first display
        if x == 0:
            self.updateAndSave("throwaway")

        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_s:
                        self.scoreGame()

            left_butn, _, _ = pg.mouse.get_pressed()
            mouse_pos = pg.mouse.get_pos()

            
            if game.turn == Game.TURN_BLACK:
                res = self.getBlackAction(left_butn, mouse_pos)

                if res is not None:
                    game.turn = Game.TURN_WHITE
                    game.takeTurnBlack(res)
                    self.updateAndSave(x)
                    x += 1
            '''
            self.screen.fill(BLUE_1)
            self.drawGrid()
            self.debugDrawRects()
            self.drawStones()
            if self.draw_territory:
                self.drawTerritory()
            pg.display.flip()
            '''

            

             
            if game.turn != Game.TURN_BLACK:
                
                new_root_vert = Graph.Vertex(game, "root")
                print("[PRE-MOVE-WHITE] board state is: ")
                for i,pt in enumerate(game.board_desc.points):
                    if pt != Board.POINT_EMPTY:
                        print("p=", i,end='')
                print("")

                best_move = search_graph.monteCarloWithUCTSearch(new_root_vert)
                print("SEARCH FINISHED")
                print("BEST MOVE = ", best_move)
                print("[IMM-MOVE-WHITE] board state is:")
                for i,pt in enumerate(game.board_desc.points):
                    if pt != Board.POINT_EMPTY:
                        print("p=", i, end='')
                print("")

                game.takeTurn(best_move)
                game.turn = Game.TURN_BLACK
                self.updateAndSave(x)
                x += 1

           
            
            """
            if i < len(self.statelist)-1:
                time.sleep(0.2)
                i += 1
                self.board_desc = self.statelist[i]
            """
            

def parseBoardFromFile(file_name, size):
    with open(file_name, "r") as fi:
        data = fi.read()
    
    new_board = Board.Board()
    new_board.size = size
    new_board.resetBoard()

    # Line = row, ignore last item (whitespace)
    data = data.split("\n")


    for i, row in enumerate(data[:-1]):
        values = row.split(" ")
        for j, val in enumerate(values):
            idx = i * size + j
            
            value = Board.POINT_EMPTY
            print("VAL = ", val)
            if val == 'B':
                value = Board.STONE_BLACK
            elif val == 'W':
                value = Board.STONE_WHITE

            new_board.points[idx] = value

    return new_board 

'''
basic_board = Board.Board()
basic_board.points[3] = Board.STONE_WHITE
basic_board.points[4] = Board.STONE_WHITE
basic_board.points[29] = Board.STONE_BLACK
basic_board.points[80] = Board.STONE_WHITE # last place
'''

def main(board=None):
    if not board:
        basic_board = parseBoardFromFile("config.goconf", 9)
    else:
        basic_board = board
    (pts_white, pts_black) = basic_board.evaluateBoardState()
    print("POINTS_WHITE = ", pts_white)
    print("POINTS_BLACK = ", pts_black)
    g = GoGUI(basic_board)
    g.mainLoop()

if __name__ == '__main__':
    board = Board.Board()
    g = GoGUI(board)
    g.mainLoop()
