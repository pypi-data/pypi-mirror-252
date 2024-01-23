# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: 2023 Wojtek Porczyk <woju@hackerspace.pl>

# TODO rewrite in concurrent.futures

import asyncio
import enum
import sys
import threading

import bleak

from loguru import logger

from . import (
    engine,
)

NORDIC_UART_RX = '6e400002-b5a3-f393-e0a9-e50e24dcca9e'
NORDIC_UART_TX = '6e400003-b5a3-f393-e0a9-e50e24dcca9e'

class Command(bytes, enum.Enum):
    TURN_LEFT =     b'H'
    BACKWARD =      b'J'
    FORWARD =       b'K'
    TURN_RIGHT =    b'L'
    SONAR =         b'S'


class BluetoothBot:
    def __init__(self, mac):
        self.mac = mac
        self.loop = None
        self.queue = None
        self.thread = None
        self.connected = False
        self.last_range = None

        self.engine = engine.RemoteControlEngine(bot=self)
        self.current_task = None

    def connect(self):
        assert self.loop is None
        self.thread = threading.Thread(target=asyncio.run, args=(self._main(),))
        self.thread.start()

    def disconnect(self):
        assert self.loop is not None
        asyncio.run_coroutine_threadsafe(
            self.queue.put((None, None)), self.loop)
        self.thread.join()

    def execute_programme(self, programme):
        logger.debug(f'{type(self).__name__}.execute_programme()')
        assert self.loop is not None
        assert self.current_task is None
        self.current_task = asyncio.run_coroutine_threadsafe(self._execute(programme), self.loop)

    def stop_programme(self):
        assert self.loop is not None
        assert self.current_task is not None
        self.current_task.cancel()


    async def _execute(self, programme):
        logger.debug(f'{type(self).__name__}._execute()')
        try:
            await programme.execute(self.engine)
        finally:
            self.current_task = None


    async def rpc(self, command):
        logger.debug(f'{type(self).__name__}.rpc({command=})')
        future = self.loop.create_future()
        await self.queue.put((command, future))
        return await future

    async def turn_left(self):
        await self.rpc(Command.TURN_LEFT)
    async def backward(self):
        await self.rpc(Command.BACKWARD)
    async def forward(self):
        await self.rpc(Command.FORWARD)
    async def turn_right(self):
        await self.rpc(Command.TURN_RIGHT)
    async def sonar(self):
        return (await self.rpc(Command.SONAR))[0]

    def rpc_threadsafe(self, command, *, timeout=None):
        assert self.loop is not None
        future = asyncio.run_coroutine_threadsafe(self.rpc(command), self.loop)
        return future.result(timeout=timeout)

    def turn_left_threadsafe(self):
        self.rpc_threadsafe(Command.TURN_LEFT)
    def backward_threadsafe(self):
        self.rpc_threadsafe(Command.BACKWARD)
    def forward_threadsafe(self):
        self.rpc_threadsafe(Command.FORWARD)
    def turn_right_threadsafe(self):
        self.rpc_threadsafe(Command.TURN_RIGHT)
    def sonar_threadsafe(self):
        return self.rpc_threadsafe(Command.SONAR)[0]


    def rpc_nowait(self, command):
        asyncio.run_coroutine_threadsafe(self.rpc(command), self.loop)

    def turn_left_nowait(self):
        self.rpc_nowait(Command.TURN_LEFT)
    def backward_nowait(self):
        self.rpc_nowait(Command.BACKWARD)
    def forward_nowait(self):
        self.rpc_nowait(Command.FORWARD)
    def turn_right_nowait(self):
        self.rpc_nowait(Command.TURN_RIGHT)
    def sonar_nowait(self):
        self.rpc_nowait(Command.SONAR)


    async def _main(self):
        self.loop = asyncio.get_running_loop()
        self.last_range = None

        try:
            async with bleak.BleakClient(self.mac) as client:
                nordic_uart_tx = client.services.get_characteristic(NORDIC_UART_TX)
                nordic_uart_rx = client.services.get_characteristic(NORDIC_UART_RX)

                self.connected = True
                self.queue = asyncio.Queue(1)
                while True:
                    command, future = await self.queue.get()
                    if command is None:
                        # disconnect
                        break

                    async def handle_tx(_characteristic, data):
                        logger.debug(f'handle_tx(..., {data=})')
                        future.set_result(data)
                        if command is Command.SONAR:
                            self.last_range = data[0]

                    await client.start_notify(nordic_uart_tx, handle_tx)

                    await client.write_gatt_char(nordic_uart_rx, command)
                    try:
                        await future
                    except asyncio.CancelledError:
                        pass
                    await client.stop_notify(nordic_uart_tx)
                    self.queue.task_done()

        except bleak.BleakError:
            # TODO register handler for disconnect
            pass

        finally:
            self.connected = False
            self.loop = None

