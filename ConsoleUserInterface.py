import sys
from ChessBoard import BOARD_SIZE
from ChessException import ChessException
from ChessGame import ChessGame
from Player import Player
import string

LETTERS_ON_BOARD = string.ascii_lowercase[0:BOARD_SIZE]
HORIZONTAL_BORDER = " +" + "=" * (BOARD_SIZE*3-1) + "+"


def check_good_input(next_step, index1, index2, index3, index4):
    source_x = LETTERS_ON_BOARD.find(next_step[index1])
    destination_x = LETTERS_ON_BOARD.find(next_step[index3])
    if source_x == -1 or destination_x == -1:
        raise ChessException('invalid column')
    source_y = int(next_step[index2])-1
    destination_y = int(next_step[index4])-1
    if not (-1 < source_y < 8 and -1 < destination_y < 8):
        raise ChessException('Invalid row')
    return source_x, source_y, destination_x, destination_y

class ConsoleUserInterface:
    def __init__(self):
        player1 = Player('Helen', 'P')
        player2 = Player('Bob', 'M')
        self.game = ChessGame(player1, player2)
        self.output = sys.stdout
        self.input = sys.stdin

    # Draw self.game.board and the state of the game
    def show(self):
        print(HORIZONTAL_BORDER, file=self.output)
        for y in range(BOARD_SIZE, 0, -1):
            print(y, '|', end='', sep='', file=self.output)
            for x in range(BOARD_SIZE):
                if self.game.board.is_empty(x, y-1):
                    print("  |", end='', file=self.output)
                else:
                    piece = self.game.board.get_piece(x, y-1)
                    print(piece.get_color().get_short_name(), end='', file=self.output)
                    print(piece.get_type().get_short_name(), end='|', file=self.output)
            if y > 1:
                print('\n '+"+--"*8+"+", file=self.output)
        print('\n', HORIZONTAL_BORDER, sep='', file=self.output)
        print(' ', '  '.join(LETTERS_ON_BOARD), file=self.output)
        print(self.game.whose_turn(), 'turn', file=self.output)

    def loop(self):
        print('Please, use the international notation for game and magic word \'exit\', if you want finish', file=self.output)
        while 1:
            self.show()
            # next_step = input('What is next step?\n')
            print('What is the next step?', file=self.output)
            next_step = self.input.readline().rstrip()
            print(next_step)
            if len(next_step) == 5:
                try:
                    (source_x, source_y, destination_x, destination_y) = check_good_input(next_step, 0, 1, 3, 4)
                except ChessException as e:
                    print('Error:', e, file=self.output)
            if 5 < len(next_step) < 8:
                try:
                    (source_x, source_y, destination_x, destination_y) = check_good_input(next_step, 1, 2, 4, 5)
                except ChessException as e:
                    print('Error:', e, file=self.output)
            if next_step == 'exit':
                break
            if self.game.whose_turn() == self.game.board.get_piece(source_x, source_y).get_color():
                try:
                    self.game.move(source_x, source_y, destination_x, destination_y)
                except ChessException as e:
                    print('Error:', e, file=self.output)
            else:
                print('To turn!', file=self.output)

if __name__ == '__main__':
    cui = ConsoleUserInterface()
    cui.loop()
