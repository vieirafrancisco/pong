import json
import socket

def read_json_response(socket):
    response = socket.recv(1024)

    if response:
        response = response.decode("utf-8")
        response = json.loads(response)

    return response


def sendall_json(socket, dict_):
    socket.sendall(bytes(json.dumps(dict_), encoding="utf-8"))

class CustomSocket:
    def __init__(self, *args, **kwargs):
        self._socket = socket.socket(*args, **kwargs)
    
    def __enter__(self):
        return self._socket

    def __exit__(self, *args):
        self._socket.close()

    def read_json(self):
        response = self._socket.recv(1024)

        if response:
            response = response.decode("utf-8")
            response = json.loads(response)

        return response

    def sendall_json(self, dict_):
        self._socket.sendall(bytes(json.dumps(dict_), encoding="utf-8"))

    def send_read_json(self, dict_):
        self.sendall_json(dict_)
        return self.read_json()

    def connect(self, addr, *args, **kwargs):
        self._socket.connect(addr, *args, **kwargs)

    def sendall(self, bytes):
        return self._socket.sendall(bytes)

    def recv(self, size):
        return self._socket.recv(size)

    def bind(self, addr, *args, **kwargs):
        return self._socket.bind(addr, *args, **kwargs)

    def listen(self, code=None):
        if code is None:
            return self._socket.listen()
        else:
            return self._socket.listen(code)

    def accept(self):
        conn, addr = self._socket.accept()

        return conn, addr