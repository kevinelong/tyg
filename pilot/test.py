"""
Requirements:
SETUP:
1. Show Map of specified width and height, default to 9x9.
2. Show Character center of the Map.
3. Place and show a treasure on the map in random position that is not next to or on the player.

TURN:
4. Ask user to if the they want to turn A--rotate-left, D--Rotate-Right or S-MOve-straight.
5. Rotate or move character Move character in specified direction
6. Block moves that would go off the map. If blocked then turn 180 degrees.
7. if player and treasure collide then remove treasure and add a new one in a blank square.
8. Arrow keys and HJKL also move: each one faces and steps a square in the
   direction pressed. Any other key is ignored, and Q quits.
9. Count collected treasures, show the tally under the board, and win once
   the goal is reached (10 by default). Redraw in place, and stop cleanly
   when the terminal gives no more input.

Run from the repository root: python3 -m pilot.test
"""
import contextlib
import io
import pathlib

from pilot import demo
from pilot.lib.character import DOWN, LEFT, RIGHT, UP
from pilot.lib.controls import handle
from pilot.lib.game import Game
from pilot.lib.keys import (ERR, ESCAPE, ESCAPE_TIMEOUT, GET_KEY_MAP, UNKNOWN,
                            match_escape, read_key)
from pilot.lib.position import Position

WIDTH = HEIGHT = 9
CENTER = WIDTH // 2


def new_game():
    """A game with the treasure parked in a corner, out of the way."""
    game = Game()
    game.treasure.position.x = 0
    game.treasure.position.y = 0
    return game


# SETUP
g = Game()
assert(g is not None)
assert(g.board.width == WIDTH)
assert(g.board.height == HEIGHT)
assert(g.character.position.x == CENTER)
assert(g.character.position.y == CENTER)
assert(0 <= g.treasure.position.x <= WIDTH - 1)
assert(0 <= g.treasure.position.y <= HEIGHT - 1)
assert(max(abs(g.treasure.position.x - CENTER),
           abs(g.treasure.position.y - CENTER)) > 1)

# FACING: direction 0..3 renders as ^ > v < clockwise
assert(g.character.direction == UP)
assert(g.character.symbol == '^')
g.character.turnRight()
assert(g.character.direction == RIGHT)
assert(g.character.symbol == '>')
g.character.turnRight()
assert(g.character.direction == DOWN)
assert(g.character.symbol == 'v')
g.character.turnRight()
assert(g.character.direction == LEFT)
assert(g.character.symbol == '<')
g.character.turnRight()
assert(g.character.direction == UP)
assert(g.character.symbol == '^')
g.character.turnLeft()
assert(g.character.direction == LEFT)
g.character.turnRight()
assert(g.character.direction == UP)
g.character.turnRight()
g.character.turnRight()
g.character.turnRight()
g.character.turnRight()
assert(g.character.direction == UP)

# KEYS: a and d turn, s steps forward
g = new_game()
assert(handle(g, 'a') is True)
assert(g.character.direction == LEFT)
assert(handle(g, 'd') is True)
assert(g.character.direction == UP)
assert(handle(g, 'd') is True)
assert(g.character.direction == RIGHT)
assert(handle(g, 's') is True)
assert((g.character.position.x, g.character.position.y) == (CENTER + 1, CENTER))

# KEYS: arrows and hjkl face and step one square
g = new_game()
assert(handle(g, 'h') is True)
assert((g.character.position.x, g.character.position.y) == (CENTER - 1, CENTER))
assert(g.character.symbol == '<')
assert(handle(g, 'j') is True)
assert((g.character.position.x, g.character.position.y) == (CENTER - 1, CENTER + 1))
assert(g.character.symbol == 'v')
assert(handle(g, 'k') is True)
assert((g.character.position.x, g.character.position.y) == (CENTER - 1, CENTER))
assert(g.character.symbol == '^')
assert(handle(g, 'l') is True)
assert((g.character.position.x, g.character.position.y) == (CENTER, CENTER))
assert(g.character.symbol == '>')
assert(handle(g, 'LEFT') is True)
assert((g.character.position.x, g.character.position.y) == (CENTER - 1, CENTER))
assert(handle(g, 'UP') is True)
assert((g.character.position.x, g.character.position.y) == (CENTER - 1, CENTER - 1))
assert(handle(g, 'DOWN') is True)
assert(handle(g, 'RIGHT') is True)
assert((g.character.position.x, g.character.position.y) == (CENTER, CENTER))
assert(handle(g, 'z') is True)
assert(handle(g, UNKNOWN) is True)     # Escape, Home, End and friends are ignored
assert(handle(g, 'q') is False)

