from ChessColor import ChessColor
from ChessFigureType import ChessFigureType


class ChessFigure:
    def __init__(self, figure_color, figure_type):
        assert(isinstance(figure_color, ChessColor))
        assert(isinstance(figure_type, ChessFigureType))

        self.color = figure_color
        self.type = figure_type

    def __str__(self):
        return '(' + str(self.color) + ' ' + str(self.type) + ')'

    def __eq__(self, other):
        return self.color == other.color and self.type == other.type

    def __hash__(self):
        return hash(self.color) * 100 + hash(self.type)

    def get_color(self):
        return self.color


# figure = ChessFigure(ChessColor.White, ChessFigureType.King)
# print(figure)
#
# figure.color = ChessColor.Black
# print(figure)

if __name__ == '__main__':
    figure1 = ChessFigure(ChessColor.White, ChessFigureType.Bishop)
    figure2 = ChessFigure(ChessColor.White, ChessFigureType.Bishop)

    print({figure1, figure2})
