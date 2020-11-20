import sys
from pong.server.pong_server import Server
from pong.client.pong_client import Client

if __name__ == "__main__":
    args = sys.argv

    if args[1] == 'start-server':
        server = Server()
        server.start() 

    if args[1] == "test-client":
        client = Client()
        client.connect_server()
        client.send_position((10, 10), (10, 20))