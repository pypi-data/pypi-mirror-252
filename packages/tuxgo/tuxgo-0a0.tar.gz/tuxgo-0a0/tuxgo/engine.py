# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: 2023 Wojtek Porczyk <woju@hackerspace.pl>

"""
Engine might be either a visitor or a virtual machine
"""

import abc
import asyncio
import dataclasses
import enum
import importlib.resources
import itertools
import operator
import sys
import types
import typing

from abc import abstractmethod
from dataclasses import dataclass
from typing import (
    Callable,
    List,
    Optional,
    Tuple,
)

from loguru import logger

from . import (
    ast,
    blocks,
    bluetooth,
)


class BaseEngine(metaclass=abc.ABCMeta):
    def __init__(self, functions=types.MappingProxyType({})):
        # pylint: disable=redefined-outer-name
        self.functions = {**functions}
        self.variables = {}

#       self.pc = None
#       self.block_markers = []
#       self.breakpoints = set()

    def exec_run(self):
        while not self.exec_step():
            pass

    def exec_step(self):
        return next(self.instructions)()

    #
    # The following methods need to be overloaded in the engine implementation:
    #

    @abstractmethod
    def eval_Number(self, number: ast.Number):
        raise NotImplementedError()

    @abstractmethod
    def eval_Variable(self, variable: ast.Variable):
        raise NotImplementedError()

    @abstractmethod
    def eval_BinOp(self, binop: ast.BinOp):
        raise NotImplementedError()

    @abstractmethod
    def eval_Condition(self, condition: ast.Condition):
        raise NotImplementedError()


    @abstractmethod
    def execute_Repeat(self, repeat: ast.Repeat):
        raise NotImplementedError()

    @abstractmethod
    def execute_RepeatWhile(self, repeat_while: ast.RepeatWhile):
        raise NotImplementedError()

    @abstractmethod
    def execute_Step(self, step: ast.Step):
        raise NotImplementedError()

    @abstractmethod
    def execute_TurnLeft(self, turn_left: ast.TurnLeft):
        raise NotImplementedError()

    @abstractmethod
    def execute_TurnRight(self, turn_right: ast.TurnRight):
        raise NotImplementedError()

    @abstractmethod
    def execute_Jump(self, jump: ast.Jump):
        raise NotImplementedError()

    @abstractmethod
    def execute_PickUp(self, pick_up: ast.PickUp):
        raise NotImplementedError()

    @abstractmethod
    def execute_Activate(self, activate: ast.Activate):
        raise NotImplementedError()

    @abstractmethod
    def execute_Draw(self, draw: ast.Draw):
        raise NotImplementedError()

    @abstractmethod
    def execute_Place(self, place: ast.Place):
        raise NotImplementedError()

    @abstractmethod
    def execute_CallFunction(self, call_function: ast.CallFunction):
        raise NotImplementedError()

    @abstractmethod
    def execute_If(self, if_: ast.If):
        raise NotImplementedError()

    @abstractmethod
    def execute_Else(self, else_: ast.Else):
        raise NotImplementedError()

    @abstractmethod
    def execute_Programme(self, programme: ast.Programme):
        raise NotImplementedError()

#class BaseVisitorEngine(BaseEngine):
#    @abstractmethod
#    def default_visit(self, node):
#        raise NotImplementedError()
#
#    def eval_Number(self, number: ast.Number):
#        self.visit_Number(number)
#    def visit_Number(self, number: ast.Number):
#        self.default_visit(number)
#
#    def eval_Variable(self, variable: ast.Variable):
#        self.visit_Variable(variable)
#    def visit_Variable(self, variable: ast.Variable):
#        self.default_visit(variable)
#
#    def eval_BinOp(self, binop: ast.BinOp):
#        self.visit_BinOp(binop)
#    def visit_BinOp(self, binop: ast.BinOp):
#        self.default_visit(binop)
#
#    def eval_Condition(self, condition: ast.Condition):
#        self.default_visit()
#
#    def execute_Repeat(self, repeat: ast.Repeat):
#        self.default_visit()
#
#    def execute_RepeatWhile(self, repeat_while: ast.RepeatWhile):
#        self.default_visit()
#
#    def execute_Step(self, step: ast.Step):
#        self.default_visit()
#
#    def execute_TurnLeft(self, turn_left: ast.TurnLeft):
#        self.default_visit()
#
#    def execute_TurnRight(self, turn_right: ast.TurnRight):
#        self.default_visit()
#
#    def execute_Jump(self, jump: ast.Jump):
#        self.default_visit()
#
#    def execute_PickUp(self, pick_up: ast.PickUp):
#        self.default_visit()
#
#    def execute_Activate(self, activate: ast.Activate):
#        self.default_visit()
#
#    def execute_Draw(self, draw: ast.Draw):
#        self.default_visit()
#
#    def execute_Place(self, place: ast.Place):
#        self.default_visit()
#
#    def execute_CallFunction(self, call_function: ast.CallFunction):
#        self.default_visit()
#
#    def execute_If(self, if_: ast.If):
#        self.default_visit()

