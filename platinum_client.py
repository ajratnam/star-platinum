from ursina import color

from config import *
from game import app, Voxel, player
from utils import SocketBox

client = SocketBox(HOST, PORT, DEBUG)
pos_li = {}


@client.set_handler
def game():
    while message := client.recv_message(client.socket):
        opcode, data = message.values()
        match opcode:
            case 0:
                for position in data:
                    Voxel(position)
            case 1:
                Voxel(data)
            case 2:
                Voxel.vx_li[data].delete()
            case 3:
                addr, pos = data.values()
                pos = (pos[0], pos[1] + 1, pos[2])
                if addr not in pos_li:
                    pos_li[addr] = Voxel(pos)
                    pos_li[addr].color = color.blue
                    pos_li[addr].highlight_color = color.blue
                else:
                    pos_li[addr].position = pos
        client.send_message(client.socket, {'op': 3, 'd': player.position})


client.connect()
app.run()
