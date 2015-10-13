import unittest

from ChessBoard import ChessBoard
from ChessColor import ChessColor
from ChessPiece import ChessPiece
from ChessPieceType import ChessPieceType
from Player import Player


__author__ = 'Анечка'


class ChessGame:
    def __init__(self, player_white, player_black):
        self.board = ChessBoard()
        self.board.set_start_position()
        self.player_white = player_white
        self.player_black = player_black
        self.move_number = 1

    def move(self, source_x, source_y, destination_x, destination_y):
        self.board.move_piece(source_x, source_y, destination_x, destination_y)
        self.move_number += 1
        pass

    def whose_turn(self):
        return ChessColor.White

    def is_check(self):
        pass

    def is_pawn_move_correct(self, source_x, source_y, destination_x, destination_y):
        pawn = self.board.get_piece(source_x, source_y)
        color_pawn = pawn.get_color()

        if source_x == destination_x and self.board.is_empty(destination_x, destination_y):
            if (source_y - destination_y == 1) and (color_pawn == ChessColor.Black):
                return True
            if (destination_y - source_y == 1) and (color_pawn == ChessColor.White):
                return True
            if (source_y - destination_y == 2) and (color_pawn == ChessColor.Black) and (source_y == 6) and self.board.is_empty(source_x, source_y - 1):
                return True
            if (destination_y - source_y == 2) and (color_pawn == ChessColor.White) and (source_y == 1) and self.board.is_empty(source_x, source_y + 1):
                return True
        if abs(source_x - destination_x) == 1:
            if not self.board.is_empty(destination_x, destination_y):
                color_attacked_piece = self.board.get_piece(destination_x, destination_y).get_color()
                if (source_y - destination_y == 1) and (color_pawn == ChessColor.Black) and (color_attacked_piece != color_pawn):
                    return True
                if (destination_y - source_y == 1) and (color_pawn == ChessColor.White) and (color_attacked_piece != color_pawn):
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
            if self.board.get_piece(source_x, source_y).get_color() == self.board.get_piece(destination_x, destination_y).get_color():
                return False
        difference_x = destination_x - source_x # перемещение вдоль оси Х
        difference_y = destination_y - source_y # перемещение вдоль оси Y
        # Если движение не по одной оси, ладья не может сходить так
        if (difference_x * difference_y != 0) or (difference_x + difference_y == 0):
            return False
        # Разберем 4 направления
        if difference_x < 0:
            for i in range(destination_x + 1, source_x):
                if not self.board.is_empty(i, source_y):
                    return False
        if difference_x > 0:
            for i in range(source_x + 1, destination_x):
                if not self.board.is_empty(i, source_y):
                    return False
        if difference_y > 0:
            for j in range(source_y + 1, destination_y):
                if not self.board.is_empty(source_x, j):
                    return False
        if difference_y < 0:
            for j in range(destination_y + 1, source_y):
                if not self.board.is_empty(source_x, j):
                    return False
        return True


class ChessGameTest(unittest.TestCase):
    def setUp(self):
        player1 = Player('Helen', 'P')
        player2 = Player('Bob', 'M')
        self.game = ChessGame(player1, player2)

    def test_pawn_movement_correct(self):
        self.assertTrue(self.game.is_pawn_move_correct(0, 1, 0, 3))
        self.assertTrue(self.game.is_pawn_move_correct(2, 1, 2, 2))
        self.assertEqual(self.game.board.get_piece(2, 1), ChessPiece(ChessColor.White, ChessPieceType.Pawn))

        self.game.move(2, 1, 3, 4)
        self.game.board.set_piece(4, 5, ChessPiece(ChessColor.Black, ChessPieceType.Pawn))
        self.assertTrue(self.game.is_pawn_move_correct(4, 5, 3, 4))

        self.game.board.set_piece(4, 5, ChessPiece(ChessColor.White, ChessPieceType.Pawn))
        self.assertFalse(self.game.is_pawn_move_correct(3, 4, 4, 5))
        self.assertTrue(self.game.board.is_empty(2, 1))

        self.game.board.set_piece(2, 3, ChessPiece(ChessColor.White, ChessPieceType.Pawn))
        self.assertFalse(self.game.is_pawn_move_correct(2, 3, 3, 4))
        self.assertTrue(self.game.is_pawn_move_correct(7, 6, 7, 4))
        self.assertTrue(self.game.is_pawn_move_correct(7, 6, 7, 5))

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


if __name__ == '__main__':
    unittest.main()