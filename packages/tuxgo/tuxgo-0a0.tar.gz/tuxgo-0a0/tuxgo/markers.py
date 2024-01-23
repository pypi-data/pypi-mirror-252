# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: 2023 Wojtek Porczyk <woju@hackerspace.pl>

import os
import pathlib
from typing import Union

import click
import cv2.aruco
import numpy as np


class Generator:
    def __init__(self, dictionary: Union[cv2.aruco.Dictionary, int, str]):
        if isinstance(dictionary, str):
            dictionary = getattr(cv2.aruco, dictionary)
        if isinstance(dictionary, int):
            dictionary = cv2.aruco.getPredefinedDictionary(dictionary)
        self.dictionary = dictionary

    def range(self) -> range:
        return range(len(self.dictionary.bytesList))

    def generate_bitmap(self, id_: int) -> np.ndarray:
        return self.dictionary.drawMarker(
            id_, self.dictionary.markerSize + 2, borderBits=1
        ).astype(bool)

    def generate(
        self, id_: int, *, size=360: int, inverted=True: bool
    ) -> np.ndarray:
        im = self.dictionary.drawMarker(id_, size)
        if inverted:
            im = 255 - im
        return im

    def generate_to_file(
        self, id_: int, filename, *, size=360: int, inverted=True: bool
    ):
        im = self.generate(id_, size=size, inverted=inverted)
        cv2.imwrite(os.fspath(filename), im)


@click.command()
@click.option('--invert/--no-invert', default=True)
@click.option('--size', type=int, default=360)
@click.option('--output-dir', '-o', type=pathlib.Path, default='.')
@click.argument('dictionary')
@click.argument('id_', type=int)
@click.pass_context
def main(ctx, invert, size, dictionary, id_, output_dir):
    try:
        generator = Generator(dictionary)
    except AttributeError:
        ctx.fail(f'no such dictionary: {dictionary!r}')
    
    inv = 'I' if invert else 'N'
    if id_ < 0:
        with click.progressbar(generator.range()) as bar:
            for id_ in bar:
                generator.generate_to_file(id_,
                    output_dir / f'{dictionary}-{id_:03}-{inv}.png',
                    size=size, inverted=invert)
    else:
        generator.generate_to_file(id_,
            output_dir / f'{dictionary}-{id_:03}-{inv}.png',
            size=size, inverted=invert)


if __name__ == '__main__':
    main()

# vim: tw=80 ts=4 sts=4 sw=4 et
