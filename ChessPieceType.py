from enum import Enum


class ChessPieceType(Enum):
    Pawn = 1
    Rook = 2
    Knight = 3
    Bishop = 4
    Queen = 5
    King = 6

    def __str__(self):
        return self._name_

if __name__ == '__main__':
    pass