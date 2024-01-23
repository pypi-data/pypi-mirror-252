# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: 2023 Wojtek Porczyk <woju@hackerspace.pl>

import tomllib

import cv2

import pygame
import pygame.image
import pygame.surfarray

from . import assets

class Badge:
    def __init__(self, qrcode, image, image_menu=None):
        self.qrcode = qrcode
        self.image = image
        self.image_menu = image_menu

    @classmethod
    def load_from_assets(cls):
        data = tomllib.load(open(assets / 'badges/badges.toml', 'rb'))
        url_template = data['url_template']

        for badge in data['badge']:
            if not badge:
                yield None
                continue

            url = url_template.format(token=badge.pop('token'))
            qrcode = pygame.surfarray.make_surface(
                cv2.QRCodeEncoder.create().encode(url))

            image_path = assets / 'badges' / badge.pop('image')
            image = pygame.image.load(image_path)

            try:
                image_menu_path = assets / 'badges' / badge.pop('image_menu')
            except KeyError:
                image_menu = None
            else:
                image_menu = pygame.image.load(image_menu_path)
            
            assert not badge
            yield cls(qrcode, image, image_menu)

if __name__ == '__main__':
    main()

# vim: tw=80 ts=4 sts=4 sw=4 et
