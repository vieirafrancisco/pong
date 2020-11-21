
import logging
import socket
import random
from pong.socket_utils import CustomSocket
from pong.settings import HOST, PORT
from pong.client.response import Response

logger = logging.getLogger(__name__)

class Client:
    def __init__(self):
        self.socket = CustomSocket()
        self.connected = False
        self.match_id = None
        self.player_id = None
        self.ready = False
        self.is_host = False
        self._is_playable = False

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

    @property
    def is_playable(self):
        if self.match_id is None:
            return False

        if not self._is_playable:
            resp = self.socket.send_read_json({"code": 2, "params": {"match_id": self.match_id}})
            self._is_playable = resp["is_playable"]
        
        return self._is_playable