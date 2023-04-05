import socket
from threading import Thread


class SocketBox:
    def __init__(self, host, port, debug=False):
        self.host = host
        self.port = port
        self.socket = socket.socket()

        self.is_serving = False
        self.debug = debug
        self.chunk_size = 1024

    def serve(self):
        self.is_serving = True
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        if self.debug:
            print('Server is up and waiting for connections')

        try:
            while self.is_serving:
                connection, address = self.socket.accept()
                if self.debug:
                    print('Connected to', *address)
                Thread(target=self.handle_client, args=(connection, address)).start()
        finally:
            self.socket.close()
            if self.debug:
                print('Server is closing')

    def connect(self):
        if self.debug:
            print('Trying to connect to server')
        self.socket.connect((self.host, self.port))
        if self.debug:
            print('Connected to server!!')
        self.handle_server()

    def send_message(self, connection, message):
        if isinstance(message, str):
            message = message.encode()
        connection.send(message)
        if self.debug:
            print(f'Sent message "{message}"')

    def recv_message(self, connection):
        message = connection.recv(self.chunk_size).decode()
        if self.debug:
            print(f'Received message "{message}"')
        return message

    def handle_client(self, connection, address):
        while data := self.recv_message(connection):
            self.send_message(connection, data[::-1])
        connection.close()
        if self.debug:
            print('Lost connection with', address)

    def handle_server(self):
        while True:
            message = input("\nEnter the message - ")
            self.send_message(self.socket, message)
            data = self.recv_message(self.socket)
            if data == "bye":
                break
        self.socket.close()
        if self.debug:
            print('Closing connection with server')