# original ScottieGo forbids redefining variables, which are more like constants
class _ConstDict(dict):
    def __setitem__(self, key, value):
        if key in self:
            raise TypeError(f'cannot redefine variable {key}')
        super().__setitem__(key, value)

class ExecEngine(BaseEngine):
    class Break(BaseException):
        pass
    class BreakFunction(BaseException):
        pass

    def __init__(self, *args, allow_variable_reassignment=True, **kwds):
        super().__init__(*args, **kwds)
        self.variables = {} if allow_variable_reassignment else _ConstDict()
        self.functions = {}
        self.main: Optional[ast.Programme] = None

    def eval_Number(self, number):
        return number.value

    def eval_Variable(self, variable):
        try:
            return self.variables[variable.name]
        except KeyError:
            raise NameError(
                f'variable {self.varname} referenced before assignment '
                f'at line {self.line} block {self.cols[0]}')

    def eval_BinOp(self, binop):
        return binop.op(binop.left.eval(engine), binop.right.eval(engine))

    def eval_Condition(self, condition):
        return self.detect(condition.direction, condition.object)


    def execute_block(self, block):
        # TODO bracket
        for stmt in block:
            stmt.execute(self)

    def execute_Programme(self, programme):
        self.execute_block(programme.body)

    def execute_Repeat(self, repeat):
        if isinstance(repeat.counter, ast.Forever):
            counter = itertools.count(start=1)
        else:
            counter = range(1, repeat.counter.eval(self) + 1)

        for _i in counter:
#           assert i < 1000
            try:
                self.execute_block(repeat.body)
            except self.Break:
                break

    def execute_RepeatWhile(self, repeat_while):
        while repeat_while.condition.eval(self):
            try:
                self.execute_block(repeat_while.body)
            except self.Break:
                break

    def execute_If(self, if_):
        # TODO this will need to be fixed using iteration over linked list (not
        # recursion) because of the markers
        if if_.condition.eval(self):
            self.execute_block(if_.body)
        elif if_.orelse is not None:
            if_.orelse.execute(self)

    def execute_Else(self, else_):
        self.execute_block(else_.body)

    def execute_CallFunction(self, call_function):
        try:
            function = self.functions[call_function.name]
        except KeyError:
            raise NameError(
                f'function {call_function.name} undefined '
                f'at line {call_function.line} block {call_function.cols[0]}')

        function.execute(engine)

    def execute_Assign(self, assign):
        self.variables[assign.name] = assign.expression.eval(self)

    def execute_Place(self, place):
        return self.place(place.direction)

    def execute_Step(self, step):
        return self.step(step.counter.eval(self))

    def execute_Activate(self, activate):
        return self.activate()

    def execute_Draw(self, draw):
        return self.draw()

    def execute_Jump(self, jump):
        return self.jump()

    def execute_PickUp(self, pick_up):
        return self.pick_up()

    def execute_TurnLeft(self, turn_left):
        return self.turn_left()

    def execute_TurnRight(self, turn_right):
        return self.turn_right()

    def execute_Break(self, break_):
        raise self.Break()

    def execute_BreakFunction(self, break_function):
        raise self.BreakFunction()


    #
    # Abstract methods to be defined by game implementation
    # (e.g., pygame or physical robot)
    #

    @abstractmethod
    def step(self, counter: int):
        raise NotImplementedError()

    @abstractmethod
    def turn_left(self):
        raise NotImplementedError()

    @abstractmethod
    def turn_right(self):
        raise NotImplementedError()

    @abstractmethod
    def jump(self):
        raise NotImplementedError()

    @abstractmethod
    def pick_up(self):
        raise NotImplementedError()

    @abstractmethod
    def place(self, direction: ast.Direction):
        raise NotImplementedError()

    @abstractmethod
    def activate(self):
        raise NotImplementedError()

    @abstractmethod
    def draw(self):
        raise NotImplementedError()

    @abstractmethod
    def detect(self, direction: ast.Direction, obj: ast.Object):
        raise NotImplementedError()

    def noop(self):
        pass


class AsyncEngine(ExecEngine):
    async def eval_Number(self, number):
        return number.value

    async def eval_Variable(self, variable):
        try:
            return self.variables[variable.name]
        except KeyError:
            raise NameError(
                f'variable {self.varname} referenced before assignment '
                f'at line {self.line} block {self.cols[0]}')

    async def eval_BinOp(self, binop):
        return binop.op(await binop.left.eval(engine), await binop.right.eval(engine))

    async def eval_Condition(self, condition):
        logger.debug(f'{type(self).__name__}.eval_Condition()')
        return await self.detect(condition.direction, condition.object)


    async def execute_block(self, block):
        logger.debug(f'{type(self).__name__}.execute_block()')
        # TODO bracket
        for stmt in block:
            await stmt.execute(self)

    async def execute_Programme(self, programme):
        logger.debug(f'{type(self).__name__}.execute_Programme()')
        await self.execute_block(programme.body)

    async def execute_Repeat(self, repeat):
        logger.debug(f'{type(self).__name__}.execute_Repeat()')
        if isinstance(repeat.counter, ast.Forever):
            counter = itertools.count(start=1)
        else:
            counter = range(1, await repeat.counter.eval(self) + 1)

        for _i in counter:
