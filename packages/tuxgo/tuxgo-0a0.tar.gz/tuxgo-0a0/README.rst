Tux Go
======

Hardware requirements
---------------------

Control box
^^^^^^^^^^^
- Raspberry Pi 4+ or later
- Camera (tested with Camera Module 3)
- Monitor that can be rotated to vertical (tested on 1024x1280)
- Keyboard

Robot
^^^^^
- bbc:microbit v1
- DFRobot Maqueen

It is technically possible to write firmware for any robot that can connect over
Bluetooth LE. Contributions are welcome.

Getting started
---------------

- Install RaspberryPi OS (at least 12/bookworm) on the SD card, as documented in
  RPi documentation.
- Connect camera, keyboard and display.
- Start RPi and configure screen to vertical.
- Install dependencies:

  .. code-block:: sh
  
      sudo apt-get install \
          python3-bleak \
          python3-click \
          python3-click-default-group \
          python3-flask \
          python3-funcparserlib \
          python3-loguru
          python3-matplotlib \
          python3-opencv \
          python3-werkzeug \

- Run the game:

  .. code-block:: sh

      python3 -m tuxgo

Acknowledgements
----------------

In rough order of the pipeline that processes data in this project, Author would
like to acknowledge the following projects and people:

Scottie Go
^^^^^^^^^^
Original game by BeCreo, for the idea. This thing is largely a reimplementation
of Scottie Go, because I wanted to drive a physical robot with the tiles and
AFAIK there's no way in ecosystem to do just that.

This project does not contain any code or assets from the original game, neither
the Author read the source code or reversed the binaries. But you can still
support BeCreo by buying original game from their store.

web page: https://scottiego.com/
support (online store): https://www.shop.scottiego.com/

Python
^^^^^^
This application was written in Python for the benefit of teachers and students
alike. Author feels that this language is a good choice to write an educational
app, since Python is taught in Polish schools as part of curriculum.

OpenCV
^^^^^^
The state-of-the-art image detection and marker recognition library, used to
detect ArUco markers on the game tiles.

web page: TBD support: TBD

numpy and matplotlib 
^^^^^^^^^^^^^^^^^^^^
Maths libraries from the Python's scientific subculture. NumPy is used for
general computation (also at the interface of OpenCV) and matplotlib happens to
contain very useful modules for affine transforms and polygon collisions.

numpy Web page: https://numpy.org/
numpy Support: https://numpy.org/about/#donate

matplotlib web page: https://matplotlib.org/
matplotlib support: https://numfocus.org/donate-to-matplotlib

funcparserlib
^^^^^^^^^^^^^
Smart little tool for writing parsers. Used to parse detected pieces into
abstract syntax tree.

web page: https://funcparserlib.pirx.ru/
github repo: https://github.com/vlasovskikh/funcparserlib
support: *(please do not support .ru people unless they migrate out of Russia)*

PyGame
^^^^^^
Python framework for writing games. Used for the visual interface, which
displays simulation.

web page: https://www.pygame.org/
support: https://www.pygame.org/contribute.html

Johann C
^^^^^^^^
For isometric artwork, which I've reused for this game in simulation mode. The
artwork is available at OpenGameArt in public domain (CC0):

- https://opengameart.org/content/svg-isometric-robot
- https://opengameart.org/content/svg-isometric-tileset

AFAIK the artwork was originally made for a programming game called simply
“Robot”: https://jlodb.poufpoufproduction.fr/report.html?activity=robot, which
is very different in style. Try it yourself.

But this artwork was reused and adapted by various people for other little
games, of which I've particularly enjoyed “iNTRUDER - The nukebot” by looneybits
(https://looneybits.itch.io/intruder,
https://opengameart.org/content/intruder-the-nukebot).

web page: https://poufpoufproduction.fr/ (has link to Fedi account)

Various Python libraries' authors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Pallets: For Flask and Werkzeug, which are used to serve a temporary HTTP server.


Dedication
----------

*To my Daughters: Marta, Ola and Klara.*

.. vim: tw=80 ts=4 sts=4 sw=4 et
