import pygame as pg
import Board 

WIDTH = 640
HEIGHT = 640

BOARD_SIZE = 480

WHITE = ( 255, 255, 255 )
BLACK = ( 0, 0, 0 )

class GoGUI:

    def __init__(self, board_desc):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT)) 

        self.board_desc = board_desc

        self.cell_size = 0
        self.startx = WIDTH/2 - BOARD_SIZE/2
        self.starty = WIDTH/2 - BOARD_SIZE/2
        self.board_rect = pg.Rect( self.startx, self.starty, 
                            BOARD_SIZE, BOARD_SIZE )

    
    def drawGrid(self):
        self.cell_size = (int)(BOARD_SIZE / self.board_desc.size)

        curr_x =  self.startx
        curr_y = self.starty
        pad_x = self.cell_size
        pad_y = self.cell_size
        
        # Draw white rect
        pg.draw.rect( self.screen, WHITE, self.board_rect )

        # horizontal lines
        for i in range(self.board_desc.size+1):
            point_from = (curr_x, curr_y)
            point_to = (curr_x + BOARD_SIZE, curr_y)
            
            pg.draw.line( self.screen, BLACK, point_from, point_to, 2 )
                            
            curr_y += pad_y

        curr_y = self.starty
        # vertical lines
        for i in range(self.board_desc.size+1):
            point_from = (curr_x, curr_y)
            point_to = (curr_x, curr_y + BOARD_SIZE)
            
            pg.draw.line( self.screen, BLACK, point_from, point_to, 2 )
                            
            curr_x += pad_x


    def mainLoop(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return
            
            self.screen.fill(WHITE)
            self.drawGrid()
            pg.display.flip()


basic_board = Board.Board()
g = GoGUI(basic_board)
g.mainLoop()
