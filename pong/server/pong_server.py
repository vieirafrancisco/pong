import json
import socket
import logging
import threading
from pong.server.match import PongMatch
from pong.server.request_handler import handle_request
from pong.settings import HOST, PORT
from pong.socket_utils import CustomSocket, read_json_response

logger = logging.getLogger(__name__)
match = PongMatch()

class Server:
    def __init__(self, host=HOST, port=PORT):
        self.socket = CustomSocket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.matchs = ServerMatchs(self)

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
                body = read_json_response(conn)
                if body:
                    handle_request(self, conn, addr, body)

default_match = PongMatch()

class ServerMatchs:
    def __init__(self, server):
        self.server = server
        self.matchs = {}


    def get_match_by_id(self, match_id):
        return default_match


    def create_match(self, *args, **kwargs):
        match = PongMatch(*args, **kwargs)
        self.matchs[match.match_id] = match

        return match