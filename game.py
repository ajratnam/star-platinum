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
    def __init__(self, name):
        super().__init__(
            parent=scene,
            model='cube',
            texture='white_cube',
            color=color.random_color()
        )

        self.texts = [Text(
            name,
            parent=scene,
            scale=10,
            color=color.black,
            origin=(0, 0)
        ) for _ in range(2)]

    def change_pos(self, pos):
        self.position = (pos[0], pos[1] + 0.5, pos[2])
        self.texts[0].position = (pos[0], pos[1] + 1.4, pos[2])
        self.texts[1].position = (pos[0], pos[1] + 1.4, pos[2])

    def change_rot(self, rot):
        self.rotation = rot
        self.texts[0].rotation = self.texts[1].rotation = rot
        self.texts[1].rotation_y = self.texts[0].rotation_y + 180


player = FirstPersonController()
