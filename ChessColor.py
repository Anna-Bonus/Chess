from enum import Enum


class ChessColor(Enum):
    Black = 1
    White = 2

    def __str__(self):
        return self._name_

    def get_short_name(self):
        return str(self)[0]

    def get_another_color(self):
        if self == ChessColor.Black:
            return ChessColor.White
        return ChessColor.Black

if __name__ == '__main__':
    pass