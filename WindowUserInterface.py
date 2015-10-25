from ChessBoard import BOARD_SIZE
from ChessColor import ChessColor
from ChessGame import ChessGame
from ChessPieceType import ChessPieceType
from Player import Player
from tkinter import *
import string
from PIL import Image, ImageTk
from  ChessException import ChessException

__author__ = 'Анечка'
LETTERS_ON_BOARD = string.ascii_lowercase[0:BOARD_SIZE]


def check_good_input(next_step, index1, index2, index3, index4):
    source_x = LETTERS_ON_BOARD.find(next_step[index1])
    destinaton_x = LETTERS_ON_BOARD.find(next_step[index3])
    if source_x == -1 or destinaton_x == -1:
        raise ChessException('invalid column')
    source_y = int(next_step[index2])-1
    destinaton_y = int(next_step[index4])-1
    if not (-1 < source_y < 8 and -1 < destinaton_y < 8):
        raise ChessException('Invalid row')
    return source_x, source_y, destinaton_x, destinaton_y



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


    def show(self):
        # frames = [[None for j in range(BOARD_SIZE+1)] for i in range(BOARD_SIZE+1)]
        frames = [[Frame(self.main_window, height=80, width=80, bd=0) for j in range(BOARD_SIZE+1)] for i in range(BOARD_SIZE+1)]
        labels = [[Label(frames[i][j]) for j in range(BOARD_SIZE+1)] for i in range(BOARD_SIZE+1)]
        for x in range(1, BOARD_SIZE+1):
            self.set_boards()
            for y in range(BOARD_SIZE, 0, -1):
                if self.game.board.get_square_color(x-1, y-1) == ChessColor.Black:
                    square_color = 'sienna'
                else:
                    square_color = 'khaki'
                frames[x][y] = LabelFrame(self.main_window, height=80, width=80, bg=square_color, bd=2)
                frames[x][y].grid(row=abs(y-BOARD_SIZE)+1, column=x, sticky=SW+NE)

                # labels[x][y] = Label(frames[x][y], width=7, height=3, text='x='+str(x)+'\ny='+str(y), bg=square_color)
                labels[x][y] = Button(frames[x][y], bg=square_color, width=80, height=80)
                if not self.game.board.is_empty(x-1, y-1):
                    piece = self.game.board.get_piece(x-1, y-1)
                    img = self.get_image(piece)
                    img = ImageTk.PhotoImage(img)
                else:
                    img = self.empty_image
                    labels[x][y].config(state='disabled')
                labels[x][y]['image'] = img
                labels[x][y].image = img
                labels[x][y].grid(row=abs(y-BOARD_SIZE)+1, column=x)

    def loop(self):
        self.show()
        self.main_window.mainloop()
        pass

if __name__ == '__main__':
    wui = WindowUserInterface()
    wui.loop()