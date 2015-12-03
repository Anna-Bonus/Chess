import jsonpickle
from ChessBoard import BOARD_SIZE, ChessBoard
from ChessColor import ChessColor
from ChessGame import ChessGame
from ChessPiece import ChessPiece
from ChessPieceType import ChessPieceType
from Player import Player
import string, copy
import tkinter.filedialog as tkFileDialog
from tkinter import *
from PIL import Image, ImageTk
import sys
sys.setrecursionlimit(10000)
__author__ = 'Анечка'
LETTERS_ON_BOARD = string.ascii_lowercase[0:BOARD_SIZE]
SQUARE_SIZE = 80


# player_check = Player('Bob', 'Marley')
# print(jsonpickle.encode(player_check), file=(open('playerfile.txt', 'w')))

# TODO: load dialog, проверка корректности загруженной игры isinstance, type()==

class WindowUserInterface:
    def __init__(self):
        player1 = Player('Helen', 'P')
        player2 = Player('Bob', 'M')
        self.font_color = 'AntiqueWhite2'
        self.game = ChessGame(player1, player2)
        self.main_window = Tk()
        self.main_window.configure(background=self.font_color)
        self.main_window.title("Chess")
        self.CHESS_PIECE_IMAGES = {}
        self.empty_image = ImageTk.PhotoImage(Image.open('Empty_Image.png'))
        for piece_type in ChessPieceType:
            for color in ChessColor:
                self.CHESS_PIECE_IMAGES[str(color)+'_'+str(piece_type)] = Image.open(str(color)+'_'+str(piece_type)+'.png')
        self.first_chose_was_done = False
        self.source_coordinates = None
        self.check_shown = False
        # self.result_notation_text = ''

    def get_image(self, chess_piece):
        return self.CHESS_PIECE_IMAGES[str(chess_piece)]

    def get_square_tk_color(self, i, j):
        if self.game.board.get_square_color(i, j) == ChessColor.Black:
            return 'sienna'
        else:
            return 'khaki'

    def set_boards(self):
        for x in range(1, BOARD_SIZE+1):
            top_letter = Label(self.main_window, text=LETTERS_ON_BOARD[x-1], bg=self.font_color)
            top_letter.grid(row=0, column=x)
            down_letter = Label(self.main_window, text=LETTERS_ON_BOARD[x-1], bg=self.font_color)
            down_letter.grid(row=9, column=x)
        for y in range(BOARD_SIZE, 0, -1):
            left_letter = Label(self.main_window, text=y, bg=self.font_color)
            left_letter.grid(row=abs(y-BOARD_SIZE)+1, column=0)
            right_letter = Label(self.main_window, text=y, bg=self.font_color)
            right_letter.grid(row=abs(y-BOARD_SIZE)+1, column=BOARD_SIZE+1)

    def set_or_destroy_check_message(self):
        if self.was_mate():
            return 0
        for color in ChessColor:
            if self.game.is_check(color) and self.check_shown == False:
                self.check_message = Label(self.frame_for_data, text='Check for '+str(color), bg=self.font_color, width=20, height=1, font="Verdana 13 bold")
                self.check_message.grid(row=0, column=1)
                self.check_shown = True
        if self.check_shown and not (self.game.is_white_check or self.game.is_black_check):
            self.check_message.destroy()
            self.check_shown = False

    def was_mate(self):
        for color in ChessColor:
            if self.game.is_mate(color):
                self.end_of_game(color.get_another_color())
                return True

    def save_notation(self):
        # with open("notation.txt", "w") as out:
        #     print(self.game.result_notation_text, file=out)
        self.save_file(self.game.result_notation_text)

    def open_new_game(self):
        self.main_window.destroy()
        new = WindowUserInterface()
        new.show()

    def end_of_game(self, winner_color):
        frame_for_mate_message = Frame(self.main_window, bg='', height=50)
        frame_for_mate_message.grid(row=1, column=1, columnspan=8, rowspan=8)

        mate_message = Label(frame_for_mate_message, text=str(winner_color)+' win!', padx=80, font="Verdana 40 bold")
        mate_message.pack(side='top')

        # save_button = Button(frame_for_mate_message, text='Save notation', command=self.save_notation)
        # save_button.pack(side='left')
        #
        # new_game_button = Button(frame_for_mate_message, text='New game', command=self.open_new_game)
        # new_game_button.pack(side='right')

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                self.labels[i+1][j+1].unbind("<Button 1>")

    def click_handler(self, x, y):
        if self.first_chose_was_done:
            (source_x, source_y) = self.source_coordinates
            destination_x, destination_y = (x, y)

            if (source_x, source_y) == (destination_x, destination_y):
                self.source_coordinates = None
                self.first_chose_was_done = False
                return 0

            if not (self.game.board.is_empty(source_x, source_y) or self.game.board.is_empty(destination_x, destination_y)):
                if self.game.board.get_piece(source_x, source_y).get_color() == self.game.board.get_piece(destination_x, destination_y).get_color():
                    self.source_coordinates = (destination_x, destination_y)
                    self.first_chose_was_done = True
                    return 0

            if self.game.is_move_correct(source_x, source_y, destination_x, destination_y):
                self.first_chose_was_done = False
                self.game.previous_board = copy.deepcopy(self.game.board)
                self.game.move(source_x, source_y, destination_x, destination_y)
                self.set_or_destroy_check_message()
                self.show_this_squares(self.game.squares_changed_last_move())
                self.show_whose_turn()
                # print('From '+str(source_x)+str(source_y)+'to'+str(destination_x)+str(destination_y))
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

    def show_mistake(self, message):
        mistake_window = Toplevel()
        mistake_message = Label(mistake_window, text=message)
        mistake_message.pack()
        mistake_window.geometry('200x90+700+355')

    def show_whose_turn(self):
        self.area_whose_turn['text'] = 'Turn for ' + str(self.game.whose_turn())

    def save_file(self, saving_text):
        file = tkFileDialog.SaveAs(self.main_window, filetypes=[('*.txt files', '.txt')]).show()
        if file == '':
            return
        if not file.endswith(".txt"):
            file += ".txt"
        open(file, 'wt').write(saving_text)

    def save_game(self):
        encoded_game = jsonpickle.encode(self.game)
        # file = tkFileDialog.SaveAs(self.main_window, filetypes=[('*.txt files', '.txt')]).show()
        # if file == '':
        #     return
        # if not file.endswith(".txt"):
        #     file += ".txt"
        # open(file, 'wt').write(encoded_game)
        self.save_file(encoded_game)

    def recursive_function_for_fields(self, pending_object, object_in_normal_game):
        a = {}
        try:
            a = object_in_normal_game.__dict__.keys()
        except AttributeError:
            pass
        for field in a:
            if field.startswith('__') and field.endswith('__'):
                continue
            try:
                if type(getattr(pending_object, field)) != type(getattr(object_in_normal_game, field)):
                    print('False1')
                    return False
            except AttributeError:
                print('False2')
                return False
            print(field)
            if not self.recursive_function_for_fields(getattr(pending_object, field), getattr(object_in_normal_game, field)):
                return False
        return True

    def check_board(self, pending_board):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if not pending_board.is_empty(i, j):
                    pending_piece = pending_board.get_piece(i, j)
                    if not self.recursive_function_for_fields(pending_piece, ChessPiece(ChessColor.White, ChessPieceType.Bishop)):
                        print('False8')
                        return False
        return True

    def loaded_game_is_correct(self):
        game_for_check = ChessGame(Player('A', 'B'), Player('C', 'D'))
        if type(self.game) != ChessGame:
            return False

        if not self.recursive_function_for_fields(self.game, game_for_check):
            return False

        if not self.check_board(self.game.board):
            return False

        if type(self.game.board) != ChessBoard or type(self.game.previous_board) != ChessBoard:
            print('False5')
            return False
        if type(self.game.player_black) != Player or type(self.game.player_white) != Player:
            print('False6')
            return False
        return True

    def load_game(self):
        encoded_game = self.load_file()
        if encoded_game is None:
            return
        try:
            self.game = jsonpickle.decode(encoded_game)
        except Exception:
            self.show_mistake('Can\'t open game file')
            return
        if not self.loaded_game_is_correct():
            self.show_mistake('Object in file is not a chess game')
            return
        try:
            self.start_frame.destroy()
        except AttributeError:
            pass

        self.show()

    def load_file(self):
        file = tkFileDialog.Open(self.main_window, filetypes=[('*.txt files', '.txt')]).show()
        if file == '':
            return
        return open(file, 'r').read()

    def place_main_window(self, width, height):
        screen_width = self.main_window.winfo_screenwidth()
        screen_height = self.main_window.winfo_screenheight()
        x_coordinate = screen_width/2-width/2
        y_coordinate = screen_height/2 - height/2-20
        self.main_window.geometry('%dx%d+%d+%d' % (width, height, x_coordinate, y_coordinate))

    def show_this_squares(self, array):
        for (i, j) in array:
            if not self.game.board.is_empty(i, j):
                piece = self.game.board.get_piece(i, j)
                img = self.get_image(piece)
                img = ImageTk.PhotoImage(img)
                self.labels[i+1][j+1]['image'] = img
                self.labels[i+1][j+1].image = img
            else:
                self.labels[i+1][j+1]['image'] = self.empty_image
                self.labels[i+1][j+1].image = self.empty_image

    def show(self):
        self.frames = [[Frame(self.main_window, height=SQUARE_SIZE, width=SQUARE_SIZE, bd=0) for j in range(BOARD_SIZE + 1)] for i in
                      range(BOARD_SIZE + 1)]
        self.labels = [[Label(self.frames[i][j], width=SQUARE_SIZE-10, height=SQUARE_SIZE-10) for j in range(BOARD_SIZE + 1)] for i in range(BOARD_SIZE+1)]
        self.set_boards()
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                handler = lambda g, ii=i, jj=j: self.click_handler(ii, jj)

                self.frames[i+1][j+1]['bg'] = self.get_square_tk_color(i, j)
                self.frames[i+1][j+1].bind("<Button-1>", handler)
                self.frames[i+1][j+1].grid(row=abs(j+1-BOARD_SIZE)+1, column=i+1, sticky=S+W+N+E)

                self.labels[i+1][j+1]['bg'] = self.get_square_tk_color(i, j)
                self.labels[i+1][j+1].bind("<Button-1>", handler)
                self.labels[i+1][j+1].pack(fill='both')

        self.frame_for_data = Frame(self.main_window, bd=1, bg=self.font_color)
        self.frame_for_data.grid(column=1, row=10, columnspan=12, sticky=N)

        self.area_whose_turn = Label(self.frame_for_data, text='Turn for ' + str(self.game.whose_turn()), bg=self.font_color, width=59)
        self.area_whose_turn.grid(row=1, column=1, rowspan=1)

        self.save_button = Button(self.frame_for_data, text='Save game', command=self.save_game, width=11)
        self.save_button.grid(row=0, column=2)

        self.open_new_button = Button(self.frame_for_data, text='Open new game', command=self.open_new_game)
        self.open_new_button.grid(row=1, column=0, rowspan=1)

        self.place_main_window(618, 720)

        self.load_game_button = Button(self.frame_for_data, text='Load game', command=self.load_game, width=11)
        self.load_game_button.grid(row=1, column=2)

        self.save_notation_button = Button(self.frame_for_data, text='Save notation', command=self.save_notation, width=11)
        self.save_notation_button.grid(row=2, column=2)

        squares_array = []
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                squares_array.append((i, j))
        self.show_this_squares(squares_array)

    def show_start_view(self):
        self.start_frame = Frame(self.main_window, bg=self.font_color, bd=16)
        self.place_main_window(220, 60)
        self.start_frame.grid(row=0, column=0)
        load_button = Button(self.start_frame, text='load saved game', command=self.load_game)
        load_button.grid(row=1, column=2)
        new_game_button = Button(self.start_frame, text='start new game', command=self.open_new_game)
        new_game_button.grid(row=1, column=1)

    def loop(self):
        self.main_window.mainloop()
        pass

if __name__ == '__main__':
    wui = WindowUserInterface()
    wui.show_start_view()
    wui.loop()