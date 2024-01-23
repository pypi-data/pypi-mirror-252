# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: 2023 Wojtek Porczyk <woju@hackerspace.pl>

import asyncio
import enum
import io
import math
import pathlib
import sys

import click
import cv2
import numpy as np
import pygame
import matplotlib.path
import matplotlib.transforms

from . import (
    assets,
    ast,
    blocks,
    detector,
    engine,
    http_server,
    parser,
)

def load_svg(path, size):
    # Robot assets have width="100%" height="100%" attributes on svg, and pygame
    # loads them as 1x1x32 surfaces, which is useless. This is adapted
    # https://stackoverflow.com/a/69509545.
    path = pathlib.Path(path)
    width, height = size
    with open(path, 'rb') as file:
        data = file.read()
    i = data.index(b'">') + 1 # this will find the end of <svg> opening tag

    buffer = io.BytesIO()
    buffer.write(data[:i])
    buffer.write(f' width="{width}" height="{height}"'.encode('ascii'))
    buffer.write(data[i:])
    buffer.seek(0)

    return pygame.image.load(buffer, path.name)

TILE_WIDTH = 128

class LevelField(enum.Enum):
    ABYSS = ' '
    FLOOR = '.' # aka EMPTY
    WALL = '#'
    ELEVATED = ':'
    WATER = '~'
    LIGHT_OFF = '?'
    LIGHT_ON = '!'

