from enum import Enum


class ChessColor(Enum):
    Black = 1
    White = 2

    def __str__(self):
        return self._name_

    def get_short_name(self):
        return str(self)[0]

if __name__ == '__main__':
    pass