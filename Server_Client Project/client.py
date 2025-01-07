import socket
import threading

class Client:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start_client(self):
        self.client_socket.connect((self.host, self.port))
        nickname = input("Enter nickname: ")
        self.client_socket.sendall(nickname.encode())
        print(f"Connected to {self.host}:{self.port}")

        receive_thread = threading.Thread(target=self.receive_message)
        receive_thread.start()

        while True:
            message = input("Client message: ")
            self.client_socket.sendall(message.encode())

    def receive_message(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                if not message:
                    break
                print(f"Server response: {message}")
            except Exception as e:
                print(f"Error: {e}")
                break
        self.client_socket.close()

if __name__ == "__main__":
    client = Client()
    client.start_client()