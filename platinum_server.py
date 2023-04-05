from config import *
from utils import SocketBox

server = SocketBox(HOST, PORT, DEBUG)
blocks = {(x, 0, z) for z in range(8) for x in range(8)}


@server.set_handler
def handle_client(connection, address):
    server.send_message(connection, {'op': 0, 'd': blocks})
    try:
        while message := server.recv_message(connection):
            opcode, data = message.values()
            match opcode:
                case 1:
                    blocks.add(data)
                case 2:
                    blocks.remove(data)
                case 3:
                    message['d'] = {'addr': address, 'pos': message['d']}
            server.forward(message, address)
    except ConnectionResetError:
        pass
    finally:
        del server.con_list[address]


server.serve()
