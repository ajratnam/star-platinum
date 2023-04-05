from config import *
from utils import SocketBox

server = SocketBox(HOST, PORT, DEBUG)
server.serve()