# EDGES: a blocked move does not move and turns the character 180 degrees
g = new_game()
g.character.position.y = 0
g.character.face(UP)
assert(g.forward() is False)
assert((g.character.position.x, g.character.position.y) == (CENTER, 0))
assert(g.character.direction == DOWN)
assert(g.character.symbol == 'v')
assert(g.forward() is True)
assert(g.character.position.y == 1)

g = new_game()
g.character.position.y = HEIGHT - 1
g.character.face(DOWN)
assert(g.forward() is False)
assert(g.character.direction == UP)

g = new_game()
g.character.position.x = 0
g.character.face(LEFT)
assert(g.forward() is False)
assert(g.character.direction == RIGHT)

g = new_game()
g.character.position.x = WIDTH - 1
g.character.face(RIGHT)
assert(g.forward() is False)
assert(g.character.direction == LEFT)

# PICKUP: stepping onto the treasure moves it to a blank square
g = new_game()
g.treasure.position.x = CENTER + 1
g.treasure.position.y = CENTER
assert(g.move(RIGHT) is True)
assert((g.character.position.x, g.character.position.y) == (CENTER + 1, CENTER))
assert((g.treasure.position.x, g.treasure.position.y) != (CENTER + 1, CENTER))
assert(max(abs(g.treasure.position.x - (CENTER + 1)),
           abs(g.treasure.position.y - CENTER)) > 1)

# RENDER: one frame, drawn in place, board then tally then controls
g = new_game()
rows = g.board.rows()
assert(len(rows) == HEIGHT)
assert(all(len(row.split()) == WIDTH for row in rows))
assert(rows[CENTER].split()[CENTER] == '^')
assert(rows[g.treasure.position.y].split()[g.treasure.position.x] == 'x')

frame = io.StringIO()
with contextlib.redirect_stdout(frame):
    g.draw()
frame = frame.getvalue()
assert(frame.startswith('\033[H'))                  # homed, so it redraws in place
assert(frame.count('\033[K') == HEIGHT + 2)         # every row wiped to end of line
assert(frame.count('\r\n') == HEIGHT + 1)           # one break between rows
assert(not frame.endswith('\n'))                    # no scroll before the next home
assert('Treasures: 0 of 10' in frame)
assert('q quit' in frame)

# GOAL: the tally counts pickups and the game is won at the goal
g = Game(goal=2)
assert(g.collected == 0)
assert(g.won is False)
g.treasure.position.x = CENTER + 1
g.treasure.position.y = CENTER
g.move(RIGHT)
assert(g.collected == 1)
assert(g.won is False)
g.treasure.position.x = CENTER + 2
g.treasure.position.y = CENTER
g.move(RIGHT)
assert(g.collected == 2)
assert(g.won is True)
assert(g.summary() == 'All 2 treasures found.')
assert(Game(goal=3).summary() == 'Treasures found: 0 of 3.')

# ESCAPES: whole sequences decode, anything else is one ignored key
assert(match_escape((ESCAPE,)) == (None, False))
assert(match_escape((ESCAPE, 91)) == (None, False))
assert(match_escape((ESCAPE, 91, 65)) == ('UP', True))
assert(match_escape((ESCAPE, 91, 66)) == ('DOWN', True))
assert(match_escape((ESCAPE, 91, 67)) == ('RIGHT', True))
assert(match_escape((ESCAPE, 91, 68)) == ('LEFT', True))
assert(match_escape((ESCAPE, 91, 51, 126)) == ('DELETE', True))
assert(match_escape((ESCAPE, 91, 90)) == (None, True))   # ESC [ Z is not mapped
assert(match_escape((ESCAPE, 97)) == (None, True))       # Alt-a is not mapped
assert(set(GET_KEY_MAP.values()) >= {'UP', 'DOWN', 'LEFT', 'RIGHT'})


