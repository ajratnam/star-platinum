from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina(borderless=False, size=(800, 600))


class Voxel(Button):
    vx_li = {}

    def __init__(self, position=(0, 0, 0)):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=.5,
            texture='white_cube',
            color=color.color(0, 0, random.uniform(.9, 1.0)),
            highlight_color=color.lime,
        )

        self.vx_li[position] = self


class Player(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='cube',
            texture='white_cube',
            color=color.random_color()
        )

    def change_pos(self, pos):
        self.position = pos

    def change_rot(self, rot):
        self.rotation = rot


player = FirstPersonController()
