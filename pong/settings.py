import logging
from enum import Enum

# init base logging
logging.basicConfig(level=logging.DEBUG)

# server
HOST = '127.0.0.1'
PORT = 65434

# server request codes
class RequestCodes():
    # update request
    CREATE_MATCH = 0
    CONNECT_MATCH = 1
    UPDATE_GAME = 3
    DISCONNECT_GAME = 5

    # get requests
    IS_PLAYABLE = 2
    MATCH_LIST = 4



# game
WIDTH, HEIGHT = 640, 480
NO_COLLISION = 0
PLAYER_COLLISION = 1
OUTBOUNDS = 2
