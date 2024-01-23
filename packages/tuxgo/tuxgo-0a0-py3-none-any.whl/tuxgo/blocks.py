# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: 2023 Wojtek Porczyk <woju@hackerspace.pl>

import dataclasses
import enum
import tomllib
import typing

from dataclasses import dataclass
from typing import (
    Optional,
)

from . import (
    assets,
    ast,
)


class TokenType(str, enum.Enum):
    BEGIN = enum.auto()
    END = enum.auto()

    SIMPLE_STMT = enum.auto()
    DIR_STMT = enum.auto()
    EXPR_STMT = enum.auto()

    DIGIT = enum.auto()
    DIRECTION = enum.auto()
    OP = enum.auto()

    FUNCNAME = enum.auto()
    VARNAME = enum.auto()
    OBJECT = enum.auto()

    NEWLINE = enum.auto()

    def __repr__(self):
        return f'{type(self).__name__}.{self.name}'


@dataclass(frozen=True)
class TokenDataMixIn:
    text: str
    type: Optional[TokenType] = dataclasses.field(default=None)

class Token(TokenDataMixIn, enum.Enum):
    BEGIN =             'START', TokenType.BEGIN
    END =               'KONIEC', TokenType.END

    TURN_LEFT =         'OBRÓT W LEWO', TokenType.SIMPLE_STMT
    TURN_RIGHT =        'OBRÓT W PRAWO', TokenType.SIMPLE_STMT
    JUMP =              'SKOCZ', TokenType.SIMPLE_STMT
    PICK_UP =           'PODNIEŚ', TokenType.SIMPLE_STMT
    ACTIVATE =          'UŻYJ', TokenType.SIMPLE_STMT
    DRAW =              'RYSUJ', TokenType.SIMPLE_STMT

    STEP =              'KROK', TokenType.EXPR_STMT
    PLACE =             'UMIEŚĆ', TokenType.DIR_STMT
    VARIABLE =          'ZMIENNA',

    REPEAT =            'POWTÓRZ',
    REPEAT_WHILE =      'POWTÓRZ DOPÓKI',
    BREAK =             'PRZERWIJ',
    IF =                'JEŻELI',
    ELSE_IF =           'W PRZECIWNYM RAZIE JEŻELI',
    ELSE =              'W PRZECIWNYM RAZIE',
    END_BLOCK =         'KONIEC PĘTLI LUB WARUNKU',

    FOREVER =           'CIĄGLE',

    HERE =              ast.Direction.HERE.value, TokenType.DIRECTION
    IN_FRONT =          ast.Direction.IN_FRONT.value, TokenType.DIRECTION
    ON_THE_LEFT =       ast.Direction.ON_THE_LEFT.value, TokenType.DIRECTION
    ON_THE_RIGHT =      ast.Direction.ON_THE_RIGHT.value, TokenType.DIRECTION
    BEHIND =            ast.Direction.BEHIND.value, TokenType.DIRECTION

    X =                 'X', TokenType.VARNAME
    Y =                 'Y', TokenType.VARNAME
    EQUALS =            '=',
    PLUS =              '+', TokenType.OP
    MINUS =             '-', TokenType.OP

    SWITCH_TO_HERO =    'STERUJ (SCOTTIE)', TokenType.SIMPLE_STMT
    SWITCH_TO_RED =     'STERUJ (CZERWONY BÓBR)', TokenType.SIMPLE_STMT
    SWITCH_TO_BLUE =    'STERUJ (NIEBIESKI BÓBR)', TokenType.SIMPLE_STMT
    SWITCH_TO_YELLOW =  'STERUJ (ŻÓŁTY BÓBR)', TokenType.SIMPLE_STMT

    CALL_FUNCTION =     'WYWOŁAJ FUNKCJĘ',
    DEFINE_FUNCTION =   'DEFINIUJ FUNKCJĘ', TokenType.BEGIN
    END_FUNCTION =      'KONIEC FUNKCJI', TokenType.END
    BREAK_FUNCTION =    'PRZERWIJ FUNKCJĘ',
    A =                 'A', TokenType.FUNCNAME
    B =                 'B', TokenType.FUNCNAME
    C =                 'C', TokenType.FUNCNAME

    OBSTACLE =          ast.Object.OBSTACLE.value, TokenType.OBJECT
    ELEVATED =          ast.Object.ELEVATED.value, TokenType.OBJECT
    MARK_1 =            ast.Object.MARK_1.value, TokenType.OBJECT
    MARK_2 =            ast.Object.MARK_2.value, TokenType.OBJECT
    COLLECTABLE =       ast.Object.COLLECTABLE.value, TokenType.OBJECT
    ACTION =            ast.Object.ACTION.value, TokenType.OBJECT
    EMPTY =             ast.Object.EMPTY.value, TokenType.OBJECT

    DIGIT_0 =           '0', TokenType.DIGIT
    DIGIT_1 =           '1', TokenType.DIGIT
    DIGIT_2 =           '2', TokenType.DIGIT
    DIGIT_3 =           '3', TokenType.DIGIT
    DIGIT_4 =           '4', TokenType.DIGIT
    DIGIT_5 =           '5', TokenType.DIGIT
    DIGIT_6 =           '6', TokenType.DIGIT
    DIGIT_7 =           '7', TokenType.DIGIT
    DIGIT_8 =           '8', TokenType.DIGIT
    DIGIT_9 =           '9', TokenType.DIGIT

    NEWLINE =           None, TokenType.NEWLINE

    def __repr__(self):
        return f'{type(self).__name__}.{self.name}'

class Block(typing.NamedTuple):
    aruco_id: int
    id: int
    token: int

    def __str__(self):
        return f'{self.id:03d} {self.token}' if self.id is not None else f'--- {self.token}'


class BlockLoader:
    def __init__(self, path=assets / 'blocks.toml'):
        self._by_id = {}
        self._by_aruco_id = {}
        with open(path, 'rb') as file:
            data = tomllib.load(file)

        for tile in data['block']:
            tile.setdefault('id', None)
            tile['token'] = Token[tile['token']]
            tile = Block(**tile)
            self._by_aruco_id[tile.aruco_id] = tile
            if tile.id is not None:
                self._by_id[tile.id] = tile

    def get_block_by_aruco_id(self, key):
        return self._by_aruco_id[key]

    def get_block_by_id(self, key):
        return self._by_id[key]

# vim: tw=80 ts=4 sts=4 sw=4 et
