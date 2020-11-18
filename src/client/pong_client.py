import socket

from src.settings import HOST, PORT

class Client:
    def __init__(self):
        pass

    @staticmethod
    def connect(ip, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(b'Hello, world')
            data = s.recv(1024)
