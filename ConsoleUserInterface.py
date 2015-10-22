import sys
from ChessBoard import BOARD_SIZE
from ChessGame import ChessGame
from Player import Player
import string

STRING = string.ascii_lowercase[0:BOARD_SIZE]


class ConsoleUserInterface:
    def __init__(self):
        player1 = Player('Helen', 'P')
        player2 = Player('Bob', 'M')
        self.game = ChessGame(player1, player2)
        self.output = sys.stdout

    # Draw self.game.board and the state of the game
    def show(self):
        # for x in range(BOARD_SIZE*2 + 2):
        #     for y in range(BOARD_SIZE * 2 + 1)
        print(" +" + "=" * (BOARD_SIZE*3-1) + "+")
        for y in range(BOARD_SIZE, 0, -1):
            print(y, '|', end='', sep='')
            for x in range(BOARD_SIZE):
                if self.game.board.is_empty(x, y-1):
                    print("  |", end='')
                else:
                    piece = self.game.board.get_piece(x, y-1)
                    print(piece.get_color().get_short_name(), end='')
                    print(piece.get_type().get_short_name(), end='|')
            if y > 1:
                print('\n '+"+--"*8+"+")
        print("\n +" + "=" * (BOARD_SIZE*3-1) + "+")
        for i in range(BOARD_SIZE):
            print('  ', STRING[i], sep='', end='')
        print('\n', self.game.whose_turn(), 'turn')

    def loop(self):
        print('Please, use the international notation for game and magic word \'exit\', if you want finish')
        while 1:
            self.show()
            next_step = input(' What is next step?\n')
            if len(next_step) == 5:
                source_x = STRING.find(next_step[0])
                source_y = int(next_step[1])-1
                destinaton_x = STRING.find(next_step[3])
                destinaton_y = int(next_step[4])-1
            if 5 < len(next_step) < 8:
                source_x = STRING.find(next_step[1])
                source_y = int(next_step[2])-1
                destinaton_x = STRING.find(next_step[4])
                destinaton_y = int(next_step[5])-1
            if next_step == 'exit':
                break
            if self.game.whose_turn() == self.game.board.get_piece(source_x, source_y).get_color():
                self.game.move(source_x, source_y, destinaton_x, destinaton_y)
            else:
                print('To turn!')

if __name__ == '__main__':
    cui = ConsoleUserInterface()
    cui.loop()