#           assert i < 1000
            try:
                await self.execute_block(repeat.body)
            except self.Break:
                break

    async def execute_RepeatWhile(self, repeat_while):
        logger.debug(f'{type(self).__name__}.execute_RepeatWhile()')
        while await repeat_while.condition.eval(self):
            try:
                await self.execute_block(repeat_while.body)
            except self.Break:
                break

    async def execute_If(self, if_):
        # TODO this will need to be fixed using iteration over linked list (not
        # recursion) because of the markers
        if await if_.condition.eval(self):
            await self.execute_block(if_.body)
        elif if_.orelse is not None:
            await if_.orelse.execute(self)

    async def execute_Else(self, else_):
        await self.execute_block(else_.body)

    async def execute_CallFunction(self, call_function):
        try:
            function = self.functions[call_function.name]
        except KeyError:
            raise NameError(
                f'function {call_function.name} undefined '
                f'at line {call_function.line} block {call_function.cols[0]}')

        await function.execute(engine)

    async def execute_Assign(self, assign):
        self.variables[assign.name] = await assign.expression.eval(self)

    async def execute_Place(self, place):
        return await self.place(place.direction)

    async def execute_Step(self, step):
        return await self.step(await step.counter.eval(self))

    async def execute_Activate(self, activate):
        return await self.activate()

    async def execute_Draw(self, draw):
        return await self.draw()

    async def execute_Jump(self, jump):
        return await self.jump()

    async def execute_PickUp(self, pick_up):
        return await self.pick_up()

    async def execute_TurnLeft(self, turn_left):
        return await self.turn_left()

    async def execute_TurnRight(self, turn_right):
        return await self.turn_right()

    async def execute_Break(self, break_):
        raise self.Break()

    async def execute_BreakFunction(self, break_function):
        raise self.BreakFunction()


    #
    # Abstract methods to be defined by game implementation
    # (e.g., pygame or physical robot)
    #

    @abstractmethod
    async def step(self, counter: int):
        raise NotImplementedError()

    @abstractmethod
    async def turn_left(self):
        raise NotImplementedError()

    @abstractmethod
    async def turn_right(self):
        raise NotImplementedError()

    @abstractmethod
    async def jump(self):
        raise NotImplementedError()

    @abstractmethod
    async def pick_up(self):
        raise NotImplementedError()

    @abstractmethod
    async def place(self, direction: ast.Direction):
        raise NotImplementedError()

    @abstractmethod
    async def activate(self):
        raise NotImplementedError()

    @abstractmethod
    async def draw(self):
        raise NotImplementedError()

    @abstractmethod
    async def detect(self, direction: ast.Direction, obj: ast.Object):
        raise NotImplementedError()

    def noop(self):
        pass


class RemoteControlEngine(AsyncEngine):
    def __init__(self, *args, bot, **kwds):
        super().__init__(*args, **kwds)
        self.bot = bot

    async def step(self, counter: int):
        logger.debug(f'{type(self).__name__}.step({counter=})')
        r = range(abs(counter))
        logger.debug(f'  {r=}')
        for i in r:
            command = (bluetooth.Command.FORWARD if counter > 0
                else bluetooth.Command.BACKWARD)
            logger.debug(f'  {command=}')
            await asyncio.sleep(0.1)
            await self.bot.rpc(command)
        logger.debug(f'{type(self).__name__}.step() return')

    async def turn_left(self):
        await self.bot.rpc(bluetooth.Command.TURN_LEFT)

    async def turn_right(self):
        await self.bot.rpc(bluetooth.Command.TURN_RIGHT)

    async def jump(self):
        raise NotImplementedError()

    async def pick_up(self):
        raise NotImplementedError()

    async def place(self, direction: ast.Direction):
        raise NotImplementedError()

    async def activate(self):
        raise NotImplementedError()

    async def draw(self):
        raise NotImplementedError()

    async def detect(self, direction: ast.Direction, obj: ast.Object):
        logger.debug(f'{type(self).__name__}.detect({direction=}, {obj=})')
        if direction is not ast.Direction.IN_FRONT:
            raise NotImplementedError()

        if obj not in (ast.Object.OBSTACLE, ast.Object.EMPTY):
            raise NotImplementedError()

        sonar_range = await self.bot.sonar()
        logger.debug(f'{type(self).__name__}.detect {sonar_range=}')
        result = (sonar_range < 10) ^ (obj is ast.Object.EMPTY)
        logger.debug(f'{type(self).__name__}.detect -> {result}')
        return result


# vim: tw=80 ts=4 sts=4 sw=4 et
