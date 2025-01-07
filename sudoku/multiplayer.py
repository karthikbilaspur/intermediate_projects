import socket

class MultiplayerGame:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port):
        self.socket.connect((host, port))

    def send_move(self, move):
        self.socket.sendall(move.encode())

    def receive_move(self):
        return self.socket.recv(1024).decode()