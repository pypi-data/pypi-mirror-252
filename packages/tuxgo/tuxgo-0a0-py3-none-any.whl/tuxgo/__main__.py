# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: 2023 Wojtek Porczyk <woju@hackerspace.pl>

import pprint

import click
import click_default_group
import cv2
import pygame
import pygame.display

from loguru import logger

from . import (
    detector as _detector,
    game_bt,
    bluetooth,
)

@click.group(cls=click_default_group.DefaultGroup, default='game',
    default_if_no_args=True)
def cli():
    pass

@cli.command('game')
@click.option('--mac', required=True)
def game(mac):
    logger.debug('pygame.init()')
    pygame.init()
    pygame.display.set_caption('tuxgo')
    screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
    bot = bluetooth.BluetoothBot(mac)
    game = game_bt.Game(screen, bot)
    game.run()


@cli.command('debug-image')
@click.argument('inpath', type=click.Path(file_okay=True, dir_okay=False))
@click.argument('outpath', type=click.Path(file_okay=True, dir_okay=False))
def debug_image(inpath, outpath):
    detector = _detector.Detector()
    frame = cv2.imread(inpath)
    #frame = cv2.blur(frame, (5, 5))
    detections = list(detector.detect_markers(frame))
    analyser = _detector.Analyser(detections)
    try:
        programme = list(analyser.get_programme(debug_frame=frame))
        pprint.pprint(programme)
    finally:
        cv2.imwrite(outpath, frame)

@cli.command('debug-video')
def debug_video():
    vc = cv2.VideoCapture(0)
    detector = _detector.Detector()

    try:
        while True:
            ret, frame = vc.read()
            if not ret:
                click.echo('frame dropped', err=True)
                continue

            flipped = cv2.flip(frame, 1)

            for detection in detector.detect_markers(frame):
                detection.debug_draw_flipped(flipped)

            cv2.imshow('tuxgo-debug', flipped)

            key = cv2.waitKey(1)
            if key & 0xff == ord('q'):
                break
            elif key & 0xff == ord('f'):
                cv2.imwrite('screenshot.png', flipped)

    finally:
        vc.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    cli()
