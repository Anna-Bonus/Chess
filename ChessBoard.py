import copy
import unittest
import string

from ChessColor import ChessColor
from ChessException import ChessException
from ChessPiece import ChessPiece
from ChessPieceType import ChessPieceType


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

    def set_piece(self, x, y, piece):
        self.board[x][y] = piece
        # exception наличия фигуры

    def get_piece(self, x, y):
        if self.is_empty(x, y):
            raise ChessException('Square %d:%d is empty' % (x, y))
        return self.board[x][y]

    def is_empty(self, x, y):
        return self.board[x][y] is None

    def clear_square(self, x, y):
        self.board[x][y] = None

    def move_piece(self, start_x, start_y, fin_x, fin_y):
        # moved_figure = copy.copy(self.get_figure(start_x, start_y))
        moved_piece = self.get_piece(start_x, start_y)
        self.clear_square(start_x, start_y)
        self.set_piece(fin_x, fin_y, moved_piece)
        # exception наличия фигуры

    def find_king(self, color):
        chess_king = ChessPiece(color, ChessPieceType.King)
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if not self.is_empty(i, j):
                    if self.get_piece(i, j) == chess_king:
                        return i, j

    def whether_go_here(self, color, destination_x, destination_y):
        result = False
        attaking_color = color
        if attaking_color == ChessColor.White:
            attacked_color = ChessColor.Black
        else:
            attacked_color = ChessColor.White
        self.set_piece(destination_x, destination_y, )
        self.set_piece(destination_x, destination_y)

    def set_start_position(self):
        next_piece = ChessPiece(ChessColor.White, ChessPieceType.Rook)
        self.set_piece(0, 0, next_piece)
        self.set_piece(7, 0, copy.copy(next_piece))
        next_piece = ChessPiece(ChessColor.White, ChessPieceType.Knight)
        self.set_piece(1, 0, next_piece)
        self.set_piece(6, 0, copy.copy(next_piece))
        next_piece = ChessPiece(ChessColor.White, ChessPieceType.Bishop)
        self.set_piece(2, 0, next_piece)
        self.set_piece(5, 0, copy.copy(next_piece))
        next_piece = ChessPiece(ChessColor.White, ChessPieceType.Queen)
        self.set_piece(3, 0, next_piece)
        next_piece = ChessPiece(ChessColor.White, ChessPieceType.King)
        self.set_piece(4, 0, next_piece)
        for i in range(0, BOARD_SIZE):
            self.set_piece(i, 1, ChessPiece(ChessColor.White, ChessPieceType.Pawn))
            for j in (6, 7):
                new_piece = copy.copy(self.get_piece(i, BOARD_SIZE - j - 1))
                new_piece.color = ChessColor.Black
                self.set_piece(i, j, new_piece)

    def clear_board(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                self.clear_square(i, j)


class ChessBoardTest(unittest.TestCase):
    def test_new_board_is_empty(self):
        board = ChessBoard()
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                self.assertTrue(board.is_empty(i, j))

    def test_start_position(self):
        board = ChessBoard()
        board.set_start_position()
        self.assertEqual(board.get_piece(0, 0), ChessPiece(ChessColor.White, ChessPieceType.Rook))
        self.assertEqual(board.get_piece(0, 1), ChessPiece(ChessColor.White, ChessPieceType.Pawn))
        self.assertEqual(board.get_piece(6, 0), ChessPiece(ChessColor.White, ChessPieceType.Knight))
        self.assertEqual(board.get_piece(2, 0), ChessPiece(ChessColor.White, ChessPieceType.Bishop))
        self.assertEqual(board.get_piece(7, 6), ChessPiece(ChessColor.Black, ChessPieceType.Pawn))
        self.assertEqual(board.get_piece(4, 7), ChessPiece(ChessColor.Black, ChessPieceType.King))
        self.assertEqual(board.get_piece(3, 7), ChessPiece(ChessColor.Black, ChessPieceType.Queen))
        self.assertEqual(board.get_piece(5, 7), ChessPiece(ChessColor.Black, ChessPieceType.Bishop))
        self.assertTrue(board.is_empty(2, 4))

    def test_set_and_clear_square(self):
        board = ChessBoard()
        board.set_piece(1, 2, ChessPiece(ChessColor.Black, ChessPieceType.Knight))
        self.assertEqual(board.board[1][2], ChessPiece(ChessColor.Black, ChessPieceType.Knight))
        board.clear_square(1, 2)
        self.assertIsNone(board.board[1][2])

    def test_set_and_get_piece(self):
        board = ChessBoard()
        board.set_piece(1, 2, ChessPiece(ChessColor.Black, ChessPieceType.Pawn))
        self.assertEqual(board.get_piece(1, 2), ChessPiece(ChessColor.Black, ChessPieceType.Pawn))

    def test_square_color(self):
        board = ChessBoard()
        self.assertEqual(board.get_square_color(1, 1), ChessColor.Black)
        self.assertEqual(board.get_square_color(2, 1), ChessColor.White)
        self.assertEqual(board.get_square_color(5, 6), ChessColor.White)
        self.assertEqual(board.get_square_color(6, 2), ChessColor.Black)
        self.assertEqual(board.get_square_color(3, 4), ChessColor.White)

    def test_move_piece(self):
        board = ChessBoard()
        board.set_start_position()
        board.move_piece(0, 1, 3, 2)
        self.assertEqual(board.get_piece(3, 2), ChessPiece(ChessColor.White, ChessPieceType.Pawn))
        self.assertTrue(board.is_empty(0, 1))

    def test_find_king(self):
        board = ChessBoard()
        board.set_start_position()
        self.assertTrue(board.find_king(ChessColor.White) == (4, 0))
        self.assertTrue(board.find_king(ChessColor.Black) == (4, 7))
        self.assertFalse(board.find_king(ChessColor.White) == (5, 3))
        self.assertFalse(board.find_king(ChessColor.White) == (0, 3))
        self.assertFalse(board.find_king(ChessColor.White) == (5, 2))

    def test_clear_board(self):
        board = ChessBoard()
        board.set_start_position()
        board.clear_board()
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                self.assertTrue(board.is_empty(i, j))

if __name__ == '__main__':
    unittest.main()


