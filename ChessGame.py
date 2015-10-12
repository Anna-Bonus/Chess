from ChessBoard import ChessBoard
from ChessColor import ChessColor
import unittest
from ChessFigure import ChessFigure
from ChessFigureType import ChessFigureType

__author__ = 'Анечка'


class Player:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname


class ChessGame:
    def __init__(self, player_white, player_black):
        self.board = ChessBoard()
        self.board.set_start_position()
        self.player_white = player_white
        self.player_black = player_black
        self.move_number = 1

    def move(self, source_x, source_y, destination_x, destination_y):
        self.board.move_figure(source_x, source_y, destination_x, destination_y)
        self.move_number += 1
        pass

    def whose_turn(self):
        return ChessColor.White

    def is_check(self):
        pass

    def is_pawn_move_correct(self, source_x, source_y, destination_x, destination_y):
        pawn = self.board.get_figure(source_x, source_y)
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
                color_attacked_figure = self.board.get_figure(destination_x, destination_y).get_color()
                if (source_y - destination_y == 1) and (color_pawn == ChessColor.Black) and (color_attacked_figure != color_pawn):
                    return True
                if (destination_y - source_y == 1) and (color_pawn == ChessColor.White) and (color_attacked_figure != color_pawn):
                    return True
        return False

    def is_knight_move_correct(self, source_x, source_y, destination_x, destination_y):
        # Knight should move 1 step along the first axis and two steps for the other. 1*2 = 2
        if abs(destination_x - source_x) * abs(destination_y - source_y) == 2:
            if self.board.is_empty(destination_x, destination_y):
                return True
            #if the delivery square is not empty, the figure of a different color should be there
            color_attacking_figure = self.board.get_figure(destination_x, destination_y).get_color()
            color_attacked_figure = self.board.get_figure(source_x, source_y).get_color()
            return color_attacked_figure != color_attacking_figure
        return False



class ChessGameTest(unittest.TestCase):
    def setUp(self):
        player1 = Player('Helen', 'P')
        player2 = Player('Bob', 'M')
        self.game = ChessGame(player1, player2)

    def test_pawn_movement_correct(self):
        self.assertTrue(self.game.is_pawn_move_correct(0, 1, 0, 3))
        self.assertTrue(self.game.is_pawn_move_correct(2, 1, 2, 2))
        self.assertEqual(self.game.board.get_figure(2, 1), ChessFigure(ChessColor.White, ChessFigureType.Pawn))

        self.game.move(2, 1, 3, 4)
        self.game.board.set_figure(4, 5, ChessFigure(ChessColor.Black, ChessFigureType.Pawn))
        self.assertTrue(self.game.is_pawn_move_correct(4, 5, 3, 4))

        self.game.board.set_figure(4, 5, ChessFigure(ChessColor.White, ChessFigureType.Pawn))
        self.assertFalse(self.game.is_pawn_move_correct(3, 4, 4, 5))
        self.assertTrue(self.game.board.is_empty(2, 1))

        self.game.board.set_figure(2, 3, ChessFigure(ChessColor.White, ChessFigureType.Pawn))
        self.assertFalse(self.game.is_pawn_move_correct(2, 3, 3, 4))
        self.assertTrue(self.game.is_pawn_move_correct(7, 6, 7, 4))
        self.assertTrue(self.game.is_pawn_move_correct(7, 6, 7, 5))

    def test_knight_movement_correct(self):
        self.assertTrue(self.game.is_knight_move_correct(1, 0, 2, 2))
        self.game.board.set_figure(2, 2, ChessFigure(ChessColor.Black, ChessFigureType.Pawn))
        self.assertTrue(self.game.is_knight_move_correct(1, 0, 2, 2))
        self.assertTrue(self.game.is_knight_move_correct(1, 0, 0, 2))

        self.game.board.set_figure(2, 2, ChessFigure(ChessColor.White, ChessFigureType.Pawn))
        self.assertFalse(self.game.is_knight_move_correct(1, 0, 2, 2))

        self.game.board.clear_square(4, 6)
        self.assertTrue(self.game.is_knight_move_correct(6, 7, 4, 6))
        self.assertTrue(self.game.is_knight_move_correct(6, 7, 7, 5))

        self.game.board.set_figure(4, 6, ChessFigure(ChessColor.White, ChessFigureType.Queen))
        self.assertTrue(self.game.is_knight_move_correct(6, 7, 4, 6))

        self.game.board.set_figure(4, 6, ChessFigure(ChessColor.Black, ChessFigureType.Queen))
        self.assertFalse(self.game.is_knight_move_correct(6, 7, 4, 6))

        self.game.board.set_figure(1, 3, ChessFigure(ChessColor.Black, ChessFigureType.Knight))
        self.assertTrue(self.game.is_knight_move_correct(1, 3, 2, 1))
        self.assertTrue(self.game.is_knight_move_correct(1, 3, 0, 1))
        self.assertFalse(self.game.is_knight_move_correct(1, 3, 0, 2))

        self.game.board.set_figure(2, 5, ChessFigure(ChessColor.White, ChessFigureType.Knight))
        self.assertTrue(self.game.is_knight_move_correct(1, 3, 2, 5))
        self.game.board.set_figure(2, 5, ChessFigure(ChessColor.Black, ChessFigureType.Knight))
        self.assertFalse(self.game.is_knight_move_correct(1, 3, 2, 5))

        self.game.board.set_figure(1, 3, ChessFigure(ChessColor.White, ChessFigureType.Knight))
        self.assertFalse(self.game.is_knight_move_correct(1, 3, 2, 1))
        self.assertFalse(self.game.is_knight_move_correct(1, 3, 0, 1))



if __name__ == '__main__':
    unittest.main()