_TILESET = {
#   LevelField.FLOOR:
#       load_svg(assets / 'tileset/401.svg', (TILE_WIDTH, TILE_WIDTH * 3//4)),
    LevelField.FLOOR:
        load_svg(assets / 'tileset/001.svg', (TILE_WIDTH, TILE_WIDTH * 3//4)),
    LevelField.WALL:
        load_svg(assets / 'tileset/472.svg', (TILE_WIDTH, TILE_WIDTH * 11//4)),
    LevelField.ELEVATED:
        load_svg(assets / 'tileset/477.svg', (TILE_WIDTH, TILE_WIDTH * 11//4)),
    LevelField.LIGHT_OFF:
        load_svg(assets / 'tileset/051.svg', (TILE_WIDTH, TILE_WIDTH * 11//4)),
    LevelField.LIGHT_ON:
        load_svg(assets / 'tileset/052.svg', (TILE_WIDTH, TILE_WIDTH * 11//4)),
}


# 37c3 colours
BLACK =     (  0,   0,   0) #000000
WHITE =     (255, 255, 255) #ffffff
GREY1 =     (217, 217, 217) #d9d9d9
GREY2 =     (170, 170, 170) #aaaaaa
GREY3 =     (122, 122, 122) #7a7a7a
GREY4 =     ( 32,  32,  32) #202020
BLUE =      ( 45,  66, 255) #2d42ff
BLUE2 =     ( 11,  21, 117) #0b1575
RED =       (222,  64,  64) #de4040
RED2 =      ( 86,  16,  16) #561010
GREEN =     (121, 255,  94) #79ff5e
GREEN2 =    ( 43, 141,  24) #2b8d18
CYAN =      ( 41, 255, 255) #29ffff
CYAN2 =     (  0, 107, 107) #006b6b
MAGENTA =   (222,  55, 255) #de37ff
MAGENTA2 =  (102,   0, 122) #66007a
YELLOW =    (246, 246, 117) #f6f675
YELLOW2 =   (117, 177,   1) #757501


class Level:
    def __init__(self, tiles):
        self.tiles = tiles

        # diagonal or "major" diagonal is from 0,0 to +inf,+inf 
        # minor diagonal is from 0,+inf to +inf,0
        self.min_major_diag = self.min_minor_diag = float('+inf')
        self.max_major_diag = self.max_minor_diag = float('-inf')

        for y in range(len(tiles)):
            for x in range(len(tiles[y])):
                if self.tiles[y][x] == LevelField.ABYSS:
                    continue
                major_diag, minor_diag = x + y, y - x
                self.min_major_diag = min(self.min_major_diag, major_diag)
                self.max_major_diag = max(self.max_major_diag, major_diag)
                self.min_minor_diag = min(self.min_minor_diag, minor_diag)
                self.max_minor_diag = max(self.max_minor_diag, minor_diag)

        assert not any(math.isinf(i) for i in (
            self.min_major_diag,
            self.max_major_diag,
            self.min_minor_diag,
            self.max_minor_diag,
        ))

    @classmethod
    def from_file(cls, file):
        tiles = []
        hero = None
        for y, line in enumerate(file):
            line = line.rstrip('\n')
            if not line:
                break
            tileline = []
            for x, c in enumerate(line):
                if c == '@':
                    if hero is not None:
                        raise ValueError('more than one hero')
                    hero = (x, y)
                    c = '.'
                tileline.append(LevelField(c))
            tiles.append(tileline)
        return cls(tiles), hero


class Button:
    def __init__(self, surface, font, x, y, width, height, text):
        self.surface = surface
        self.font = font
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self):
        radius = self.height / 2
        pygame.draw.circle(self.surface, WHITE, (self.x + radius, self.y + radius), radius)
        pygame.draw.rect(self.surface, WHITE, pygame.Rect((self.x + radius, self.y), (self.width - radius, self.height)))
        font_surf = self.font.render(self.text, True, (0, 0, 0), WHITE)
        self.surface.blit(font_surf, (self.x + radius * 0.7, self.y + (self.height - font_surf.get_height()) / 2))

class ButtonSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text, font):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

        radius = height / 2
        pygame.draw.circle(self.image, WHITE, (radius, radius), radius)
        pygame.draw.rect(self.image, WHITE, pygame.Rect((radius, 0), (width - radius, height)))
        text_surf = font.render(text, True, (0, 0, 0), WHITE)
        self.image.blit(text_surf, (radius * 0.7, (height - text_surf.get_height()) / 2))

class ButtonBar(pygame.sprite.AbstractGroup):
    width = 300
    height = 100

    def __init__(self, screen, n=7):
        super().__init__()
        self._buttons = [None for i in range(n)]

        screen_rect = screen.get_rect()
        self.x = screen_rect.width - self.width
        self.padding = (screen_rect.height - n * self.height) / (n + 1)
        self.font = pygame.font.Font(assets / 'fonts/Rajdhani-Bold.otf', 60)

    def __getitem__(self, key):
        return self._buttons[key]

    def set_button(self, index, text, _callback):
        if self._buttons[index] is not None:
            self._buttons[index].kill()
        self.add(ButtonSprite(self.x, self.y(index), self.width, self.height, text, self.font), index=index)

    def remove_button(self, i):
        self._buttons[i].sprite.kill()

    def y(self, index):
        index %= len(self._buttons) # can be negative!
        return self.padding * (index + 1) + self.height * index

    def add(self, sprite, *, index):
        if self._buttons[index] is not None:
            self.remove(self._buttons[index])
        super().add(sprite)
        self._buttons[index] = sprite

    def remove_internal(self, sprite):
        self._buttons[self._buttons.index(sprite)] = None
        super().remove_internal(self, sprite)

class Tile(pygame.sprite.Sprite):
    def __init__(self, *args, image, midbottom, **kwds):
        super().__init__(*args, **kwds)
        self.image = image
        self.rect = image.get_rect()
        self.rect.midbottom = midbottom

class Robot(pygame.sprite.Sprite):
    def __init__(self, *args, transform_level, images, pos, rotation, **kwds):
        super().__init__(*args, **kwds)
        self.images = images
        self.transform = matplotlib.transforms.CompositeAffine2D(
            transform_level,
            matplotlib.transforms.Affine2D().translate(0, -36)
        )
        self._rotation = None
        self.set_rotation(rotation)
        self.rect = self.image.get_rect()
        self._pos = None
        self.move(pos)

    @property
    def pos(self):
        return self._pos

    def move(self, pos):
        self._pos = tuple(pos)
        self.rect.midbottom = self.transform.transform(self._pos)

        layer = pos_to_layer(*pos)
        for group in self.groups():
            try:
                change_layer = group.change_layer
            except AttributeError:
                pass
            else:
                change_layer(self, layer)

    @pos.setter
    def pos(self, pos):
        return self.move(pos)

    def set_rotation(self, rotation):
        self._rotation = rotation % len(self.images)
        self.image = self.images[self._rotation]

    def get_rotation(self):
        return self._rotation

    rotation = property(get_rotation, set_rotation)


def get_sprites_for_level(level, transform):
    group = pygame.sprite.LayeredUpdates()
    for y in range(len(level.tiles)):
        for x in range(len(level.tiles[y])):
            tile = level.tiles[y][x]
            if tile == LevelField.ABYSS:
                continue
            group.add(Tile(
                    image=_TILESET[level.tiles[y][x]],
                    midbottom=transform.transform((x, y))),
                layer=pos_to_layer(x, y))
    return group


# there's a stack of three transforms:
# 1. transform_isometric: base transform that skews in game (integral)
#    coordinates into isometric view
# 2. transform_level: translates the level into the centre of the screen; this
#    transform is applied to all the sprites
# 3. transform_robot: adds offset to the robot sprite (which is a bit special)
#    in relation to the board

# (0,0) is to the top
TRANSFORM_ISOMETRIC_ORIGIN_TOP = matplotlib.transforms.Affine2D.from_values(
     64, 32,
    -64, 32,
    0, 0,
)

# (0,0) is to the left
TRANSFORM_ISOMETRIC_ORIGIN_LEFT = matplotlib.transforms.Affine2D.from_values(
    64, -32,
    64,  32,
    0, 0,
)

def pos_to_layer_origin_top(x, y):
    return y + x

def pos_to_layer_origin_left(x, y):
    return y - x

pos_to_layer = pos_to_layer_origin_left

def get_level_transform_for_surface_origin_top(surface, level):
    half = surface.get_height() / 2
    tx = max(
        half + (level.min_minor_diag + level.max_minor_diag) / 2 * TILE_WIDTH / 2,
        (level.max_minor_diag + 1) * TILE_WIDTH / 2
    )
    ty = max(
        half - (level.min_major_diag + level.max_major_diag) / 2 * TILE_WIDTH / 4
            + TILE_WIDTH / 2,
        (-level.min_major_diag) * TILE_WIDTH / 2 + TILE_WIDTH * 3 / 4
    )

    return matplotlib.transforms.CompositeAffine2D(
        TRANSFORM_ISOMETRIC_ORIGIN_TOP,
        matplotlib.transforms.Affine2D().translate(tx, ty)
    )

def get_level_transform_for_surface_origin_left(surface, level):
    print(f'{level.min_major_diag=}')
    print(f'{level.max_major_diag=}')
    print(f'{level.min_minor_diag=}')
    print(f'{level.max_minor_diag=}')

    half = surface.get_height() / 2

    tx = max(
        half - (level.min_major_diag + level.max_major_diag) / 2 * TILE_WIDTH / 2,
        (level.min_major_diag + 1) * TILE_WIDTH / 2
    )
    ty = max(
        half - (level.min_minor_diag + level.max_minor_diag) / 2 * TILE_WIDTH / 4
            + TILE_WIDTH / 2,
        (level.min_minor_diag) * TILE_WIDTH / 2 + TILE_WIDTH * 3 / 4
    )

    return matplotlib.transforms.CompositeAffine2D(
        TRANSFORM_ISOMETRIC_ORIGIN_LEFT,
        matplotlib.transforms.Affine2D().translate(tx, ty)
    )

get_level_transform_for_surface = get_level_transform_for_surface_origin_left

class Game(engine.ExecEngine):
    def __init__(self, *args, screen, level, hero, hero_rotation, **kwds):
        self.screen = screen
        self.level = level
        self.transform_level = get_level_transform_for_surface(screen, level)
        self.robot = Robot(transform_level=self.transform_level, images=[
            load_svg(assets / 'robot/robot01.svg', (96, 96)),
            load_svg(assets / 'robot/robot02.svg', (96, 96)),
            load_svg(assets / 'robot/robot03.svg', (96, 96)),
            load_svg(assets / 'robot/robot04.svg', (96, 96)),
        ], pos=hero, rotation=hero_rotation)
        self.sprites = get_sprites_for_level(
            level, transform=self.transform_level)
        self.sprites.add(self.robot, layer=pos_to_layer(*self.robot.pos))
        self.running = False
        self.clock = pygame.time.Clock()

    def loop_once(self, tick=1, *, _really_once=True):
        self.process_events(once=_really_once)
        self.screen.fill((0, 0, 0))
        self.sprites.draw(self.screen)

        height = self.screen.get_height()
        half = height / 2
        pygame.draw.line(self.screen, (255, 0, 0),
            (0, half), (height, half))
        pygame.draw.line(self.screen, (255, 0, 0),
            (half, 0), (half, height))

        pygame.display.flip()
        if tick:
            self.clock.tick(tick)

    def loop(self):
        self.running = True

        while self.running:
            self.loop_once(tick=False)
            self.clock.tick(50)

    def process_events(self, once):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT
            or event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                if once:
                    sys.exit()
                else:
                    self.running = False


    def step(self, counter: int):
        pos = list(self.robot.pos)
        for i in range(abs(counter)):
            pos[self.robot.rotation % 2] += (int(math.copysign(1, counter))
                * ((-1) ** (self.robot.rotation // 2)))
            self.robot.pos = pos
            self.loop_once()

    def turn_left(self):
        self.robot.rotation -= 1
        self.loop_once()

    def turn_right(self):
        self.robot.rotation += 1
        self.loop_once()

    def jump(self):
        self.step(1)
#       self.loop_once()
#       raise NotImplementedError()

    def pick_up(self):
        raise NotImplementedError()

    def place(self, direction: ast.Direction):
        raise NotImplementedError()

    def activate(self):
        raise NotImplementedError()

    def draw(self):
        raise NotImplementedError()

    def detect(self, direction: ast.Direction, obj: ast.Object):
        raise NotImplementedError()

    def execute_Programme(self, programme):
        self.loop_once()
        super().execute_Programme(programme)
        self.loop()


w_przeręblu = [
    (blocks.Token.BEGIN,),
    (blocks.Token.REPEAT, blocks.Token.FOREVER),
        (blocks.Token.TURN_RIGHT,),
    (blocks.Token.END_BLOCK,),
    (blocks.Token.END,),
]

prog1_blocks = [
    (blocks.Token.BEGIN,),
    (blocks.Token.STEP, blocks.Token.DIGIT_1),
    (blocks.Token.TURN_RIGHT,),
    (blocks.Token.STEP, blocks.Token.DIGIT_1),
    (blocks.Token.TURN_LEFT,),
    (blocks.Token.STEP, blocks.Token.DIGIT_1),
    (blocks.Token.TURN_RIGHT,),
    (blocks.Token.STEP, blocks.Token.DIGIT_1),
    (blocks.Token.TURN_LEFT,),
    (blocks.Token.STEP, blocks.Token.DIGIT_1),
    (blocks.Token.TURN_RIGHT,),
    (blocks.Token.STEP, blocks.Token.DIGIT_1),
    (blocks.Token.TURN_LEFT,),
    (blocks.Token.END,),
]


def game_noninteractive():
    pygame.init()
    pygame.display.set_caption('tuxgo')
    screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)

    with open(assets / 'levels/level-woju') as file:
#   with open(assets / 'levels/level-mem-sy') as file:
#   with open(assets / 'levels/level-0-0') as file:
        level, hero = Level.from_file(file)
    if hero is None:
        hero = (0, 0)

    vm = Game(
        screen=screen,
        level=level,
        hero=hero,
        hero_rotation=0,
    )

    parser.parse(w_przeręblu).execute(vm)
#   parser.parse(prog1_blocks).execute(vm)

    pygame.quit()

def game_interactive():
    det = detector.Detector()

    pygame.init()
    pygame.display.set_caption('tuxgo')
    screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)

    with open(assets / 'levels/level-woju') as file:
#   with open(assets / 'levels/level-mem-sy') as file:
#   with open(assets / 'levels/level-0-0') as file:
        level, hero = Level.from_file(file)
    if hero is None:
        hero = (0, 0)

    vm = Game(
        screen=screen,
        level=level,
        hero=hero,
        hero_rotation=0,
    )

    vm.loop_once(tick=0)

    while True:
        image = http_server.get_image_from_http_server()
        image = np.asarray(bytearray(image), dtype=np.uint8)
        frame = cv2.imdecode(image, 0)
        analyser = detector.Analyser(det.detect_markers(frame))
        programme = parser.parse(analyser.get_programme())
        programme.execute(vm)

    pygame.quit()

def main():
    game_noninteractive()

if __name__ == '__main__':
    main()

# vim: tw=80 ts=4 sts=4 sw=4 et
