# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: 2023 Wojtek Porczyk <woju@hackerspace.pl>

import os
import pathlib

import cv2
import pytest

from tuxgo import (
    blocks,
    detector,
)

@pytest.fixture
def load_frame():
    def load_frame(filename):
        return cv2.imread(os.fspath(pathlib.Path(__file__).parent / filename))
    return load_frame

@pytest.fixture
def detect_markers_in_frame(load_frame):
    def detect_markers_in_frame(frame):
        return detector.Detector().detect_markers(load_frame(frame))
    return detect_markers_in_frame

def test_trivial(detect_markers_in_frame):
    analyser = detector.Analyser(detect_markers_in_frame('test_trivial.jpg'))
    assert list(analyser.get_programme()) == [
        (blocks.Token.BEGIN,),
        (blocks.Token.END,),
    ]

rotate_programme = [
    (blocks.Token.BEGIN,),
    (blocks.Token.STEP, blocks.Token.DIGIT_6),
    (blocks.Token.REPEAT, blocks.Token.DIGIT_3),
    (blocks.Token.TURN_RIGHT,),
    (blocks.Token.STEP, blocks.Token.DIGIT_2),
    (blocks.Token.PICK_UP,),
    (blocks.Token.END_BLOCK,),
    (blocks.Token.END,),
]

@pytest.mark.parametrize('rot', [0, 45, 90])
def test_rotate(detect_markers_in_frame, rot):
    analyser = detector.Analyser(detect_markers_in_frame(
        f'test_rotate_{rot:02d}.jpg'))
    assert list(analyser.get_programme()) == rotate_programme

# vim: tw=80 ts=4 sts=4 sw=4 et
