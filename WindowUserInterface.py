from ChessBoard import BOARD_SIZE
from ChessColor import ChessColor
from ChessGame import ChessGame
from ChessPieceType import ChessPieceType
from Player import Player
import string, copy
from time import time
from tkinter import *
from PIL import Image, ImageTk
__author__ = 'Анечка'
LETTERS_ON_BOARD = string.ascii_lowercase[0:BOARD_SIZE]
SQUARE_SIZE = 80

class WindowUserInterface:
    def __init__(self):
        player1 = Player('Helen', 'P')
        player2 = Player('Bob', 'M')
        self.game = ChessGame(player1, player2)
        self.main_window = Tk()
        self.CHESS_PIECE_IMAGES = {}
        self.empty_image = ImageTk.PhotoImage(Image.open('Empty_Image.png'))
        for piece_type in ChessPieceType:
            for color in ChessColor:
                self.CHESS_PIECE_IMAGES[str(color)+'_'+str(piece_type)] = Image.open(str(color)+'_'+str(piece_type)+'.png')
        self.first_chose_was_done = False
        self.source_coordinates = None


    def get_image(self, chess_piece):
        return self.CHESS_PIECE_IMAGES[str(chess_piece)]

    def set_boards(self):
        for x in range(1, BOARD_SIZE+1):
            top_letter = Label(self.main_window, text=LETTERS_ON_BOARD[x-1])
            top_letter.grid(row=0, column=x)
            down_letter = Label(self.main_window, text=LETTERS_ON_BOARD[x-1])
            down_letter.grid(row=9, column=x)
        for y in range(BOARD_SIZE, 0, -1):
            left_letter = Label(self.main_window, text=y)
            left_letter.grid(row=abs(y-BOARD_SIZE)+1, column=0)
            right_letter = Label(self.main_window, text=y)
            right_letter.grid(row=abs(y-BOARD_SIZE)+1, column=BOARD_SIZE+1)

    def click_handler(self, x, y):
        print("Click on %d:%d" % (x, y))
        if self.first_chose_was_done:
            (source_x, source_y) = self.source_coordinates
            destination_x, destination_y = (x, y)
            if self.game.is_move_correct(source_x, source_y, destination_x, destination_y):
                self.first_chose_was_done = False
                self.game.previous_board = copy.deepcopy(self.game.board)
                self.game.move(source_x, source_y, destination_x, destination_y)
                print(self.game.squares_changed_last_move())
                self.show_this_squares(self.game.squares_changed_last_move())
                #print('From '+str(source_x)+str(source_y)+'to'+str(destination_x)+str(destination_y))
            else:
                self.source_coordinates = None
                self.first_chose_was_done = False
                self.show_mistake('Wrong move!')
        else:
            if self.game.board.is_empty(x, y):
                self.show_mistake('You can\'t go from empty square')
            else:
                if self.game.whose_turn() != self.game.board.get_piece(x, y).get_color():
                    self.show_mistake(str(self.game.whose_turn())+' player\'s turn!')
                else:
                    self.first_chose_was_done = True
                    self.source_coordinates = (x, y)
        # self.show_this_squares(self.game.squares_changed_last_move())
        #self.show()

    def show_mistake(self, message):
        #print(self.main_window.geometry())
        mistake_window = Toplevel()
        mistake_message = Label(mistake_window, text=message)
        mistake_message.pack()
        mistake_window.geometry('80x90+600+355')
        # mistake_window.mainloop()

    def show_this_squares(self, array):
        for (i, j) in array:
            print('Redraw %d:%d' % (i, j))
            if self.game.board.get_square_color(i, j) == ChessColor.Black:
                square_color = 'sienna'
            else:
                square_color = 'khaki'
            #print('Turn for '+str(self.game.whose_turn()))
            #if self.game.board.is_empty(i, j):
            # self.frames[i+1][j+1] = Frame(self.main_window, height=80, width=80, bd=0, bg=square_color)
            self.frames[i+1][j+1].config(bg=square_color)
            self.frames[i+1][j+1].bind("<Button-1>", lambda g, ii=i, jj=j: self.click_handler(ii, jj))
            self.frames[i+1][j+1].grid(row=abs(j+1-BOARD_SIZE)+1, column=i+1, sticky=S+W+N+E)
            # else:
            if not self.game.board.is_empty(i, j):
                #self.labels = [[Label(self.frames[i][j]) for j in range(BOARD_SIZE+1)] for i in range(BOARD_SIZE+1)]
                #self.labels[i+1][j+1].config(bg=square_color)
                self.labels[i+1][j+1]['bg']=square_color
                piece = self.game.board.get_piece(i, j)
                #print(piece)
                img = self.get_image(piece)
                img = ImageTk.PhotoImage(img)
                self.labels[i+1][j+1]['image'] = img
                self.labels[i+1][j+1].image = img
                self.labels[i+1][j+1].bind("<Button-1>", lambda t, x=i, y=j: self.click_handler(x, y))
                self.labels[i+1][j+1].pack()
            else:
                #self.labels[i+1][j+1]['image'] = ''
                self.labels[i+1][j+1]['image'] = self.empty_image
                self.labels[i+1][j+1].image = self.empty_image

    def show(self):
        self.frames = [[Frame(self.main_window, height=SQUARE_SIZE, width=SQUARE_SIZE, bd=0) for j in range(BOARD_SIZE + 1)] for i in
                      range(BOARD_SIZE + 1)]
        self.labels = [[Label(self.frames[i][j], width=SQUARE_SIZE-10, height=SQUARE_SIZE-10) for j in range(BOARD_SIZE+1)] for i in range(BOARD_SIZE+1)]
        if not self.first_chose_was_done:
            print('Turn for '+str(self.game.whose_turn()))
        squares_array = []
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                squares_array.append((i, j))
        #print(massiv)
        self.show_this_squares(squares_array)
        # for x in range(1, BOARD_SIZE+1):
        #     self.set_boards()
        #     for y in range(BOARD_SIZE, 0, -1):
        #         self.show_this_squares((x-1, y-1))
            #     if self.game.board.get_square_color(x-1, y-1) == ChessColor.Black:
            #         square_color = 'sienna'
            #     else:
            #         square_color = 'khaki'
            #     self.frames[x][y] = LabelFrame(self.main_window, height=80, width=80, bg=square_color, bd=2)
            #     self.frames[x][y].bind("<Button-1>", lambda g, xx=x, yy=y: self.click_handler(xx-1, yy-1))
            #     self.frames[x][y].grid(row=abs(y-BOARD_SIZE)+1, column=x, sticky=SW+NE)
            #     self.labels[x][y] = Button(self.frames[x][y], bg=square_color, width=80, height=80)
            #     if not self.game.board.is_empty(x-1, y-1):
            #         piece = self.game.board.get_piece(x-1, y-1)
            #         img = self.get_image(piece)
            #         img = ImageTk.PhotoImage(img)
            #         self.labels[x][y]['image'] = img
            #         self.labels[x][y].image = img
            #         self.labels[x][y].bind("<Button-1>", lambda t, x=x, y=y: self.click_handler(x-1, y-1))
            #         self.labels[x][y].grid(row=abs(y-BOARD_SIZE)+1, column=x)


    def loop(self):
        self.show()
        self.main_window.mainloop()
        pass

if __name__ == '__main__':
    wui = WindowUserInterface()
    wui.loop()