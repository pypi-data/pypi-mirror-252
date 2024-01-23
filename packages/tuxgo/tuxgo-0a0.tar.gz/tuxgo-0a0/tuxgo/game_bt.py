# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: 2023 Wojtek Porczyk <woju@hackerspace.pl>

import datetime
import enum
import sys

import click
import cv2
import funcparserlib.parser
import libcamera
import numpy as np
import picamera2
import pygame
import pygame.camera
import pygame.display
import pygame.event
import pygame.surfarray
import pygame.time

from abc import abstractmethod
from loguru import logger

from . import (
    assets,
    badges,
    bluetooth,
    detector as _detector,
    parser,
    utils,
)

from .theme import Colour



PYGAME_EVENT_UPDATE_CPU_LOAD = pygame.event.custom_type()


class Widgets:
    def __init__(self, surface):
        self.surface = surface
        self.surface_width, self.surface_height = self.surface.get_size()
        self.font = pygame.font.Font(assets / 'fonts/VCROCDFaux.ttf', 30)

    def label(self, text, /, *,
        fg=Colour.WHITE, bg=Colour.BLACK,
        top=None, bottom=None, left=None, right=None,
    ):
        assert (top is not None) ^ (bottom is not None)
        assert (left is not None) ^ (right is not None)

        fontsurf = self.font.render(text, True, fg, bg)
        width, height = fontsurf.get_size()

        x = left if left is not None else self.surface_width - width - right
        y = (top * height if top is not None
            else self.surface_height - (bottom + 1) * height)
        self.surface.blit(fontsurf, (x, y))

    def key(self, key, descr, /, *,
        top=None, bottom=None, left=None, right=None,
    ):
        assert (top is not None) ^ (bottom is not None)
        assert (left is not None) ^ (right is not None)

        keysurf = self.font.render(key, True, Colour.WHITE, Colour.BLUE)
        descrsurf = self.font.render(' ' + descr, True, Colour.BLACK, Colour.WHITE)
        width, height = descrsurf.get_size()

        x = left if left is not None else self.surface_width - width - right
        y = (top * height if top is not None
            else self.surface_height - (bottom + 1) * height)

        self.surface.blit(descrsurf, (x, y))
        self.surface.blit(keysurf, (x - keysurf.get_width(), y))


class Component:
    def __init__(self, game):
        self.game = game

    def add_widgets(self):
        pass

    def handle_event(self, event):
        pass


class RobotComponent(Component):
    def add_widgets(self):
        if self.game.bot.connected:
            self.game.widgets.label(f'CONNECTED',
                bottom=2, left=0, bg=Colour.GREEN2)
            self.game.widgets.key('WSAD', 'Move robot',
                bottom=1, left=100)
            self.game.widgets.key('E', 'Sonar',
                bottom=1, left=350)

            if self.game.bot.last_range is not None:
                self.game.widgets.label(f'RANGE: {self.game.bot.last_range:3d} cm',
                    bottom=2, left=350)
        elif self.game.bot.loop is not None:
            self.game.widgets.label(f'CONNECTING',
                bottom=2, left=0)
        else:
            self.game.widgets.label(f'DISCONNECTED',
                bottom=2, left=0, bg=Colour.RED)
            self.game.widgets.key('R', 'Reconnect',
                bottom=1, left=100)

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if self.game.bot.connected:
            if event.key == pygame.K_w:
                self.game.bot.forward_nowait()
                return True
            if event.key == pygame.K_s:
                self.game.bot.backward_nowait()
                return True
            if event.key == pygame.K_a:
                self.game.bot.turn_left_nowait()
                return True
            if event.key == pygame.K_d:
                self.game.bot.turn_right_nowait()
                return True
            if event.key == pygame.K_e:
                self.game.bot.sonar_nowait()
                return True

        elif self.game.bot.loop is None:
            if event.key == pygame.K_r:
                self.game.bot.connect()
                return True

