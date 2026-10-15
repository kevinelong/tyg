"""The scripted session behind docs/demo.svg, and the frames it draws.

docs/make_screenshot.py renders those frames; pilot/test.py recomputes them and
fails when docs/demo-frames.txt no longer matches, so the picture in the README
cannot quietly drift away from what the game prints.
"""
import contextlib
import io
import random
import re

from pilot.lib.controls import handle
from pilot.lib.game import Game

SEED = 16
KEYS = ('k', 'k', 'l', 'DOWN', 'l', 'k', 'k',
        'a', 's', 'k', 'UP', 'j', 'h')

ESCAPES = re.compile(r'\x1b\[[0-9;?]*[a-zA-Z]')


def frame_lines(output):
    """One frame of drawn output as printable lines, cursor codes removed."""
    return ESCAPES.sub('', output.replace('\r', '')).splitlines()


def draw(game):
    """One frame of output, as play() writes it."""
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        game.draw()
    return frame_lines(buffer.getvalue())


def frames():
    """Every frame the demo session draws, in the order play() draws them.

    play() draws, then reads a key, so N keypresses leave N + 1 frames: the
    state each key was pressed in, then the state it left behind.
    """
    random.seed(SEED)
    game = Game()
    drawn = []
    for key in KEYS:
        drawn.append(draw(game))
        if not handle(game, key):
            break
    drawn.append(draw(game))
    return drawn


def text_dump():
    """The frames as one text block: what the SVG shows, readable in a diff."""
    return '\n\n'.join('\n'.join(frame) for frame in frames()) + '\n'
