from flask.helpers import send_from_directory, make_response
from ChessColor import ChessColor
from ChessException import ChessException
from ChessGame import ChessGame
from ChessPiece import ChessPiece
from ChessPieceType import ChessPieceType
from Player import Player
from utils import generate_symbols_string
from web import board
from flask import render_template, request
import ChessBoard
import json

# game = ChessGame(Player('Player', 'White'), Player('Player', 'Black'))
games = {}

def get_session():
    session = request.cookies.get('session')
    if session not in games:
        session = None
    if session is None:
        session = generate_symbols_string(5)
        games[session] = ChessGame(Player('test-Player', 'White'), Player('test-Player', 'Black'))
    return session

@board.route('/')
@board.route('/index')
# @neponyatka.route('/pumpum')
# @neponyatka.route()
def index():
    user = {'nickname': 'Annie'}
    return '''
<html>
    <head>
        <title>Title</title>
    </head>
    <body>
        <h3>Hello, ''' + user['nickname'] + '''</h3>
    </body>
</html>
'''


@board.route('/pumpum')
def pumpum():
    piece = ChessPiece(ChessColor.Black, ChessPieceType.Bishop)
    posts = [
        {
            'author': {'nickname': 'Ron'},
            'body': ChessPiece(ChessColor.Black, ChessPieceType.Bishop)
        },
        {
            'author': {'nickname': 'Germiona'},
            'body': 'Ron ate the frog'
        }
    ]
    return render_template('template_square.html',
                           title='HomePage',
                           piece=piece)

@board.route('/show_line')
def show_line():
    line = [
        ChessPiece(ChessColor.Black, ChessPieceType.King),
        ChessPiece(ChessColor.White, ChessPieceType.Knight),
        ChessPiece(ChessColor.Black, ChessPieceType.Pawn)
    ]
    return render_template('template_line.html',
                           line=line)

@board.route('/show_board_ver1')
def show_board_ver1():
    board = [
        [
        ChessPiece(ChessColor.Black, ChessPieceType.King),
        ChessPiece(ChessColor.White, ChessPieceType.Knight),
        ChessPiece(ChessColor.Black, ChessPieceType.Pawn)
        ],
        [
        ChessPiece(ChessColor.White, ChessPieceType.Queen),
        ChessPiece(ChessColor.Black, ChessPieceType.Rook),
        ChessPiece(ChessColor.White, ChessPieceType.King)
        ]
    ]
    return render_template('template_board.html',
                           board=board)


@board.route('/show_board_ver2')
def show_board_ver2():
    # board = ChessGame(Player('Player', 'White'), Player('Player', 'Black')).board
    session = get_session()
    game = games[session]
    board = game.board
    resp = make_response(render_template('template_board.html', board=board))
    resp.set_cookie('session', session)
    return resp

@board.route('/move', methods=['POST'])
def move():
    global games
    session = get_session()
    game = games[session]

    try:
        source_x = int(request.form['source_x'])
        source_y = int(request.form['source_y'])
        destination_x = int(request.form['destination_x'])
        destination_y = int(request.form['destination_y'])
    except:
        return json.dumps({'status': 'Error', 'message': 'Invalid arguments (move)'})
    try:
        game.move(source_x, source_y, destination_x, destination_y)

        is_check = 0
        if game.is_black_check:
            is_check = ChessColor.Black.value
        elif game.is_white_check:
            is_check = ChessColor.White.value

        is_mate = 0
        if game.is_mate(ChessColor.Black):
            is_mate = ChessColor.Black.value
        elif game.is_mate(ChessColor.White):
            is_mate = ChessColor.White.value

        if is_mate:
            game = ChessGame(Player('Player', 'White'), Player('Player', 'Black'))
            games[session] = game

        resp = make_response(json.dumps({'status': 'Ok',
                           'is_check': is_check,
                           'is_mate': is_mate,
                           'turn': str(game.whose_turn()),
                           'board': game.board.to_json_array()
                        }))
        resp.set_cookie('session', session)
        return resp

        # return 'Ok'
    except ChessException as e:
        return json.dumps({'status': 'Error', 'message': 'Movement problem: %s' % e})

@board.route('/set_names', methods=['POST'])
def set_names():
    session = get_session()
    game = games[session]
    if request.form['white_name'] and request.form['white_surname'] and request.form['black_name'] and request.form['black_surname']:
        game.player_white = Player(request.form['white_name'], request.form['white_surname'])
        game.player_black = Player(request.form['black_name'], request.form['black_surname'])
        return json.dumps({'status': 'Ok'})
    else:
        return json.dumps(({'status': 'Error', 'message': 'Wrong player\'s data'}))


@board.route('/get_status', methods=['GET'])
def get_status():
    # session = request.cookies.get('session')
    session = get_session()
    game = games[session]
    # if session not in games:
    if game.player_white.name == 'test-Player':
        game_has_begun = False
    else:
        game_has_begun = True
    return json.dumps({'status': 'Ok', 'game_has_begun': game_has_begun, 'turn': str(game.whose_turn())})

@board.route('/hello')
def hello():
    return json.dumps({'name': 'Anna', 'surname': 'Bazhenova', 'age': 22, 'cities': ['Yekaterinburg', 'Kachkanar']})
