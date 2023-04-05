import pickle
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
        self.handler = lambda: None
        self.con_list = {}

    def serve(self):
        self.is_serving = True
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)

        try:
            while self.is_serving:
                connection, address = self.socket.accept()
                self.con_list[address] = connection
                Thread(target=self.handler, args=(connection, address)).start()
        finally:
            self.socket.close()

    def connect(self):
        self.socket.connect((self.host, self.port))
        Thread(target=self.handler, args=()).start()

    def send_message(self, connection, message):
        print(message)
        message = pickle.dumps(message)
        connection.send(message)

    def recv_message(self, connection):
        message = connection.recv(self.chunk_size)
        return pickle.loads(message)

    def forward(self, message, source):
        for address, connection in self.con_list.items():
            if address != source:
                self.send_message(connection, message)

    def set_handler(self, handler):
        self.handler = handler
