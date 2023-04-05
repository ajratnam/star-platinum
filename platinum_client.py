from config import *
from utils import SocketBox

client = SocketBox(HOST, PORT, DEBUG)
client.connect()
