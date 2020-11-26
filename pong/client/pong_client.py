import logging
import socket
import random

from pong.socket_utils import CustomSocket
from pong.socket_utils import read_json_response, sendall_json
from pong.settings import HOST, PORT
from pong.settings import WIDTH, HEIGHT
from pong.client.response import Response

logger = logging.getLogger(__name__)


class Client:
    def __init__(self, game, connect=False):
        self.game = game
        self.socket = CustomSocket()
        self.connected = False
        self.match_id = None
        self.player_id = None
        self.ready = False
        self.is_host = False
        self._is_playable = False
        if connect:
            self.connect_server()

    def connect_server(self, host=HOST, port=PORT):
        logger.info(f"trying to connect to server with host: {host} and port: {port}")
        self.socket.connect((host, port))
        
        resp = self.socket.send_read_json({
            'code': 1, 
            'params': {"match_id": None}}
        )
        self.player_id = resp.get('player_id', None)
        self.match_id = resp.get('match_id', None)
        self.is_host = resp.get("is_host", None)

        if self.player_id is None or self.match_id is None or self.is_host is None:
            raise Exception(f"format error in server response, host: {host}, port: {port}")
        
        self.connected = True
        logger.info(f"client {self.player_id} connected to server with host: {host} and port: {port}")
        logger.info(f"client {self.player_id} connected in match {self.match_id}")

    def send_position(self, player_pos, ball_pos, score):
        if not self.connected:
            self.connect_server()

        head = {
            "player_id": self.player_id,
            "match_id": self.match_id,
            "player_pos": player_pos,
            "ball_pos": ball_pos,
            "score": score
        }
        
        resp = self.socket.send_read_json({"code": 3, "params": head})
        return Response(**resp)

    def set_players_positions(self):
        if self.is_host:
            self.game.player1.set_pos(10, HEIGHT//2)
            self.game.player2.set_pos(WIDTH-10, HEIGHT//2)
        else:
            self.game.player1.set_pos(WIDTH-10, HEIGHT//2)
            self.game.player2.set_pos(10, HEIGHT//2)

    def update(self):
        response = self.send_position(
            self.game.player1.pos,
            self.game.ball.pos,
            self.game.score
        )
        
        if not self.is_host:
            self.game.ball.set_pos(*response.ball_pos)
            self.game.score = response.score
        self.game.player2.set_pos(*response.other_player_pos)

    @property
    def is_playable(self):
        if self.match_id is None:
            return False

        if not self._is_playable:
            resp = self.socket.send_read_json({"code": 2, "params": {"match_id": self.match_id}})
            self._is_playable = resp["is_playable"]
        
        return self._is_playable
