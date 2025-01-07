import socket
import threading

class Server:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.nickname_mapping = {}

    def start_server(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server started on {self.host}:{self.port}")

        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connected to {client_address}")

            client_handler = threading.Thread(
                target=self.handle_client,
                args=(client_socket, client_address)
            )
            client_handler.start()

    def handle_client(self, client_socket, client_address):
        nickname = client_socket.recv(1024).decode()
        self.nickname_mapping[client_socket] = nickname
        self.clients.append(client_socket)
        print(f"Client {nickname} connected")

        while True:
            try:
                message = client_socket.recv(1024).decode()
                if not message:
                    break
                print(f"Received from {nickname}: {message}")
                response = input("Server response: ")
                client_socket.sendall(response.encode())
            except Exception as e:
                print(f"Error: {e}")
                break
        self.clients.remove(client_socket)
        del self.nickname_mapping[client_socket]
        client_socket.close()
        print(f"Client {nickname} disconnected")

if __name__ == "__main__":
    server = Server()
    server.start_server()