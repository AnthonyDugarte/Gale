import os
from pathlib import Path

import click


def touch(path: Path, text: str = None):
    with open(path, 'w') as f:
        if text is not None:
            f.write(text)


@click.group
def cli():
    pass


GAME_CLASS_TEMPLATE = '''
"""
This module was autogenerated by gale.
"""
import pygame

from gale.game import Game
from gale.state_machine import StateMachine


class {game_name}(Game):
    def init(self) -> None:
        self.state_machine = StateMachine()

    def update(self, dt: float) -> None:
        self.state_machine.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        self.state_machine.render(surface)

'''

GAME_MAIN_TEMPLATE = '''
"""
This module was autogenerated by gale.
"""
import settings
from src.{game_class} import {game_class}

if __name__ == '__main__':
    game = {game_class}(
        "{game_class}",
        settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT,
        settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT
    )
    game.exec()

'''

SETTINGS_TEMPLATE = '''
"""
This module was autogenerated by gale.
"""
import pathlib

import pygame

from gale import frames
from gale import input_handler

input_handler.InputHandler.set_keyboard_action(input_handler.KEY_SCAPE, 'quit')

# Size we want to emulate
VIRTUAL_WIDTH = 320
VIRTUAL_HEIGHT = 180

# Size of our actual window
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

BASE_DIR = pathlib.Path(__file__).parent

# Register your textures from the graphics folder, for instance:
# TEXTURES = {
#     'my_texture': pygame.image.load(BASE_DIR / 'graphics/my_texture.png')
# }
TEXTURES = {}

# Register your frames, for instance:
# FRAMES = {
#     'my_frames': frames.generate_frames(TEXTURES['my_texture'], 16, 16)
# }
FRAMES = {}

pygame.mixer.init()

# Register your sound from the sounds folder, for instance:
# SOUNDS = {
#     'my_sound': pygame.mixer.Sound(BASE_DIR / 'sounds/my_sound.wav'),
# }
SOUNDS = {}

pygame.font.init()

# Register your fonts from the fonts folder, for instance:
# SOUNDS = {
#     'small': pygame.font.Font(BASE_DIR / 'fonts/font.ttf', 8)
# }
FONTS = {}

'''


@click.command
@click.argument('name')
def create_project(name: str) -> None:
    if os.path.exists(name):
        click.echo(f"Project {name} already exists.")
        return

    os.mkdir(name)
    app_path = os.path.join(os.getcwd(), name)

    game_class = name.capitalize()

    touch(
        os.path.join(app_path, 'main.py'),
        GAME_MAIN_TEMPLATE.format(game_class=game_class)
    )
    touch(os.path.join(app_path, 'settings.py'), SETTINGS_TEMPLATE)

    for directory in ['src', 'sounds', 'graphics', 'fonts']:
        os.mkdir(os.path.join(app_path, directory))

    click.echo('Project {} created'.format(name))


cli.add_command(create_project)

if __name__ == '__main__':
    cli()