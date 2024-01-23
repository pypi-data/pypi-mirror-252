# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: 2023 Wojtek Porczyk <woju@hackerspace.pl>

from tuxgo import (
    ast,
    blocks,
    engine,
    parser,
)

class Engine(engine.ExecEngine):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.steps = 0
        self.turns = 0
        self.jumps = 0

    def step(self, counter: int):
        self.steps += counter

    def turn_left(self):
        self.turns += 1

    def turn_right(self):
        self.turns -= 1

    def jump(self):
        self.jumps += 1

    def pick_up(self):
        pass

    def place(self, direction: ast.Direction):
        pass

    def activate(self):
        pass

    def draw(self):
        pass

    def detect(self, direction: ast.Direction, obj: ast.Object):
        if direction == ast.Direction.IN_FRONT:
            if obj == ast.Object.OBSTACLE:
                return self.steps >= 10
            else:
                return self.steps < 10
        if direction == ast.Direction.HERE:
            return obj != ast.Object.EMPTY
        raise NotImplementedError()

def test_step():
    programme = parser.parse([
        (blocks.Token.BEGIN,),
            (blocks.Token.STEP, blocks.Token.DIGIT_6),
            (blocks.Token.STEP, blocks.Token.DIGIT_9),
        (blocks.Token.END,),
    ])

    engine = Engine()
    programme.execute(engine)
    assert engine.steps == 15

def test_turns():
    programme = parser.parse([
        (blocks.Token.BEGIN,),
            (blocks.Token.TURN_LEFT,),
            (blocks.Token.TURN_LEFT,),
            (blocks.Token.TURN_RIGHT,),
        (blocks.Token.END,),
    ])

    engine = Engine()
    programme.execute(engine)
    assert engine.turns == 1

def test_if():
    programme = parser.parse([
        (blocks.Token.BEGIN,),
            (blocks.Token.IF, blocks.Token.HERE, blocks.Token.EMPTY),
                (blocks.Token.TURN_LEFT,),
            (blocks.Token.ELSE,),
                (blocks.Token.TURN_RIGHT,),
            (blocks.Token.END_BLOCK,),
        (blocks.Token.END,),
    ])

    engine = Engine()
    programme.execute(engine)
    assert engine.turns == -1

def test_repeat():
    programme = parser.parse([
        (blocks.Token.BEGIN,),
            (blocks.Token.REPEAT, blocks.Token.DIGIT_4, blocks.Token.DIGIT_2),
                (blocks.Token.TURN_LEFT,),
            (blocks.Token.END_BLOCK,),
        (blocks.Token.END,),
    ])

    engine = Engine()
    programme.execute(engine)
    assert engine.turns == 42

def test_repeat_forever():
    programme = parser.parse([
        (blocks.Token.BEGIN,),
            (blocks.Token.REPEAT, blocks.Token.FOREVER),
                (blocks.Token.STEP, blocks.Token.DIGIT_1),
                (blocks.Token.IF, blocks.Token.IN_FRONT, blocks.Token.OBSTACLE),
                    (blocks.Token.BREAK,),
                (blocks.Token.END_BLOCK,),
            (blocks.Token.END_BLOCK,),
        (blocks.Token.END,),
    ])

    engine = Engine()
    programme.execute(engine)
    assert engine.steps == 10

def test_repeat_while():
    programme = parser.parse([
        (blocks.Token.BEGIN,),
            (blocks.Token.REPEAT_WHILE, blocks.Token.IN_FRONT, blocks.Token.EMPTY),
                (blocks.Token.STEP, blocks.Token.DIGIT_1),
            (blocks.Token.END_BLOCK,),
        (blocks.Token.END,),
    ])

    engine = Engine()
    programme.execute(engine)
    assert engine.steps == 10

# vim: tw=80 ts=4 sts=4 sw=4 et
