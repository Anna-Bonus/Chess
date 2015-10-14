from ChessColor import ChessColor
from ChessPieceType import ChessPieceType


class ChessPiece:
    def __init__(self, piece_color, piece_type):
        assert(isinstance(piece_color, ChessColor))
        assert(isinstance(piece_type, ChessPieceType))

        self.color = piece_color
        self.type = piece_type

    def __str__(self):
        return '(' + str(self.color) + ' ' + str(self.type) + ')'

    def __eq__(self, other):
        return self.color == other.color and self.type == other.type

    def __hash__(self):
        return hash(self.color) * 100 + hash(self.type)

    def get_color(self):
        return self.color

    def get_type(self):
        return self.type

if __name__ == '__main__':
    piece1 = ChessPiece(ChessColor.White, ChessPieceType.Bishop)
    piece2 = ChessPiece(ChessColor.White, ChessPieceType.Bishop)

    print({piece1, piece2})
