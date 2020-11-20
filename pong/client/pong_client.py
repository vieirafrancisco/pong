
import logging
import socket
import random
from pong.socket_utils import read_json_response, sendall_json
from pong.settings import HOST, PORT
from pong.client.response import Response

logger = logging.getLogger(__name__)

class Client:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.match_id = None
        self.player_id = None
        self.ready = False
        self.is_host = False
        self._is_playable = False

    def connect_server(self, host=HOST, port=PORT):
        logger.info(f"trying to connect to server with host: {host} and port: {port}")
        self.socket.connect((host, port))
        sendall_json(self.socket, {'connect': 'true'})
        response = read_json_response(self.socket)
        self.player_id = response.get('player_id', None)
        self.match_id = response.get('match_id', None)
        self.is_host = response.get("is_host", None)
        print("teste", self.is_host)

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
        
        sendall_json(self.socket, head)
        return Response(**read_json_response(self.socket))

    @property
    def is_playable(self):
        if not self._is_playable:
            sendall_json(self.socket, {"is_playable": True})
            self._is_playable = read_json_response(self.socket)["is_playable"]
        
        return self._is_playable