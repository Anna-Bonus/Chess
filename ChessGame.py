import unittest

from ChessBoard import ChessBoard
from ChessColor import ChessColor
from ChessPiece import ChessPiece
from ChessPieceType import ChessPieceType
from Player import Player


__author__ = 'Анечка'


def sign(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0


class ChessGame:
    def __init__(self, player_white, player_black):
        self.board = ChessBoard()
        self.board.set_start_position()
        self.player_white = player_white
        self.player_black = player_black
        self.move_number = 1

    def move(self, source_x, source_y, destination_x, destination_y):
        if self.is_move_correct(source_x, source_y, destination_x, destination_y):
            self.board.move_piece(source_x, source_y, destination_x, destination_y)
            self.move_number += 1

    def whose_turn(self):
        if self.move_number % 2 == 0:
            return ChessColor.Black
        return ChessColor.White

    def where_is_king(self, color):
        for i in range(0, 8):
            for j in range(0, 8):
                if not self.board.is_empty(i, j):
                    if self.board.get_piece(i, j) == ChessPiece(color, ChessPieceType.King):
                        return i, j

    def is_check_for_white(self):
        (king_x, king_y) = self.where_is_king(ChessColor.White)
        for i in range(0, 8):
            for j in range(0, 8):
                if self.is_move_correct(i, j, king_x, king_y):
                    return True
        return False

    def is_check_for_black(self):
        (king_x, king_y) = self.where_is_king(ChessColor.Black)
        for i in range(0, 8):
            for j in range(0, 8):
                if self.is_move_correct(i, j, king_x, king_y):
                    return True
        return False

    # Проверяет, что
    # в клетке [source] есть фигура
    # если в клетке [destination] есть фигура, то она другого цвета
    # TODO: если в [source] стоит король, то отдельно проверяем рокировку
    def is_move_correct(self, source_x, source_y, destination_x, destination_y):
        if self.board.is_empty(source_x, source_y):
            return False
        source_color = self.board.get_piece(source_x, source_y).get_color()
        if not self.board.is_empty(destination_x, destination_y):
            destination_color = self.board.get_piece(destination_x, destination_y).get_color()
            if source_color == destination_color:
                return False
        checkers = {ChessPieceType.Pawn: self.is_pawn_move_correct,
                    ChessPieceType.Rook: self.is_rook_move_correct,
                    ChessPieceType.Bishop: self.is_bishop_move_correct,
                    ChessPieceType.Queen: self.is_queen_move_is_correct,
                    ChessPieceType.King: self.is_king_move_correct,
                    ChessPieceType.Knight: self.is_knight_move_correct}
        piece_type = self.board.get_piece(source_x, source_y).get_type()
        result = checkers[piece_type](source_x, source_y, destination_x, destination_y)
        return result

    def is_pawn_move_correct(self, source_x, source_y, destination_x, destination_y):
        pawn = self.board.get_piece(source_x, source_y)
        color_pawn = pawn.get_color()

        if source_x == destination_x and self.board.is_empty(destination_x, destination_y):
            if (source_y - destination_y == 1) and (color_pawn == ChessColor.Black):
                return True
            if (destination_y - source_y == 1) and (color_pawn == ChessColor.White):
                return True
            if (source_y - destination_y == 2) and (color_pawn == ChessColor.Black) and (
                        source_y == 6) and self.board.is_empty(source_x, source_y - 1):
                return True
            if (destination_y - source_y == 2) and (color_pawn == ChessColor.White) and (
                        source_y == 1) and self.board.is_empty(source_x, source_y + 1):
                return True
        if abs(source_x - destination_x) == 1:
            if not self.board.is_empty(destination_x, destination_y):
                color_attacked_piece = self.board.get_piece(destination_x, destination_y).get_color()
                if (source_y - destination_y == 1) and (color_pawn == ChessColor.Black) and (
                            color_attacked_piece != color_pawn):
                    return True
                if (destination_y - source_y == 1) and (color_pawn == ChessColor.White) and (
                            color_attacked_piece != color_pawn):
                    return True
        return False

    def is_knight_move_correct(self, source_x, source_y, destination_x, destination_y):
        # Knight should move 1 step along the first axis and two steps for the other. 1*2 = 2
        if abs(destination_x - source_x) * abs(destination_y - source_y) == 2:
            if self.board.is_empty(destination_x, destination_y):
                return True
            # if the delivery square is not empty, the figure of a different color should be there
            color_attacking_piece = self.board.get_piece(destination_x, destination_y).get_color()
            color_attacked_piece = self.board.get_piece(source_x, source_y).get_color()
            return color_attacked_piece != color_attacking_piece
        return False

    def is_rook_move_correct(self, source_x, source_y, destination_x, destination_y):
        # Проверим, что в пункте назначения не стоит фигура того же цвета, что и наша
        if not self.board.is_empty(destination_x, destination_y):
            if self.board.get_piece(source_x, source_y).get_color() == self.board.get_piece(destination_x,
                                                                                            destination_y).get_color():
                return False
        difference_x = destination_x - source_x  # перемещение вдоль оси Х
        difference_y = destination_y - source_y  # перемещение вдоль оси Y
        # Если движение не по одной оси, ладья не может сходить так
        if (difference_x * difference_y != 0) or (difference_x + difference_y == 0):
            return False
        # направление по осям
        factor_x = sign(difference_x)
        factor_y = sign(difference_y)
        for index in range(1, abs(difference_x)):
            if not self.board.is_empty(source_x + factor_x * index, source_y + factor_y * index):
                return False
        for index in range(1, abs(difference_y)):
            if not self.board.is_empty(source_x + factor_x * index, source_y + factor_y * index):
                return False
        return True

    def is_king_move_correct(self, source_x, source_y, destination_x, destination_y):
        # Проверим, что в пункте назначения не стоит фигура того же цвета, что и наша
        if not self.board.is_empty(destination_x, destination_y):
            if self.board.get_piece(source_x, source_y).get_color() == self.board.get_piece(destination_x,
                                                                                            destination_y).get_color():
                return False
        difference_x = destination_x - source_x  # перемещение вдоль оси Х
        difference_y = destination_y - source_y  # перемещение вдоль оси Y
        if abs(difference_x) <= 1 and abs(difference_y) <= 1:
            return True
        return False

    def is_bishop_move_correct(self, source_x, source_y, destination_x, destination_y):
        # Проверим, что в пункте назначения не стоит фигура того же цвета, что и наша
        if not self.board.is_empty(destination_x, destination_y):
            if self.board.get_piece(source_x, source_y).get_color() == self.board.get_piece(destination_x,
                                                                                            destination_y).get_color():
                return False
        difference_x = destination_x - source_x  # перемещение вдоль оси Х
        difference_y = destination_y - source_y  # перемещение вдоль оси Y
        if abs(destination_x - source_x) != abs(destination_y - source_y):
            return False
        # направление по осям
        factor_x = sign(difference_x)
        factor_y = sign(difference_y)
        for index in range(1, abs(difference_x)):
            if not self.board.is_empty(source_x + factor_x * index, source_y + factor_y * index):
                return False
        return True

    def is_queen_move_is_correct(self, source_x, source_y, destination_x, destination_y):
        return self.is_bishop_move_correct(source_x, source_y, destination_x, destination_y) or \
               self.is_rook_move_correct(source_x, source_y, destination_x, destination_y)


class ChessGameTest(unittest.TestCase):
    def setUp(self):
        player1 = Player('Helen', 'P')
        player2 = Player('Bob', 'M')
        self.game = ChessGame(player1, player2)

    def test_pawn_movement_correct(self):
        self.assertTrue(self.game.is_pawn_move_correct(0, 1, 0, 3))
        self.assertTrue(self.game.is_pawn_move_correct(2, 1, 2, 2))
        self.assertEqual(self.game.board.get_piece(2, 1), ChessPiece(ChessColor.White, ChessPieceType.Pawn))

        self.game.board.set_piece(3, 4, ChessPiece(ChessColor.White, ChessPieceType.Pawn))
        self.game.board.set_piece(4, 5, ChessPiece(ChessColor.Black, ChessPieceType.Pawn))
        self.assertTrue(self.game.is_pawn_move_correct(4, 5, 3, 4))

        self.game.board.set_piece(4, 5, ChessPiece(ChessColor.White, ChessPieceType.Pawn))
        self.assertFalse(self.game.is_pawn_move_correct(3, 4, 4, 5))

        self.game.board.set_piece(2, 3, ChessPiece(ChessColor.White, ChessPieceType.Pawn))
        self.assertFalse(self.game.is_pawn_move_correct(2, 3, 3, 4))
        self.assertTrue(self.game.is_pawn_move_correct(7, 6, 7, 4))
        self.assertTrue(self.game.is_pawn_move_correct(7, 6, 7, 5))

        self.game.board.set_piece(7, 5, ChessPiece(ChessColor.White, ChessPieceType.King))
        self.assertFalse(self.game.is_pawn_move_correct(7, 6, 7, 4))
        self.assertFalse(self.game.is_pawn_move_correct(7, 6, 7, 5))

    def test_knight_movement_correct(self):
        self.assertTrue(self.game.is_knight_move_correct(1, 0, 2, 2))
        self.game.board.set_piece(2, 2, ChessPiece(ChessColor.Black, ChessPieceType.Pawn))
        self.assertTrue(self.game.is_knight_move_correct(1, 0, 2, 2))
        self.assertTrue(self.game.is_knight_move_correct(1, 0, 0, 2))

        self.game.board.set_piece(2, 2, ChessPiece(ChessColor.White, ChessPieceType.Pawn))
        self.assertFalse(self.game.is_knight_move_correct(1, 0, 2, 2))

        self.game.board.clear_square(4, 6)
        self.assertTrue(self.game.is_knight_move_correct(6, 7, 4, 6))
        self.assertTrue(self.game.is_knight_move_correct(6, 7, 7, 5))

        self.game.board.set_piece(4, 6, ChessPiece(ChessColor.White, ChessPieceType.Queen))
        self.assertTrue(self.game.is_knight_move_correct(6, 7, 4, 6))

        self.game.board.set_piece(4, 6, ChessPiece(ChessColor.Black, ChessPieceType.Queen))
        self.assertFalse(self.game.is_knight_move_correct(6, 7, 4, 6))

        self.game.board.set_piece(1, 3, ChessPiece(ChessColor.Black, ChessPieceType.Knight))
        self.assertTrue(self.game.is_knight_move_correct(1, 3, 2, 1))
        self.assertTrue(self.game.is_knight_move_correct(1, 3, 0, 1))
        self.assertFalse(self.game.is_knight_move_correct(1, 3, 0, 2))

        self.game.board.set_piece(2, 5, ChessPiece(ChessColor.White, ChessPieceType.Knight))
        self.assertTrue(self.game.is_knight_move_correct(1, 3, 2, 5))
        self.game.board.set_piece(2, 5, ChessPiece(ChessColor.Black, ChessPieceType.Knight))
        self.assertFalse(self.game.is_knight_move_correct(1, 3, 2, 5))

        self.game.board.set_piece(1, 3, ChessPiece(ChessColor.White, ChessPieceType.Knight))
        self.assertFalse(self.game.is_knight_move_correct(1, 3, 2, 1))
        self.assertFalse(self.game.is_knight_move_correct(1, 3, 0, 1))

    def test_rook_movement_correct(self):
        self.assertFalse(self.game.is_rook_move_correct(0, 0, 0, 2))
        self.game.board.clear_square(0, 1)
        self.assertTrue(self.game.is_rook_move_correct(0, 0, 0, 2))

        self.game.board.move_piece(4, 1, 4, 3)
        self.assertTrue(self.game.is_rook_move_correct(4, 3, 4, 6))
        self.assertFalse(self.game.is_rook_move_correct(4, 3, 4, 7))

        self.game.board.set_piece(4, 6, ChessPiece(ChessColor.White, ChessPieceType.Pawn))
        self.assertFalse(self.game.is_rook_move_correct(4, 3, 4, 6))
        self.assertFalse(self.game.is_rook_move_correct(4, 3, 6, 4))

        self.game.board.set_piece(6, 3, ChessPiece(ChessColor.Black, ChessPieceType.Pawn))
        self.assertTrue(self.game.is_rook_move_correct(4, 3, 6, 3))
        self.assertFalse(self.game.is_rook_move_correct(4, 3, 7, 3))
        self.assertFalse(self.game.is_rook_move_correct(4, 3, 6, 6))

        self.game.board.set_piece(2, 3, ChessPiece(ChessColor.White, ChessPieceType.Pawn))
        self.assertFalse(self.game.is_rook_move_correct(4, 3, 2, 3))
        self.assertFalse(self.game.is_rook_move_correct(4, 3, 1, 3))
        self.assertTrue(self.game.is_rook_move_correct(4, 3, 3, 3))
        self.assertTrue(self.game.is_rook_move_correct(4, 3, 4, 1))
        self.assertFalse(self.game.is_rook_move_correct(4, 3, 4, 0))

        self.game.board.set_piece(4, 0, ChessPiece(ChessColor.Black, ChessPieceType.King))
        self.assertTrue(self.game.is_rook_move_correct(4, 3, 4, 0))

    def test_king_movement_correct(self):
        self.assertFalse(self.game.is_king_move_correct(4, 0, 4, 1))
        self.assertTrue(self.game.is_king_move_correct(4, 1, 4, 2))
        self.assertTrue(self.game.is_king_move_correct(4, 1, 5, 2))

        self.game.board.set_piece(4, 3, ChessPiece(ChessColor.Black, ChessPieceType.King))
        self.assertFalse(self.game.is_king_move_correct(4, 3, 4, 1))
        self.assertTrue(self.game.is_king_move_correct(4, 3, 4, 2))

        self.game.move(4, 1, 4, 2)
        self.assertTrue(self.game.is_king_move_correct(4, 3, 4, 2))
        self.assertTrue(self.game.is_king_move_correct(4, 3, 5, 4))

        self.game.board.set_piece(5, 4, ChessPiece(ChessColor.Black, ChessPieceType.Knight))
        self.assertFalse(self.game.is_king_move_correct(4, 3, 5, 4))

        self.game.board.set_piece(3, 3, ChessPiece(ChessColor.White, ChessPieceType.Pawn))
        self.assertTrue(self.game.is_king_move_correct(4, 3, 3, 3))

    def test_bishop_movement_correct(self):
        self.assertTrue(self.game.is_bishop_move_correct(3, 1, 5, 3))
        self.assertTrue(self.game.is_bishop_move_correct(6, 1, 2, 5))
        self.assertFalse(self.game.is_bishop_move_correct(3, 1, 4, 0))

        self.game.board.set_piece(4, 0, ChessPiece(ChessColor.Black, ChessPieceType.Knight))
        self.assertTrue(self.game.is_bishop_move_correct(3, 1, 4, 0))
        self.assertTrue(self.game.is_bishop_move_correct(4, 0, 5, 1))

        self.game.board.set_piece(4, 4, ChessPiece(ChessColor.White, ChessPieceType.Bishop))
        self.assertTrue(self.game.is_bishop_move_correct(4, 4, 6, 6))
        self.assertFalse(self.game.is_bishop_move_correct(4, 4, 6, 1))
        self.assertFalse(self.game.is_bishop_move_correct(4, 4, 7, 7))
        self.assertFalse(self.game.is_bishop_move_correct(4, 4, 7, 1))
        self.assertFalse(self.game.is_bishop_move_correct(4, 4, 2, 4))
        self.assertTrue(self.game.is_bishop_move_correct(4, 4, 2, 6))
        self.assertTrue(self.game.is_bishop_move_correct(4, 4, 2, 2))

    def test_queen_movement_correct(self):
        self.assertTrue(self.game.is_queen_move_is_correct(5, 6, 5, 1))
        self.assertTrue(self.game.is_queen_move_is_correct(5, 6, 7, 4))
        self.assertFalse(self.game.is_queen_move_is_correct(5, 6, 4, 6))
        self.assertFalse(self.game.is_queen_move_is_correct(5, 6, 6, 3))
        self.assertTrue(self.game.is_queen_move_is_correct(5, 6, 2, 3))
        self.assertTrue(self.game.is_queen_move_is_correct(5, 6, 5, 4))
        self.assertFalse(self.game.is_queen_move_is_correct(5, 6, 4, 3))
        self.assertFalse(self.game.is_queen_move_is_correct(5, 6, 7, 5))

        self.assertTrue(self.game.is_queen_move_is_correct(2, 1, 2, 6))
        self.assertFalse(self.game.is_queen_move_is_correct(2, 1, 3, 6))
        self.assertTrue(self.game.is_queen_move_is_correct(2, 1, 7, 6))
        self.assertFalse(self.game.is_queen_move_is_correct(2, 1, 6, 6))
        self.assertTrue(self.game.is_queen_move_is_correct(2, 1, 0, 3))
        self.assertFalse(self.game.is_queen_move_is_correct(2, 1, 3, 5))

    def test_where_is_king(self):
        self.assertTrue(self.game.where_is_king(ChessColor.White) == (4, 0))
        self.assertTrue(self.game.where_is_king(ChessColor.Black) == (4, 7))
        self.assertFalse(self.game.where_is_king(ChessColor.White) == (5, 3))
        self.assertFalse(self.game.where_is_king(ChessColor.White) == (0, 3))
        self.assertFalse(self.game.where_is_king(ChessColor.White) == (5, 2))
        self.assertFalse(self.game.where_is_king(ChessColor.White) == (6, 7))
        self.assertFalse(self.game.where_is_king(ChessColor.White) == (3, 3))
        self.assertFalse(self.game.where_is_king(ChessColor.White) == (2, 1))
        self.assertFalse(self.game.where_is_king(ChessColor.White) == (0, 5))
        self.assertFalse(self.game.where_is_king(ChessColor.White) == (1, 7))

    def test_is_move_correct(self):
        self.assertTrue(self.game.is_move_correct(0, 1, 0, 2))
        self.assertTrue(self.game.is_move_correct(0, 1, 0, 3))
        self.assertTrue(self.game.is_move_correct(0, 6, 0, 4))
        self.assertTrue(self.game.is_move_correct(0, 6, 0, 5))
        self.assertTrue(self.game.is_move_correct(1, 6, 1, 4))

        self.game.board.clear_square(3, 1)
        self.assertTrue(self.game.is_move_correct(3, 0, 3, 3))

        self.game.move(3, 0, 3, 3)
        self.assertTrue(self.game.is_move_correct(3, 3, 6, 6))
        self.assertFalse(self.game.is_move_correct(3, 3, 7, 6))
        self.assertTrue(self.game.is_move_correct(3, 3, 3, 6))
        self.assertFalse(self.game.is_move_correct(3, 3, 5, 1))

        self.game.board.clear_square(5, 1)
        self.assertTrue(self.game.is_move_correct(3, 3, 5, 1))

        self.game.board.set_piece(5, 1, ChessPiece(ChessColor.Black, ChessPieceType.Bishop))
        self.assertTrue(self.game.is_move_correct(3, 3, 5, 1))
        self.assertTrue(self.game.is_move_correct(5, 1, 6, 0))
        self.assertFalse(self.game.is_move_correct(5, 1, 2, 4))

        self.assertTrue(self.game.is_move_correct(6, 0, 5, 2))
        self.assertFalse(self.game.is_move_correct(6, 0, 4, 1))

    def test_is_check(self):
        self.assertFalse(self.game.is_check_for_white())
        self.assertFalse(self.game.is_check_for_black())

        self.game.board.set_piece(4, 4, ChessPiece(ChessColor.White, ChessPieceType.King))
        self.game.board.clear_square(4, 0)
        self.assertFalse(self.game.is_check_for_white())
        self.assertFalse(self.game.is_check_for_black())

        self.game.move(4, 4, 4, 5)
        self.assertTrue(self.game.is_check_for_white())
        self.assertFalse(self.game.is_check_for_black())

        self.game.move(4, 5, 4, 4)
        self.game.board.set_piece(5, 4, ChessPiece(ChessColor.Black, ChessPieceType.King))
        self.game.board.clear_square(4, 7)
        self.assertTrue(self.game.is_check_for_white())
        self.assertTrue(self.game.is_check_for_black())

    def test_move(self):
        self.game.move(4, 1, 4, 3)
        self.game.move(4, 6, 4, 5)
        self.game.move(5, 0, 0, 5)
        self.game.move(1, 6, 0, 5)
        self.game.move(3, 0, 6, 3)
        self.assertTrue(self.game.board.is_empty(3, 0))
        self.assertTrue(self.game.board.is_empty(4, 1))
        self.assertTrue(self.game.board.is_empty(5, 0))
        self.assertTrue(self.game.board.is_empty(1, 6))
        self.assertTrue(self.game.board.is_empty(4, 6))
        self.assertEqual(self.game.board.get_piece(0, 5), ChessPiece(ChessColor.Black, ChessPieceType.Pawn))
        self.assertEqual(self.game.board.get_piece(4, 5), ChessPiece(ChessColor.Black, ChessPieceType.Pawn))
        self.assertEqual(self.game.board.get_piece(4, 3), ChessPiece(ChessColor.White, ChessPieceType.Pawn))
        self.assertEqual(self.game.board.get_piece(6, 3), ChessPiece(ChessColor.White, ChessPieceType.Queen))


if __name__ == '__main__':
    unittest.main()