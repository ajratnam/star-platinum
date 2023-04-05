from config import *
from game import app, Voxel, player, Player
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
                addr, pdata = data.values()
                pos, rot = pdata.values()
                if addr not in pos_li:
                    pos_li[addr] = Player(addr)
                pos_li[addr].change_pos(pos)
                pos_li[addr].change_rot(rot)

        client.send_message(client.socket, {'op': 3, 'd': {'pos': player.position, 'rot': player.rotation}})


client.connect()
app.run()