class BadgesComponent(Component):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.enabled = not all(badge is None for badge in self.game.badges)

    def add_widgets(self):
        if self.enabled:
            self.game.widgets.key('B', 'Badges', bottom=1, left=850)

    def handle_event(self, event):
        if (self.enabled
        and event.type == pygame.KEYDOWN
        and event.key == pygame.K_b):
            self.game.mode = self.game.mode_badges
            return True

class ClockComponent(Component):
    def add_widgets(self):
        self.game.widgets.label(f'{datetime.datetime.now():%H:%M}',
            top=0, right=0)

class CPUComponent(Component):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.cpuload = utils.CPULoad()
        self.cpuload.update()
        pygame.time.set_timer(PYGAME_EVENT_UPDATE_CPU_LOAD, 1000)

    def add_widgets(self):
        self.game.widgets.label(self.cpuload.format_all(), top=0, left=0)

    def handle_event(self, event):
        if event.type == PYGAME_EVENT_UPDATE_CPU_LOAD:
            self.cpuload.update()
            return True

class PWMComponent(Component):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.pwm = utils.PWM()
        self.pwm.period = 1000000 # ns -> 1 kHz
        self.pwm.duty_cycle = 0
        self.pwm.enable = 1

    def add_widgets(self):
        self.game.widgets.key('[]', 'Lamp ctl.', bottom=0, left=600)

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_LEFTBRACKET:
            self.pwm.duty_cycle = max(0, self.pwm.duty_cycle - 100000)
            return True
        if event.key == pygame.K_RIGHTBRACKET:
            self.pwm.duty_cycle = min(1000000, self.pwm.duty_cycle + 100000)
            return True

class RFKillComponent(Component):
    def add_widgets(self):
        if not utils.get_rfkill_state('phy0'):
            self.game.widgets.label('WIFI NOT RFKILL\'D', bottom=3, left=0, bg=Colour.RED)

class Game:
    def __init__(self, screen, bot):
        self.screen = screen
        self.screen_width, self.screen_height = self.screen.get_size()
        self.font_vcr_60 = pygame.font.Font(assets / 'fonts/VCROCDFaux.ttf', 60)
        self.widgets = Widgets(self.screen)
        self.clock = pygame.time.Clock()

        self.mode = self.mode_normal

        self.bot = bot

        self.camera = None
        self.detector = _detector.Detector()
        self.frame = None
        self.metadata = None

        self.badges = list(badges.Badge.load_from_assets())
        self.current_badge = None

        self.comp_clock = ClockComponent(self)
        self.comp_robot = RobotComponent(self)
        self.comp_badges = BadgesComponent(self)
        self.comp_cpu = CPUComponent(self)
        self.comp_pwm = PWMComponent(self)
        self.comp_rfkill = RFKillComponent(self)


    def run(self):
        self.init_camera()
        self.camera.start()
        try:
            while True:
                self.mode()
                pygame.display.flip()
                self.clock.tick(50)

        finally:
            self.comp_pwm.pwm.enable = 0
            try:
                self.camera.stop()
            except SystemError: # raised on double stop
                pass


    #
    # CAMERA FUNCTIONS
    #

    def init_camera(self):
        self.camera = picamera2.Picamera2()
        self.camera.configure(self.camera.create_preview_configuration(
            main={
                'format': 'BGR888',
                'size': (int(self.screen_height * 1.3), int(self.screen_width * 1.3)),
            },
            lores=None,
            raw=None,
            display=None,
            encode=None,
            controls={
                'ExposureValue': 1.1,
            },
        ))

    def capture_frame(self):
        request = self.camera.capture_request()
        self.frame = np.rot90(request.make_array('main')).copy()
        self.metadata = picamera2.Metadata(request.get_metadata())
        request.release()


    #
    # COMPONENTS AND EVENT HANDLING
    #

    def handle_exit(self, event):
        if (event.type == pygame.QUIT
        or (event.type == pygame.KEYDOWN and event.key == pygame.K_q)):
            if self.bot.loop is not None:
                self.bot.disconnect()
            sys.exit()

    def handle_event(self, components, event):
        self.handle_exit(event)

        # CPULoad is a bit special, we need to always catch the timer event,
        # no matter which mode we're in
        if self.comp_cpu.handle_event(event):
            return

        for component in components:
            if component.handle_event(event):
                break

    def add_widgets(self, components):
        for component in components:
            component.add_widgets()

    #
    # SCREEN MODES
    #

    def mode_normal(self):
        components = (
            self.comp_clock,
            self.comp_robot,
            self.comp_badges,
            self.comp_cpu,
            self.comp_pwm,
            self.comp_rfkill,
        )

        self.capture_frame()
        display_frame = self.frame.copy()

        detections = self.detector.detect_markers(self.frame)
        analyser = _detector.Analyser(detections)
        for detection in detections:
            detection.debug_draw(display_frame)
        try:
            programme = list(analyser.get_programme(debug_frame=display_frame))
        except _detector.BoardError:
            error = True
        else:
            error = False

