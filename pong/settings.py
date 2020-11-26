import logging

# init base logging
logging.basicConfig(level=logging.DEBUG)

# server
HOST = '127.0.0.1'
PORT = 65432

# game
WIDTH, HEIGHT = 640, 480
NO_COLLISION = 0
PLAYER_COLLISION = 1
OUTBOUNDS = 2
