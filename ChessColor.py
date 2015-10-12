from enum import Enum


class ChessColor(Enum):
    Black = 1
    White = 2

    def __str__(self):
        return self._name_

if __name__ == '__main__':
    pass