#           surface = pygame.surfarray.make_surface(frame.T)

        # XXX WTF this math, TODO get understanding
        surface = pygame.surfarray.make_surface(np.flipud(np.rot90(display_frame)))
        surface = pygame.transform.scale(surface, self.screen.get_size())
        frame_width, frame_height = surface.get_size()
#       logger.debug(f'{surface.get_size()=}')

        self.screen.blit(surface, (
            (self.screen_width  - frame_width)  / 2, 
            (self.screen_height - frame_height) / 2))

        self.widgets.label(f'EXP: {self.metadata.ExposureTime:5} us',
            top=1, left=0)
        self.widgets.label(f'GAIN:'
            f' A{self.metadata.AnalogueGain:.1f}'
            f' D{self.metadata.DigitalGain:.1f}'
            f' R{self.metadata.ColourGains[0]:.1f}'
            f' B{self.metadata.ColourGains[1]:.1f}',
            top=1, left=240)
        self.widgets.label(f'BLUR: {self.detector.blur} px',
            top=1, left=650)
        self.widgets.label(f'FPS: {self.clock.get_fps():4.1f} Hz',
            top=1, right=0)

        self.widgets.label(f'SHUTTER: 1/{1000000/self.metadata.ExposureTime:3.0f} s',
            top=2, left=0)
        self.widgets.label(f'ILLUM: {self.metadata.Lux:4.0f} lux',
            top=2, left=300)
        self.widgets.label(f'PWM: {self.comp_pwm.pwm.percent:3.0f} %',
            top=2, left=600)

        self.widgets.label(f'TEMP: {self.metadata.SensorTemperature:2.0f} °C',
            top=2, right=0)



        if error:
            self.widgets.label('ERROR', bottom=2, right=0, bg=Colour.RED)
        else:
            self.widgets.label('OK', bottom=2, right=0)

        self.widgets.key('SPACE', 'Snapshot', bottom=0, left=100)

#       self.widgets.key('C', 'Cam. sett.', bottom=1, left=600)
#       self.widgets.key('I', 'Load file', bottom=0, left=600)
        self.widgets.key('+-', 'Blur ctl.', bottom=1, left=600)

        self.widgets.key('Q', 'Quit', bottom=0, left=850)

        self.add_widgets(components)