class FakeScreen:
    """A curses screen that hands out prepared bytes, then nothing."""

    def __init__(self, keys):
        self.keys = list(keys)
        self.timeouts = []

    def getch(self):
        if self.keys:
            return self.keys.pop(0)
        return ERR

    def timeout(self, milliseconds):
        self.timeouts.append(milliseconds)


# READING: arrows come back named, junk is ignored whole, no input is None
screen = FakeScreen([ESCAPE, 91, 65, 107])
assert(read_key(screen) == 'UP')
assert(read_key(screen) == 'k')
assert(screen.timeouts == [ESCAPE_TIMEOUT, -1])

screen = FakeScreen([ESCAPE, 91, 90, 107])               # ESC [ Z, then k
assert(read_key(screen) == UNKNOWN)                      # the whole run is one key
assert(read_key(screen) == 'k')

screen = FakeScreen([ESCAPE, 91, 54, 126])
assert(read_key(screen) == 'PAGE_DOWN')
screen = FakeScreen([ESCAPE, 97, 107])                   # Alt-a, then k
assert(read_key(screen) == UNKNOWN)
assert(read_key(screen) == 'k')
screen = FakeScreen([ESCAPE])                            # ESC on its own
assert(read_key(screen) == UNKNOWN)
assert(screen.timeouts == [ESCAPE_TIMEOUT, -1])          # and blocking is restored

assert(read_key(FakeScreen([])) is None)                 # end of input, not a crash

# POSITIONS: usable as values and readable in a debug print
assert(Position(1, 2) == Position(1, 2))
assert(Position(1, 2) != Position(2, 1))
assert(Position(1, 2) != (1, 2))
assert(len({Position(1, 2), Position(1, 2)}) == 1)
assert(repr(Position(1, 2)) == 'Position(1, 2)')

# SCREENSHOT: docs/demo.gif shows these frames, docs/demo-frames.txt is their text
ROOT = pathlib.Path(__file__).resolve().parent.parent
assert(demo.text_dump() == (ROOT / 'docs' / 'demo-frames.txt').read_text(encoding='utf-8')), \
    'docs/demo-frames.txt is stale - run python3 docs/make_screenshot.py'

drawn = demo.frames()
for frame in drawn:
    assert(len(frame) == 11)
    assert([len(line) for line in frame] == [17] * 9 + [18, 48])


def gif(data):
    """Walk a GIF: (width, height, per-frame details, loops)."""
    assert(data[:6] in (b'GIF87a', b'GIF89a'))
    width, height = int.from_bytes(data[6:8], 'little'), int.from_bytes(data[8:10], 'little')
    flags = data[10]
    at = 13 + (3 * 2 ** ((flags & 0x07) + 1) if flags & 0x80 else 0)
    frames, control, loops = [], None, False
    while at < len(data):
        block = data[at]
        if block == 0x3b:
            break
        if block == 0x21:
            label = data[at + 1]
            at += 2
            if label == 0xf9:
                control = {'delay': int.from_bytes(data[at + 2:at + 4], 'little'),
                           'dispose': (data[at + 1] >> 2) & 0x07,
                           'transparent': bool(data[at + 1] & 0x01)}
            if label == 0xff and data[at + 1:at + 12] == b'NETSCAPE2.0':
                loops = True
        elif block == 0x2c:
            local = data[at + 9]
            at += 10
            if local & 0x80:
                at += 3 * 2 ** ((local & 0x07) + 1)
            frames.append(control)
            at += 1                          # the LZW minimum code size byte
        else:
            raise AssertionError('unexpected GIF block 0x{0:02x} at {1}'.format(block, at))
        while data[at]:                      # skip the data sub-blocks
            at += 1 + data[at]
        at += 1
    return width, height, frames, loops


gif_width, gif_height, gif_frames, gif_loops = gif((ROOT / 'docs' / 'demo.gif').read_bytes())
assert((gif_width, gif_height) == (440, 224))
assert(gif_loops is True)
assert(len(gif_frames) == len(drawn))
assert({frame['delay'] for frame in gif_frames} == {50})     # half a second each
assert(not any(frame['transparent'] for frame in gif_frames)), \
    'the GIF uses transparent-diff frames - viewers disagree about them, so ' \
    'regenerate with make_screenshot.py (palettegen reserve_transparent=0, ' \
    '-gifflags -transdiff)'
