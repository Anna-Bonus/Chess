from flask import Flask


board = Flask(__name__, static_folder='static')

import views