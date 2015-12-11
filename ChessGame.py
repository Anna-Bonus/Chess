import unittest

from ChessBoard import ChessBoard, BOARD_SIZE
from ChessColor import ChessColor
from ChessPiece import ChessPiece
from ChessPieceType import ChessPieceType
from Player import Player
from utils import sign
from ChessException import ChessException
import copy
import string
import time

LETTERS_ON_BOARD = string.ascii_lowercase[0:BOARD_SIZE]
__author__ = 'Анечка'





class ChessGame:
    def __init__(self, player_white, player_black):
        self.board = ChessBoard()
        self.board.set_start_position()
        self.player_white = player_white
        self.player_black = player_black
        self.move_number = 1
        self.previous_board = copy.deepcopy(self.board)
        self.result_notation_text = ''

        self.is_white_check = False
        self.is_black_check = False

        self.possible_white_long_castling = True
        self.possible_white_short_castling = True
        self.possible_black_long_castling = True
        self.possible_black_short_castling = True

        # self.move_correct_checkers = {ChessPieceType.Pawn: self.is_pawn_move_correct,
        #     ChessPieceType.Rook: self.is_rook_move_correct,
        #     ChessPieceType.Bishop: self.is_bishop_move_correct,
        #     ChessPieceType.Queen: self.is_queen_move_is_correct,
        #     ChessPieceType.King: self.is_king_move_correct,
        #     ChessPieceType.Knight: self.is_knight_move_correct}

    def can_this_color_fix_check(self, color):
        if self.whose_turn() != color:
            return False
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if not self.board.is_empty(i, j):
                    if self.board.get_piece(i, j).get_color() == color:
                        for k in range(BOARD_SIZE):
                            for l in range(BOARD_SIZE):
                                if self.is_move_correct(i, j, k, l):
                                    attacked_piece = None
                                    if not self.board.is_empty(k, l):
                                        attacked_piece = self.board.get_piece(k, l)
                                    self.board.move_piece(i, j, k, l)
                                    if not self.is_check(color):
                                        self.board.move_piece(k, l, i, j)
                                        self.board.set_piece(k, l, attacked_piece)
                                        return True
                                    self.board.move_piece(k, l, i, j)
                                    self.board.set_piece(k, l, attacked_piece)
        return False

    def move(self, source_x, source_y, destination_x, destination_y):
        if self.board.is_empty(source_x, source_y):
            raise ChessException('Empty source square')
        source_color = self.board.get_piece(source_x, source_y).get_color()
        if self.whose_turn() != source_color:
            raise ChessException("It's "+str(source_color.get_another_color())+' turn!')

        if not self.is_move_correct(source_x, source_y, destination_x, destination_y):
            raise ChessException("Incorrect move")

        # Если это рокировка, то ладью тоже нужно передвинуть
        #self.previous_board = copy.deepcopy(self.board)
        if self.check_castling(source_x, source_y, destination_x, destination_y):
            if destination_x < source_x:
                rook_x = 0
            else:
                rook_x = BOARD_SIZE - 1
                # destination_x может быть равна только 3 или 5

            self.add_step_to_notation_if_castling(source_x, source_y, destination_x, destination_y)
            self.board.move_piece(rook_x, source_y, 3 + 2 * sign(rook_x), source_y)
        else:
            self.add_step_to_notation(source_x, source_y, destination_x, destination_y)

        self.board.move_piece(source_x, source_y, destination_x, destination_y)
        self.move_number += 1
        black_mate = self.is_mate(ChessColor.Black)
        white_mate = self.is_mate(ChessColor.White)
        if black_mate or white_mate:
            self.result_notation_text += '#'
        # Если ход был сделан Ладьей или Королем, исключаем дальнейшую возможность соответствующих рокировок
        if (source_x, source_y) == (0, 0) or (source_x, source_y) == (4, 0) or (destination_x, destination_y) == (0, 0):
            self.possible_white_long_castling = False
        if (source_x, source_y) == (7, 0) or (source_x, source_y) == (4, 0) or (destination_x, destination_y) == (7, 0):
            self.possible_white_short_castling = False
        if (source_x, source_y) == (0, 7) or (source_x, source_y) == (4, 7) or (destination_x, destination_y) == (0, 7):
            self.possible_black_long_castling = False
        if (source_x, source_y) == (7, 7) or (source_x, source_y) == (4, 7) or (destination_x, destination_y) == (7, 7):
            self.possible_black_short_castling = False

        if self.is_check(ChessColor.Black):
            self.is_black_check = True
        elif self.is_black_check:
            self.is_black_check = False
        if self.is_check(ChessColor.White):
            self.is_white_check = True
        elif self.is_white_check:
            self.is_white_check = False

        #print(self.squares_changed_last_move())

    def squares_changed_last_move(self):
        result = []
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board.is_empty(i, j) + self.previous_board.is_empty(i, j) == 1:
                    result.append((i, j))
                    #print(i, j)
                elif self.board.is_empty(i, j) + self.previous_board.is_empty(i, j) == 0:
                    if self.board.get_piece(i, j) != self.previous_board.get_piece(i, j):
                        result.append((i, j))
                        #print(self.previous_board.get_piece(i, j), self.board.get_piece(i, j))
        #print(result)
        return result

    def whose_turn(self):
        if self.move_number % 2 == 0:
            return ChessColor.Black
        return ChessColor.White

    def is_check(self, color):
        # print(type(self.board.find_king(color)))
        # self.board.show()
        (king_x, king_y) = self.board.find_king(color)
        # print('looking for ', str(color), 'King === ', king_x,' ', king_y)
        return self.can_be_attacked(king_x, king_y, color)

    def is_mate(self, color):
        t1 = time.time()
        is_check = self.is_check(color)
        t2 = time.time()
        can_fix = not self.can_this_color_fix_check(color)
        t3 = time.time()
        # print('is_check:  ' + str(t2 - t1) + '    can_fix: ' + str(t3 - t2))
        # return self.is_check(color) and not self.can_this_color_fix_check(color)
        return is_check and can_fix

    def make_check_himself(self, source_x, source_y, destination_x, destination_y):
        color = self.board.get_piece(source_x, source_y).get_color()
        self.board.move_piece(source_x, source_y, destination_x, destination_y)
        if self.is_check(color):
            self.board.move_piece(destination_x, destination_y, source_x, source_y)
            return True
        self.board.move_piece(destination_x, destination_y, source_x, source_y)
        return False

    # Проверяет, что
    # в клетке [source] есть фигура
    # если в клетке [destination] есть фигура, то она другого цвета
    # check_is_move_under_check - проверить, есть ли сейчас шах ходящему игроку, и, если есть, корректен ли ход с точки зрения этого шаха
    # (закрывает ли его при необходимости)
    def is_move_correct(self, source_x, source_y, destination_x, destination_y, check_is_move_under_check=True):
        if self.board.is_empty(source_x, source_y):
            return False
        source_color = self.board.get_piece(source_x, source_y).get_color()
        if not self.board.is_empty(destination_x, destination_y):
            destination_color = self.board.get_piece(destination_x, destination_y).get_color()
            if source_color == destination_color:
                return False
        piece_type = self.board.get_piece(source_x, source_y).get_type()
        # Check the castling
        if self.check_castling(source_x, source_y, destination_x, destination_y):
            return True
        # if self.make_check_himself(source_x, source_y, destination_x, destination_y):
        #     return False

        if check_is_move_under_check:
            if self.is_check(source_color):
                piece_under_attack = None
                if not self.board.is_empty(destination_x, destination_y):
                    piece_under_attack = self.board.get_piece(destination_x, destination_y)
                self.board.move_piece(source_x, source_y, destination_x, destination_y)

                is_check_after_move = self.is_check(source_color)

                self.board.move_piece(destination_x, destination_y, source_x, source_y)
                self.board.set_piece(destination_x, destination_y, piece_under_attack)

                if is_check_after_move:
                    return False


        return move_correct_checkers[piece_type](self, source_x, source_y, destination_x, destination_y)

    def can_be_attacked(self, x, y, color):
        result = False
        substitution_done = False
        if self.board.is_empty(x, y):
            self.board.set_piece(x, y, ChessPiece(color, ChessPieceType.Pawn))
            substitution_done = True
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.is_move_correct(i, j, x, y, check_is_move_under_check=False):
                    result = True
        if substitution_done:
            self.board.clear_square(x, y)
        return result

    def check_castling(self, source_x, source_y, destination_x, destination_y):
        if self.board.is_empty(source_x, source_y):
            return False
        if self.board.get_piece(source_x, source_y).get_type() != ChessPieceType.King:
            return False
        difference_x = destination_x - source_x
        difference_y = destination_y - source_y
        if abs(difference_x) != 2 or difference_y != 0:
            return False
        factor_x = sign(difference_x)
        # Проверям, что на пути от короля до ладьи ничего не стоит
        checking_square = [source_x + factor_x, source_y]
        while self.board.is_empty(*checking_square) and 0 <= checking_square[0] < BOARD_SIZE:
            checking_square[0] += factor_x
        if checking_square[0] < 0 or checking_square[0] >= BOARD_SIZE:
            return False
        if self.board.get_piece(*checking_square).get_type() != ChessPieceType.Rook:
            return False
        # Проверка, что король не под шахом и поле, пересекаемое или занимаемое им, не атаковано
        for i in range(3):
            checking_square = [source_x + factor_x * i, source_y]
            if self.can_be_attacked(checking_square[0], checking_square[1], self.board.get_piece(source_x, source_y).get_color()):
                return False
        # Проверяем, что данные ладья и король не делали свой ход
        if (source_x, source_y, destination_x, destination_y) == (4, 0, 2, 0) and self.possible_white_long_castling:
            return True
        if (source_x, source_y, destination_x, destination_y) == (4, 0, 6, 0) and self.possible_white_short_castling:
            return True
        if (source_x, source_y, destination_x, destination_y) == (4, 7, 2, 7) and self.possible_black_long_castling:
            return True
        if (source_x, source_y, destination_x, destination_y) == (4, 7, 6, 7) and self.possible_black_short_castling:
            return True
        return False

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

    def get_number_of_string_in_notation(self):
        return str((self.move_number+1)//2) + '. '

    def add_step_to_notation(self, source_x, source_y, destination_x, destination_y):
        moving_piece = self.board.get_piece(source_x, source_y)
        if moving_piece.get_color() == ChessColor.White:
            # str_step = '\n'*sign(self.game.move_number-1) + str((self.game.move_number+1)//2) + '. '
            # str_step = ('\n' if self.game.move_number > 1 else '' ) + str((self.game.move_number+1)//2) + '. '
            str_step = ('\n' if self.move_number > 1 else '') + self.get_number_of_string_in_notation()
        else:
            str_step = ' '
        str_step += moving_piece.get_name_for_notation()
        str_step += LETTERS_ON_BOARD[source_x] + str(source_y+1)
        if self.board.is_empty(destination_x, destination_y):
            str_step += '-'
        else:
            str_step += 'x'
        str_step += LETTERS_ON_BOARD[destination_x] + str(destination_y+1)
        self.result_notation_text += str_step

    def add_step_to_notation_if_castling(self, source_x, source_y, destination_x, destination_y):
        print('Da, castling dolzhna bit')
        if (destination_x, destination_y) == (2, 0):
            self.result_notation_text += '\n' + self.get_number_of_string_in_notation() + '0-0-0 '
        if (destination_x, destination_y) == (2, 7):
            self.result_notation_text += '0-0-0'
        if (destination_x, destination_y) == (6, 0):
            self.result_notation_text += '\n' + self.get_number_of_string_in_notation() + '0-0 '
        if (destination_x, destination_y) == (6, 7):
            self.result_notation_text += '0-0 '

move_correct_checkers = {ChessPieceType.Pawn: ChessGame.is_pawn_move_correct,
    ChessPieceType.Rook: ChessGame.is_rook_move_correct,
    ChessPieceType.Bishop: ChessGame.is_bishop_move_correct,
    ChessPieceType.Queen: ChessGame.is_queen_move_is_correct,
    ChessPieceType.King: ChessGame.is_king_move_correct,
    ChessPieceType.Knight: ChessGame.is_knight_move_correct}

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

        self.assertFalse(self.game.is_move_correct(6, 0, 5, 2))
        self.assertFalse(self.game.is_move_correct(6, 0, 4, 1))

    def test_is_check(self):
        self.assertFalse(self.game.is_check(ChessColor.White))
        self.assertFalse(self.game.is_check(ChessColor.Black))

        self.game.board.set_piece(4, 4, ChessPiece(ChessColor.White, ChessPieceType.King))
        self.game.board.clear_square(4, 0)
        self.assertFalse(self.game.is_check(ChessColor.White))
        self.assertFalse(self.game.is_check(ChessColor.Black))

        self.game.move(4, 4, 4, 5)
        self.assertTrue(self.game.is_check(ChessColor.White))
        self.assertFalse(self.game.is_check(ChessColor.Black))

        # self.game.move(4, 5, 4, 4)
        self.game.board.move_piece(4, 5, 4, 4)
        self.game.board.set_piece(5, 4, ChessPiece(ChessColor.Black, ChessPieceType.King))
        self.game.board.clear_square(4, 7)
        self.assertTrue(self.game.is_check(ChessColor.White))
        self.assertTrue(self.game.is_check(ChessColor.Black))

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

    def test_were_is_queen(self):
        self.game.move(5, 1, 5, 3)
        self.game.move(4, 6, 4, 4)
        self.game.move(5, 3, 4, 4)
        self.game.move(3, 7, 7, 3)
        self.game.move(6, 1, 6, 2)
        self.game.move(7, 3, 6, 2)
        self.game.board.show()
        self.assertEqual(self.game.board.get_piece(6, 2), ChessPiece(ChessColor.Black, ChessPieceType.Queen))

    def test_scholars_mate(self):
        self.game.board.move_piece(4, 1, 4, 3)
        self.game.board.move_piece(5, 6, 5, 4)
        self.game.board.move_piece(4, 3, 5, 4)
        self.game.board.move_piece(6, 6, 6, 4)
        self.game.move(3, 0, 7, 4)

    def test_check_move_under_check(self):
        self.game.move(5, 1, 5, 3)
        self.game.move(4, 6, 4, 4)
        self.game.move(5, 3, 4, 4)
        self.game.move(3, 7, 7, 3)
        self.assertRaises(ChessException, self.game.move, 6, 0, 5, 2)


    def test_can_be_attacked(self):
        self.game.move(4, 1, 4, 3)
        self.game.move(4, 6, 4, 4)
        self.game.move(5, 0, 0, 5)
        self.game.move(3, 7, 6, 4)

        self.assertTrue(self.game.can_be_attacked(1, 6, ChessColor.Black))
        self.assertTrue(self.game.can_be_attacked(0, 5, ChessColor.White))
        self.assertTrue(self.game.can_be_attacked(6, 1, ChessColor.White))
        self.assertTrue(self.game.can_be_attacked(3, 1, ChessColor.White))
        self.assertTrue(self.game.can_be_attacked(5, 4, ChessColor.Black))
        self.assertTrue(self.game.can_be_attacked(2, 3, ChessColor.Black))

        self.assertFalse(self.game.can_be_attacked(2, 0, ChessColor.White))
        self.assertFalse(self.game.can_be_attacked(5, 6, ChessColor.White))
        self.assertFalse(self.game.can_be_attacked(5, 6, ChessColor.Black))
        self.assertFalse(self.game.can_be_attacked(3, 4, ChessColor.White))
        self.assertFalse(self.game.can_be_attacked(3, 4, ChessColor.White))

    def test_notation(self):
        self.assertEqual(self.game.result_notation_text, '')
        self.game.move(4, 1, 4, 3)
        self.game.move(5, 6, 5, 4)
        self.game.move(4, 3, 5, 4)
        self.game.move(6, 6, 6, 4)
        self.game.move(3, 0, 7, 4)
        self.assertEqual(self.game.result_notation_text, '1. e2-e4 f7-f5\n2. e4xf5 g7-g5\n3. Qd1-h5#')

        self.game = ChessGame('Bob Marley', 'Demi Moor')
        self.game.move(3, 1, 3, 3)
        self.game.move(4, 6, 4, 4)
        self.game.move(4, 1, 4, 3)
        self.game.move(5, 7, 1, 3)
        self.assertEqual(self.game.result_notation_text, '1. d2-d4 e7-e5\n2. e2-e4 Bf8-b4')

        self.game = ChessGame('Bob Marley', 'Demi Moor')
        try:
            self.game.move(4, 1, 6, 2)
        except:
            pass
        self.assertEqual(self.game.result_notation_text, '')

    def test_castling(self):
        self.assertFalse(self.game.is_move_correct(4, 0, 2, 0))
        self.game.board.clear_board()

        self.game.board.set_piece(4, 0, ChessPiece(ChessColor.White, ChessPieceType.King))
        self.game.board.set_piece(0, 0, ChessPiece(ChessColor.White, ChessPieceType.Rook))
        self.game.board.set_piece(7, 0, ChessPiece(ChessColor.White, ChessPieceType.Rook))
        self.game.board.set_piece(1, 7, ChessPiece(ChessColor.Black, ChessPieceType.King))
        self.assertTrue(self.game.check_castling(4, 0, 2, 0))
        self.assertTrue(self.game.is_move_correct(4, 0, 2, 0))

        self.game.move(4, 0, 4, 1)
        self.game.board.move_piece(4, 1, 4, 0)
        # self.game.move(4, 1, 4, 0)
        self.assertFalse(self.game.is_move_correct(4, 0, 2, 0))
        self.assertFalse(self.game.is_move_correct(4, 0, 6, 0))
        self.game.possible_white_long_castling = True
        self.game.possible_white_short_castling = True
        self.assertTrue(self.game.is_move_correct(4, 0, 2, 0))
        self.assertTrue(self.game.is_move_correct(4, 0, 6, 0))

        self.game.board.clear_board()

        self.game.board.set_piece(4, 7, ChessPiece(ChessColor.Black, ChessPieceType.King))
        self.game.board.set_piece(0, 7, ChessPiece(ChessColor.Black, ChessPieceType.Rook))
        self.game.board.set_piece(7, 7, ChessPiece(ChessColor.Black, ChessPieceType.Rook))
        self.game.board.set_piece(2, 5, ChessPiece(ChessColor.White, ChessPieceType.King))
        self.assertTrue(self.game.check_castling(4, 7, 2, 7))
        self.assertTrue(self.game.is_move_correct(4, 7, 2, 7))

        self.game.move(4, 7, 4, 6)
        # self.game.move(4, 6, 4, 7)
        self.game.board.move_piece(4, 6, 4, 7)
        self.assertFalse(self.game.is_move_correct(4, 7, 2, 7))
        self.assertFalse(self.game.is_move_correct(4, 7, 6, 7))
        self.game.possible_black_long_castling = True
        self.game.possible_black_short_castling = True
        self.assertTrue(self.game.is_move_correct(4, 7, 2, 7))
        self.assertTrue(self.game.is_move_correct(4, 7, 6, 7))

        self.game.board.set_piece(2, 6, ChessPiece(ChessColor.White, ChessPieceType.Pawn))
        self.assertFalse(self.game.is_move_correct(4, 7, 2, 7))
        self.game.board.set_piece(2, 6, ChessPiece(ChessColor.Black, ChessPieceType.Pawn))
        self.assertTrue(self.game.is_move_correct(4, 7, 2, 7))
        self.game.board.set_piece(2, 7, ChessPiece(ChessColor.Black, ChessPieceType.Pawn))
        self.assertFalse(self.game.is_move_correct(4, 7, 2, 7))

        self.assertTrue(self.game.is_move_correct(4, 7, 6, 7))
        self.game.board.move_piece(4, 7, 6, 7)
        # self.game.move(4, 7, 6, 7)
        self.assertEqual(self.game.board.get_piece(6, 7), ChessPiece(ChessColor.Black, ChessPieceType.King))
        self.assertEqual(self.game.board.get_piece(7, 7), ChessPiece(ChessColor.Black, ChessPieceType.Rook))
        self.assertTrue(self.game.board.is_empty(4, 7))
        self.assertTrue(self.game.board.is_empty(5, 7))
        self.assertFalse(self.game.is_move_correct(4, 7, 2, 7))


if __name__ == '__main__':
    unittest.main()