#       for i, item in enumerate(self.metadata.__dict__.items()):
#           k, v = item
#           self.widgets.label(f'{k}: {v}', left=0, top=i + 3)


        for event in pygame.event.get():
            self.handle_event(components, event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.mode = self.mode_snapshot

                if event.key == pygame.K_MINUS:
                    self.detector.blur = max(1, self.detector.blur - 1)
                if event.key in (pygame.K_PLUS, pygame.K_EQUALS):
                    self.detector.blur += 1


    def mode_snapshot(self):
        components = (
            self.comp_clock,
            self.comp_robot,
            self.comp_badges,
            self.comp_pwm,
            self.comp_rfkill,
        )

        display_frame = self.frame.copy()
        detections = self.detector.detect_markers(self.frame)
        analyser = _detector.Analyser(detections)
        for detection in detections:
            detection.debug_draw(display_frame)
        try:
            programme = list(analyser.get_programme(debug_frame=display_frame))
            parsed = parser.parse(programme)

        except (_detector.BoardError, funcparserlib.parser.NoParseError):
            error = True
        else:
            error = False

#           surface = pygame.surfarray.make_surface(frame.T)

        # XXX WTF this math, TODO get understanding
        surface = pygame.surfarray.make_surface(np.flipud(np.rot90(display_frame)))
        surface = pygame.transform.scale(surface, self.screen.get_size())
        frame_width, frame_height = surface.get_size()
#       logger.debug(f'{surface.get_size()=}')

        self.screen.blit(surface, (
            (self.screen_width  - frame_width)  / 2, 
            (self.screen_height - frame_height) / 2))

        self.add_widgets(components)
        self.widgets.key('SPACE', 'Snapshot', bottom=0, left=100)
        self.widgets.key('Q', 'Quit', bottom=0, left=850)

        if error:
            self.widgets.label('ERROR', bottom=2, right=0, bg=Colour.RED)
        else:
            for i, line in enumerate(programme, 1):
                line = ' '.join(token.value.text for token in line)
                self.widgets.label(f'{i:2d} {line}', top=i, left=0)
            self.widgets.label('OK', bottom=2, right=0)

            if self.bot.connected:
                if self.bot.current_task is not None:
                    self.widgets.key('X', 'Stop', bottom=0, left=350)
                elif not error:
                    self.widgets.key('R', 'Run', bottom=0, left=350)

        for event in pygame.event.get():
            self.handle_event(components, event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.mode = self.mode_normal

                if event.key == pygame.K_SPACE:
                    self.capture_frame()

                if self.bot.connected:
                    if self.bot.current_task is not None:
                        if event.key == pygame.K_x:
                           self.bot.stop_programme()
                    elif not error:
                        if event.key == pygame.K_r:
                           self.bot.execute_programme(parsed)

    def mode_badges(self):
        self.screen.fill((0, 0, 0))

        image_size = 256
        assert self.screen_height == 1280

        padding = (self.screen_width - 2 * image_size) / 3

        for i, badge in enumerate(self.badges):
            if badge is None:
                continue

            x = padding + (image_size + padding) * (i // 5)
            y = image_size * (i % 5)

            image = pygame.transform.scale(
                badge.image_menu or badge.image, (image_size, image_size))

            label = self.font_vcr_60.render(
                str((i + 1) % 10), True, (0, 0, 0), (255, 255, 255))

            self.screen.blit(image, (x, y))
            self.screen.blit(label, (x - label.get_width() - 16, y))

        for event in pygame.event.get():
            self.handle_event((), event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.mode = self.mode_normal
                    continue

                for i in range(min(len(self.badges), 10)):
                    if event.key == getattr(pygame, f'K_{(i + 1) % 10}'):
                        if self.badges[i] is not None:
                            self.mode = self.mode_badge
                            self.current_badge = self.badges[i]

    def mode_badge(self):
        assert self.current_badge

        padding = 48

        self.screen.fill((0, 0, 0))

        qrcode_size = (self.screen_height
            - 3 * padding - self.current_badge.image.get_height())
        qrcode = pygame.transform.scale(
            self.current_badge.qrcode, (qrcode_size, qrcode_size))

        self.screen.blit(qrcode,
            ((self.screen_width - qrcode_size) / 2, padding))
        self.screen.blit(self.current_badge.image, (
            (self.screen_width - self.current_badge.image.get_width()) / 2,
            (self.screen_height - self.current_badge.image.get_height() - padding)
        ))

        for event in pygame.event.get():
            self.handle_event((), event)

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_b):
                    self.mode = self.mode_badges
                    self.current_badge = None
                    continue

                for i in range(min(len(self.badges), 10)):
                    if event.key == getattr(pygame, f'K_{(i + 1) % 10}'):
                        if self.badges[i] is not None:
                            self.current_badge = self.badges[i]

    def mode_camera_settings(self):
        raise NotImplementedError()

    def mode_load_file(self):
        raise NotImplementedError()


# vim: tw=80 ts=4 sts=4 sw=4 et
