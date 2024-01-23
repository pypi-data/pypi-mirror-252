# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: 2023 Wojtek Porczyk <woju@hackerspace.pl>

import pprint

from tuxgo import (
    blocks,
    parser,
)

def test_parser():
    parser.parse([
        (blocks.Token.BEGIN,),
            (blocks.Token.STEP, blocks.Token.DIGIT_6),
            (blocks.Token.REPEAT, blocks.Token.DIGIT_3),
                (blocks.Token.TURN_RIGHT,),
                (blocks.Token.STEP, blocks.Token.DIGIT_2),
                (blocks.Token.IF, blocks.Token.HERE, blocks.Token.COLLECTABLE),
                    (blocks.Token.PICK_UP,),
                (blocks.Token.ELSE_IF, blocks.Token.IN_FRONT, blocks.Token.MARK_1),
                    (blocks.Token.BREAK,),
                (blocks.Token.ELSE,),
                    (blocks.Token.CALL_FUNCTION, blocks.Token.A),
                (blocks.Token.END_BLOCK,),
            (blocks.Token.END_BLOCK,),
        (blocks.Token.END,),
    ])

def test_if():
    parser.parse([
        (blocks.Token.BEGIN,),
            (blocks.Token.IF, blocks.Token.HERE, blocks.Token.EMPTY),
                (blocks.Token.STEP, blocks.Token.DIGIT_1),
            (blocks.Token.END_BLOCK,),
        (blocks.Token.END,),
    ])

def test_if_else():
    parser.parse([
        (blocks.Token.BEGIN,),
            (blocks.Token.IF, blocks.Token.HERE, blocks.Token.EMPTY),
                (blocks.Token.STEP, blocks.Token.DIGIT_1),
            (blocks.Token.ELSE,),
                (blocks.Token.STEP, blocks.Token.DIGIT_2),
            (blocks.Token.END_BLOCK,),
        (blocks.Token.END,),
    ])

def test_if_elif():
    parser.parse([
        (blocks.Token.BEGIN,),
            (blocks.Token.IF, blocks.Token.HERE, blocks.Token.EMPTY),
                (blocks.Token.STEP, blocks.Token.DIGIT_1),
            (blocks.Token.ELSE_IF, blocks.Token.HERE, blocks.Token.EMPTY),
                (blocks.Token.STEP, blocks.Token.DIGIT_2),
            (blocks.Token.END_BLOCK,),
        (blocks.Token.END,),
    ])

def test_if_elif_else():
    parser.parse([
        (blocks.Token.BEGIN,),
            (blocks.Token.IF, blocks.Token.HERE, blocks.Token.EMPTY),
                (blocks.Token.STEP, blocks.Token.DIGIT_1),
            (blocks.Token.ELSE_IF, blocks.Token.HERE, blocks.Token.EMPTY),
                (blocks.Token.STEP, blocks.Token.DIGIT_2),
            (blocks.Token.ELSE,),
                (blocks.Token.STEP, blocks.Token.DIGIT_3),
            (blocks.Token.END_BLOCK,),
        (blocks.Token.END,),
    ])

def test_if_elif_elif():
    pprint.pprint(parser.parse([
        (blocks.Token.BEGIN,),
            (blocks.Token.IF, blocks.Token.HERE, blocks.Token.EMPTY),
                (blocks.Token.STEP, blocks.Token.DIGIT_1),
            (blocks.Token.ELSE_IF, blocks.Token.HERE, blocks.Token.EMPTY),
                (blocks.Token.STEP, blocks.Token.DIGIT_2),
            (blocks.Token.ELSE_IF, blocks.Token.HERE, blocks.Token.EMPTY),
                (blocks.Token.STEP, blocks.Token.DIGIT_3),
            (blocks.Token.END_BLOCK,),
        (blocks.Token.END,),
    ]))

def test_if_elif_elif_else():
    pprint.pprint(parser.parse([
        (blocks.Token.BEGIN,),
            (blocks.Token.IF, blocks.Token.HERE, blocks.Token.EMPTY),
                (blocks.Token.STEP, blocks.Token.DIGIT_1),
            (blocks.Token.ELSE_IF, blocks.Token.HERE, blocks.Token.EMPTY),
                (blocks.Token.STEP, blocks.Token.DIGIT_2),
            (blocks.Token.ELSE_IF, blocks.Token.HERE, blocks.Token.EMPTY),
                (blocks.Token.STEP, blocks.Token.DIGIT_3),
            (blocks.Token.ELSE,),
                (blocks.Token.STEP, blocks.Token.DIGIT_4),
            (blocks.Token.END_BLOCK,),
        (blocks.Token.END,),
    ]))

# vim: tw=80 ts=4 sts=4 sw=4 et
