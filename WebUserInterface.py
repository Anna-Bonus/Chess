import ChessBoard

class WebUserInterface:
    def __init__(self):
        from web import board
        self.board = board

    def run(self):
        self.board.run(debug=True)



if __name__ == '__main__':
    wui = WebUserInterface()
    wui.run()