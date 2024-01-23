# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: 2023 Wojtek Porczyk <woju@hackerspace.pl>

import abc
import dataclasses
import enum

from abc import abstractmethod
from dataclasses import dataclass
from typing import (
    Callable,
    List,
    Optional,
    Tuple,
    Union,
)

class Direction(enum.Enum):
    HERE =          'TUTAJ'
    IN_FRONT =      'Z PRZODU'
    ON_THE_LEFT =   'Z LEWEJ'
    ON_THE_RIGHT =  'Z PRAWEJ'
    BEHIND =        'Z TYŁU'

    def __repr__(self):
        return f'{type(self).__name__}.{self.name}'

class Object(enum.Enum):
    OBSTACLE =      'PRZESZKODA'
    ELEVATED =      'WZNIESIENIE'
    MARK_1 =        'KOPERTA: KWADRAT'
    MARK_2 =        'KOPERTA: KRZYŻYK'
    COLLECTABLE =   'PRZEDMIOT DO ZEBRANIA'
    ACTION =        'POLE AKCJI'
    EMPTY =         'PUSTE POLE'

    def __repr__(self):
        return f'{type(self).__name__}.{self.name}'

@dataclass(frozen=True)
class Parsed(metaclass=abc.ABCMeta):
    line: int = dataclasses.field(repr=False)
    cols: Tuple[int, int] = dataclasses.field(repr=False)

class Expression(Parsed):
    @abstractmethod
    def eval(self, engine) -> int:
        raise NotImplementedError()

class Forever(Parsed):
    pass

@dataclass(frozen=True)
class Number(Expression):
    value: int

    def eval(self, engine):
        return engine.eval_Number(self)

@dataclass(frozen=True)
class Variable(Expression):
    name: str

    def eval(self, engine):
        return engine.eval_Variable(self)

@dataclass(frozen=True)
class BinOp(Expression):
    op: Callable[[int, int], int]
    left: Expression
    right: Expression

    def eval(self, engine):
        return engine.eval_BinOp(self)

@dataclass(frozen=True)
class Condition(Parsed):
    direction: Direction
    object: Object

    def eval(self, engine):
        return engine.eval_Condition(self)

@dataclass(frozen=True)
class Statement(Parsed):
    #: Range of lines. For simple statement this is (self.line, self.line).
    lines: Tuple[int, int] = dataclasses.field(init=False, repr=False)
    def __post_init__(self):
        # in case a child class overrode this attribute, we don't overwrite
        try:
            self.lines
        except AttributeError:
            # we're dataclass(frozen=True), so we need to resort to tricks
            object.__setattr__(self, 'lines', (self.line, self.line))
        
    @abstractmethod
    def execute(self, engine: 'BaseEngine'):
        raise NotImplementedError()

class TurnLeft(Statement):
    def execute(self, engine):
        return engine.execute_TurnLeft(self)

class TurnRight(Statement):
    def execute(self, engine):
        return engine.execute_TurnRight(self)

class Jump(Statement):
    def execute(self, engine):
        return engine.execute_Jump(self)

class PickUp(Statement):
    def execute(self, engine):
        return engine.execute_PickUp(self)

class Activate(Statement):
    def execute(self, engine):
        return engine.execute_Activate(self)

@dataclass(frozen=True)
class Draw(Statement):
    def execute(self, engine):
        return engine.execute_Draw(self)

@dataclass(frozen=True)
class Step(Statement):
    counter: Expression

    def execute(self, engine):
        return engine.execute_Step(self)

@dataclass(frozen=True)
class Place(Statement):
    direction: Direction

    def execute(self, engine):
        return engine.execute_Place(self)

@dataclass(frozen=True)
class Assign(Statement):
    name: str
    expression: Expression

    def execute(self, engine):
        return engine.execute_Assign(self)

@dataclass(frozen=True)
class CallFunction(Statement):
    name: str

    def execute(self, engine):
        return engine.execute_CallFunction(self)

@dataclass(frozen=True)
class Break(Statement):
    def execute(self, engine):
        return engine.execute_Break(self)

@dataclass(frozen=True)
class BreakFunction(Statement):
    def execute(self, engine):
        return engine.execute_BreakFunction(self)

@dataclass(frozen=True)
class Block(Statement):
    lines: Tuple[int, int] = dataclasses.field(repr=False)
    body: List[Statement]
    body_lines: Tuple[int, int] = dataclasses.field(init=False, repr=False)

    def __post_init__(self):
        try:
            self.body_lines
        except AttributeError:
            object.__setattr__(self, 'body_lines', (
                min(stmt.lines[0] for stmt in self.body),
                max(stmt.lines[1] for stmt in self.body),
            ))

@dataclass(frozen=True)
class Repeat(Block):
    counter: Union[Expression, Forever]

    def execute(self, engine):
    	return engine.execute_Repeat(self)

@dataclass(frozen=True)
class ConditionStatement(Block):
    condition: Condition

@dataclass(frozen=True)
class RepeatWhile(ConditionStatement):
    def execute(self, engine):
        return engine.execute_RepeatWhile(self)

class Else(Block):
    def execute(self, engine):
        return engine.execute_Else(self)

@dataclass(frozen=True)
class If(ConditionStatement):
    orelse: Union['If', Else]
    def execute(self, engine):
        return engine.execute_If(self)

@dataclass(frozen=True)
class Programme(Block):
    def execute(self, engine):
        return engine.execute_Programme(self)

@dataclass(frozen=True)
class Function(Block):
    name: str
    def execute(self, engine):
        return engine.execute_Function(self)

# vim: tw=80 ts=4 sts=4 sw=4 et
