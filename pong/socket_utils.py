import json
import socket

def read_json_response(socket):
    response = socket.recv(1024)
    #print(f"socket {socket} recebeu", response)

    if response:
        response = response.decode("utf-8")
        response = json.loads(response)

    return response


def sendall_json(socket, dict_):
    #print(f"socket {socket} enviou", dict_)
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