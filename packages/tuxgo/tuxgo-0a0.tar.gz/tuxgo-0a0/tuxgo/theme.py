# SPDX-License-Identifier: AGPL-3.0-or-later
# SPDX-FileCopyrightText: 2023 Wojtek Porczyk <woju@hackerspace.pl>

import enum

# 37c3 colours
class Colour(tuple, enum.Enum):
    BLACK =     (  0,   0,   0) #000000
    WHITE =     (255, 255, 255) #ffffff
    GREY1 =     (217, 217, 217) #d9d9d9
    GREY2 =     (170, 170, 170) #aaaaaa
    GREY3 =     (122, 122, 122) #7a7a7a
    GREY4 =     ( 32,  32,  32) #202020
    BLUE =      ( 45,  66, 255) #2d42ff
    BLUE2 =     ( 11,  21, 117) #0b1575
    RED =       (222,  64,  64) #de4040
    RED2 =      ( 86,  16,  16) #561010
    GREEN =     (121, 255,  94) #79ff5e
    GREEN2 =    ( 43, 141,  24) #2b8d18
    CYAN =      ( 41, 255, 255) #29ffff
    CYAN2 =     (  0, 107, 107) #006b6b
    MAGENTA =   (222,  55, 255) #de37ff
    MAGENTA2 =  (102,   0, 122) #66007a
    YELLOW =    (246, 246, 117) #f6f675
    YELLOW2 =   (117, 177,   1) #757501
