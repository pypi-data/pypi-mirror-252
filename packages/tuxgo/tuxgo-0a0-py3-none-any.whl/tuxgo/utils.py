# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: 2023 Wojtek Porczyk <woju@hackerspace.pl>

import collections
import errno
import os
import pathlib
import time

class CPULoad:
    # see also: proc(5)

    def __init__(self):
        self._last = collections.defaultdict(lambda: (0, 0))
        self.usage = {}

    def update(self):
        with open('/proc/stat') as file:
            for line in file:
                if not line.startswith('cpu'):
                    continue
                cpu = line[3]
                cpu = None if cpu == ' ' else int(cpu)
                if cpu is None:
                    continue
                data = list(map(int, line.strip().split()[1:]))
                curr_sum, curr_idle = sum(data), data[3]
                last_sum, last_idle = self._last[cpu]
                try:
                    self.usage[cpu] = 100 * (
                        1 - (curr_idle - last_idle) / (curr_sum - last_sum))
                except ZeroDivisionError:
                    self.usage[cpu] = None
                self._last[cpu] = curr_sum, curr_idle

    def format_cpu(self, cpu):
        value = self.usage[cpu]
        value = '---.-' if value is None else f'{value:5.1f}'
        return f'CPU{cpu}: {value} %'

    def format_all(self):
        return ' '.join(self.format_cpu(cpu) for cpu in sorted(self.usage))


class _PWMProp:
    def __set_name__(self, owner, name):
        self.name = name
    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        data = (instance.path / self.name).read_text().strip()
        return int(data) if data.isdigit() else data
    def __set__(self, instance, value):
        (instance.path / self.name).write_text(str(value))

PWM_OPEN_RETRY_COUNT = 5

class PWM:
    def __init__(self, chip='pwmchip0', channel=0):
        self.path_chip = pathlib.Path('/sys/class/pwm') / chip
        try:
            (self.path_chip / 'export').write_text(str(channel))
        except OSError as e:
            if e.errno != errno.EBUSY:
                raise
        self.path = self.path_chip / f'pwm{channel}'

        # wait for udev to settle
        for i in range(PWM_OPEN_RETRY_COUNT):
            if os.access(self.path / 'enable', os.W_OK):
                break
            time.sleep(.1)

    duty_cycle = _PWMProp()
    enable = _PWMProp()
    period = _PWMProp()
    polarity = _PWMProp()

    @property
    def percent(self):
        return 100 * self.duty_cycle / self.period


def get_rfkill_state(name):
    for path in pathlib.Path('/sys/class/rfkill').glob('*'):
        if (path / 'name').read_text().strip() == name:
            return not int((path / 'state').read_text().strip())
