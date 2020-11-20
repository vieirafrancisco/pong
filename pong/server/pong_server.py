import json
import socket
import logging
import threading
from pong.server.match import PongMatch
from pong.settings import HOST, PORT
from pong.socket_utils import read_json_response, sendall_json

logger = logging.getLogger(__name__)
match = PongMatch()


class Server:
    def __init__(self, host=HOST, port=PORT):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.games = []

    def start(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen()

        logger.info(f"Server is running in host, {self.host} and port, {self.port}")

        while(True):
            conn, addr = self.socket.accept()
            logger.info(f"Connected by {addr}")

            self.create_thread_conn(conn, addr, self.handle)

    def create_thread_conn(self, conn, addr, handle):
        thread = threading.Thread(target=handle, args=(conn, addr))
        thread.daemon = True
        thread.start()

    def handle(self, conn, addr):
        with conn:
            while 1:
                response = read_json_response(conn)
                if response:
                    if "connect" in response:
                        player = match.add_player(1000, 10)
                        sendall_json(conn, {
                            "player_id": str(player.id),
                            "match_id": str(match.match_id),
                            "is_host": player.is_host
                            })
                        logger.info(f"player connected with id {player.id}")
                    elif "is_playable" in response:
                        sendall_json(conn, {"is_playable": match.is_playable})
                    else:
                        player_id, player_pos = response["player_id"], response["player_pos"]
                        match.update_player(player_id, player_pos)
                        if player_id == match.player1.id:
                            match.update_ball(*response["ball_pos"])
                            match.update_score(*response["score"])

                        response = match.get_response(player_id)
                        sendall_json(conn, response)
