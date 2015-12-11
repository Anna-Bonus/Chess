__author__ = 'Анечка'
import string
import random

def generate_symbols_string(length):
    res = ''
    symbols = string.digits + string.ascii_letters
    for i in range(length):
        res += random.choice(symbols)
    return res

def sign(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0