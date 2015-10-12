import copy
import unittest
import string

from ChessColor import ChessColor
from ChessException import ChessException
from ChessFigure import ChessFigure
from ChessFigureType import ChessFigureType


BOARD_SIZE = 8
SYMBOLS_STRING = string.ascii_lowercase


class ChessBoard:
    def __init__(self):
        self.board = [[None for j in range(BOARD_SIZE)] for i in range(BOARD_SIZE)]

    @staticmethod
    def get_square_color(x, y):
        if (x + y) % 2:
            return ChessColor.White
        return ChessColor.Black

    def set_figure(self, x, y, figure):
        self.board[x][y] = figure
        # exception наличия фигуры

    def get_figure(self, x, y):
        if self.is_empty(x, y):
            raise ChessException('Square %d:%d is empty' % (x, y))
        return self.board[x][y]

    def is_empty(self, x, y):
        return self.board[x][y] is None

    def clear_square(self, x, y):
        self.board[x][y] = None

    def move_figure(self, start_x, start_y, fin_x, fin_y):
        # moved_figure = copy.copy(self.get_figure(start_x, start_y))
        moved_figure = self.get_figure(start_x, start_y)
        self.clear_square(start_x, start_y)
        self.set_figure(fin_x, fin_y, moved_figure)
        # exception наличия фигуры

    def set_start_position(self):
        next_figure = ChessFigure(ChessColor.White, ChessFigureType.Rook)
        self.set_figure(0, 0, next_figure)
        self.set_figure(7, 0, copy.copy(next_figure))
        next_figure = ChessFigure(ChessColor.White, ChessFigureType.Knight)
        self.set_figure(1, 0, next_figure)
        self.set_figure(6, 0, copy.copy(next_figure))
        next_figure = ChessFigure(ChessColor.White, ChessFigureType.Bishop)
        self.set_figure(2, 0, next_figure)
        self.set_figure(5, 0, copy.copy(next_figure))
        next_figure = ChessFigure(ChessColor.White, ChessFigureType.Queen)
        self.set_figure(3, 0, next_figure)
        next_figure = ChessFigure(ChessColor.White, ChessFigureType.King)
        self.set_figure(4, 0, next_figure)
        for i in range(0, BOARD_SIZE):
            self.set_figure(i, 1, ChessFigure(ChessColor.White, ChessFigureType.Pawn))
            for j in (6, 7):
                new_figure = copy.copy(self.get_figure(i, BOARD_SIZE - j - 1))
                new_figure.color = ChessColor.Black

                self.set_figure(i, j, new_figure)


class ChessBoardTest(unittest.TestCase):
    def test_new_board_is_empty(self):
        board = ChessBoard()
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                self.assertTrue(board.is_empty(i, j))

    def test_start_position(self):
        board = ChessBoard()
        board.set_start_position()
        self.assertEqual(board.get_figure(0, 0), ChessFigure(ChessColor.White, ChessFigureType.Rook))
        self.assertEqual(board.get_figure(0, 1), ChessFigure(ChessColor.White, ChessFigureType.Pawn))
        self.assertEqual(board.get_figure(6, 0), ChessFigure(ChessColor.White, ChessFigureType.Knight))
        self.assertEqual(board.get_figure(2, 0), ChessFigure(ChessColor.White, ChessFigureType.Bishop))
        self.assertEqual(board.get_figure(7, 6), ChessFigure(ChessColor.Black, ChessFigureType.Pawn))
        self.assertEqual(board.get_figure(4, 7), ChessFigure(ChessColor.Black, ChessFigureType.King))
        self.assertEqual(board.get_figure(3, 7), ChessFigure(ChessColor.Black, ChessFigureType.Queen))
        self.assertEqual(board.get_figure(5, 7), ChessFigure(ChessColor.Black, ChessFigureType.Bishop))
        self.assertTrue(board.is_empty(2, 4))

    def test_set_and_clear_square(self):
        board = ChessBoard()
        board.set_figure(1, 2, ChessFigure(ChessColor.Black, ChessFigureType.Knight))
        self.assertEqual(board.board[1][2], ChessFigure(ChessColor.Black, ChessFigureType.Knight))
        board.clear_square(1, 2)
        self.assertIsNone(board.board[1][2])

    def test_set_and_get_figure(self):
        board = ChessBoard()
        board.set_figure(1, 2, ChessFigure(ChessColor.Black, ChessFigureType.Pawn))
        self.assertEqual(board.get_figure(1, 2), ChessFigure(ChessColor.Black, ChessFigureType.Pawn))

    def test_square_color(self):
        board = ChessBoard()
        self.assertEqual(board.get_square_color(1, 1), ChessColor.Black)
        self.assertEqual(board.get_square_color(2, 1), ChessColor.White)
        self.assertEqual(board.get_square_color(5, 6), ChessColor.White)
        self.assertEqual(board.get_square_color(6, 2), ChessColor.Black)
        self.assertEqual(board.get_square_color(3, 4), ChessColor.White)

    def test_move_figure(self):
        board = ChessBoard()
        board.set_start_position()
        board.move_figure(0, 1, 3, 2)
        self.assertEqual(board.get_figure(3, 2), ChessFigure(ChessColor.White, ChessFigureType.Pawn))
        self.assertTrue(board.is_empty(0, 1))

if __name__ == '__main__':
    unittest.main()


