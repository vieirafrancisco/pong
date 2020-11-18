from socketserver import TCPServer, BaseRequestHandler
from pong.settings import HOST, PORT

class PongRequestHandler(BaseRequestHandler):
    def handle(self):
        pass

class PongServer(TCPServer):
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.games = []

    

    def start():
        pass


