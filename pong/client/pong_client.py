import logging
import socket
import random

from pong.socket_utils import CustomSocket
from pong.socket_utils import read_json_response, sendall_json
from pong.settings import HOST, PORT, RequestCodes as r_code
from pong.settings import WIDTH, HEIGHT
from pong.client.response import Response

logger = logging.getLogger(__name__)

class ClientPlayer():
    def __init__(self, client, player_id = None, match_id = None):
        self.client = client
        self.id = player_id
        self.match_id = match_id
        self.is_host = False
        self.connected_match = False

    def connect_match(self, match_id):
        resp = self.client.send_request(r_code.CONNECT_MATCH, {"match_id": match_id})
        self.match_id = resp["match_id"]
        self.id = resp["player_id"]
        self.is_host = resp["is_host"]
        self.connected_match = True

    def disconnect_match(self):
        if not self.connected_match:
            raise Exception("client is not connected to an match")
        if self.connected_match:
            self.client.send_request(
                r_code.DISCONNECT_GAME, 
                {"match_id": self.match_id, 
                "player_id": self.id})
        
            self.match_id = None
            self.player_id = None
            self.connected_match = False
            self.is_host = False

class Client:
    def __init__(self, game, connect=False):
        self.game = game
        self.player = ClientPlayer(self)
        self.conn = CustomSocket()
        self._is_playable = False
        self.connected = False

        if connect:
            self.connect_server()

    def send_request(self, code, request):
        return self.conn.send_read_json({"code": code, "params": request})

    def connect_server(self, host=HOST, port=PORT):
        logger.info(f"trying to connect to server with host: {host} and port: {port}")
        self.conn.connect((host, port))
        self.connected = True
        logger.info(f"client connected to server with host: {host} and port: {port}")

    def send_position(self, player_pos, ball_pos, score):
        if not self.connected:
            self.connect_server()

        head = {
            "player_id": self.player.id,
            "match_id": self.player.match_id,
            "player_pos": player_pos,
            "ball_pos": ball_pos,
            "score": score
        }
        
        resp = self.send_request(r_code.UPDATE_GAME, head)
        return Response(**resp)

    def set_players_positions(self):
        if self.player.is_host:
            self.game.player1.set_pos(10, HEIGHT//2)
            self.game.player2.set_pos(WIDTH-10, HEIGHT//2)
        else:
            self.game.player1.set_pos(WIDTH-10, HEIGHT//2)
            self.game.player2.set_pos(10, HEIGHT//2)

    def get_matchs(self):
        resp = self.send_request(r_code.MATCH_LIST, {})
        return resp

    def update(self):
        response = self.send_position(
            self.game.player1.pos,
            self.game.ball.pos,
            self.game.score
        )
        
        if not self.player.is_host:
            self.game.ball.set_pos(*response.ball_pos)
            self.game.score = response.score
        self.game.player2.set_pos(*response.other_player_pos)

    @property
    def is_playable(self):
        if self.player.match_id is None:
            return False

        if not self._is_playable:
            resp = self.send_request(r_code.IS_PLAYABLE, {"match_id": self.player.match_id})
            self._is_playable = resp["is_playable"]
        
        return self._is_playable
