import chess
import threading
import time
import pygame as pg
import math as m


class Board(chess.Board):
    def __init__(self, square_size = 60, **args):
        chess.Board.__init__(self, **args)
        self.square_size = square_size
        self.font_size = min(15, square_size)
        self.active_piece = 0
        self.black = (100, 100, 100)
        self.white = (200, 200, 200)
        letters = ["k", "q", "r", "b", "n", "p"]
        self.black_piece_images = {}
        self.white_piece_images = {}
        self.active_piece = -1
        self.active_moves = []
        self.active_piece_image = self.__load_png(f"./ui/img/other/active_piece.png")
        self.possible_move_image = self.__load_png(f"./ui/img/other/possible_move.png")
        for letter in letters:
            self.black_piece_images[letter] = self.__load_png(f"./ui/img/black/{letter}.png")
            self.white_piece_images[letter] = self.__load_png(f"./ui/img/white/{letter}.png")
        


    def display(self):
        """
        Creates a thread that shows actual board on pygame screen
        """
       #self.__display()
        start = threading.Thread(target = self.__display)
        start.start()


    def __display(self):
        pg.init()
        pg.font.init()
        pg.display.set_caption('')
        self.screen = pg.display.set_mode([8 * self.square_size, 8 * self.square_size])
        self.font = pg.font.SysFont('Helvetica', self.font_size)
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            self.screen.fill(self.black)
            self.__draw_board()
            self.__update_active_piece()
            self.__draw_figures()
            self.__draw_letters()
            self.__check_if_piece_selected()
            #print(self.active_moves)
            self.__highlight_possible_moves()
            pg.display.flip()
        pg.quit()

    def __draw_board(self):
        for x in range(0, 8 * self.square_size, self.square_size):
            for y in range(x % (2 * self.square_size),
             x % (2 * self.square_size) + 8 * self.square_size,
             self.square_size * 2):
                pg.draw.rect(self.screen, self.white, (x, y, self.square_size, self.square_size))

    def __draw_letters(self):
        """
        function that draw letters 
        """
        for y, index in zip(
            range(1,8 * self.square_size, self.square_size),
            range(8, 0, -1),
            ):
            text_surface = self.font.render(str(index), False, (0, 0, 0))
            self.screen.blit(text_surface, (1,y))
        
        for x, index in zip(
            range(self.square_size - self.font_size, 8 * self.square_size, self.square_size),
            range(65, 73),
            ):
            text_surface = self.font.render(chr(index), False, (0, 0, 0))
            self.screen.blit(text_surface, (x,self.square_size * 8 - self.font_size)) 

    def __load_png(self, filename):
            piece = pg.image.load(filename)
            piece = pg.transform.scale(piece, (self.square_size, self.square_size))
            return piece

    def __draw_figures(self):
        # function that does not work because pip install pynanosvg does not work
        # this function should display images from svg files, not png
        def load_svg(filename, surface, position, size=None):
            from svg import Parser, Rasterizer
            if size is None:
                w = surface.get_width()
                h = surface.get_height()
            else:
                w, h = size
            svg = Parser.parse_file(filename)
            rast = Rasterizer()
            buff = rast.rasterize(svg, w, h)
            image = pg.image.frombuffer(buff, (w, h), 'ARGB')
            surface.blit(image, position)

        
        #load_png("./img/black/p.png", self.screen, (0,0), (self.square_size, self.square_size))


        for index, piece in self.piece_map().items():
            if piece.color:
                self.screen.blit(
                    self.white_piece_images[piece.symbol().lower()],
                    (
                        chess.square_file(index) * self.square_size,
                        (7 - chess.square_rank(index)) * self.square_size,
                        self.square_size,
                        self.square_size
                    )
                )
            else:
                self.screen.blit(
                    self.black_piece_images[piece.symbol().lower()],
                    (
                        chess.square_file(index) * self.square_size,
                        (7 - chess.square_rank(index)) * self.square_size,
                        self.square_size,
                        self.square_size
                    )
                )

    def __square_number(self, pos):
        x, y = pos
        x = m.floor(x / self.square_size)
        y = 7 - m.floor(y / self.square_size)
        return x + 8 * y

    def __update_active_piece(self):
        if not self.active_piece == -1:
            self.screen.blit(
                    self.active_piece_image,
                    (
                        chess.square_file(self.active_piece) * self.square_size,
                        (7 - chess.square_rank(self.active_piece)) * self.square_size,
                        self.square_size,
                        self.square_size
                    )
                )
    
    def __check_if_piece_selected(self):
        """
        This function sets activie_piece to index of highlighted piece or -1 of none of the
        pieces is active.
        """
        self.__square_number(pg.mouse.get_pos())
        if pg.mouse.get_pressed()[0]:
            if self.__square_number(pg.mouse.get_pos()) in self.piece_map().keys():
                if self.piece_map()[self.__square_number(pg.mouse.get_pos())].color == self.turn:
                    self.active_piece = self.__square_number(pg.mouse.get_pos())
                    #self.active_moves = []
                elif not self.active_piece == -1:   
                    if self.__square_number(pg.mouse.get_pos()) in [move.to_square for move in self.__legal_moves_from_square(self.active_piece)]:
                        self.push(self.find_move(self.active_piece, self.__square_number(pg.mouse.get_pos())))
                        self.active_piece = -1
                        self.active_moves = []


            elif not self.active_piece == -1:   
                if self.__square_number(pg.mouse.get_pos()) in [move.to_square for move in self.__legal_moves_from_square(self.active_piece)]:
                    self.push(self.find_move(self.active_piece, self.__square_number(pg.mouse.get_pos())))
                    self.active_piece = -1
                    self.active_moves = []


        if not self.active_piece == -1:
            if not self.piece_map()[self.active_piece].color == self.turn:
                self.active_piece = -1

    def __legal_moves_from_square(self, square):
        """
        This function returns moves available in position that begins in particular square.
        """
        for move in self.legal_moves:
            if move.from_square == square:
                yield move

    def __highlight_possible_moves(self):
        if not self.active_piece == -1:
            for move in self.__legal_moves_from_square(self.active_piece):
                self.screen.blit(
                        self.possible_move_image,
                        (
                            chess.square_file(move.to_square) * self.square_size,
                            (7 - chess.square_rank(move.to_square)) * self.square_size,
                            self.square_size,
                            self.square_size
                        )
                    )


    


        




      