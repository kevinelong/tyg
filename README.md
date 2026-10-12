# tyg

![tyg running in a terminal: a 9x9 board of dots with the character ^ at the centre and the treasure x at (6, 1), and under it the lines "Treasures: 0 of 10" and "a/d turn  s step  h j k l or arrows move  q quit". The animation walks the character up and right to the treasure, turns it in place, steps it forward, and bumps it into the top edge, where it turns 180 degrees.](docs/demo.svg)

A small terminal game: a 9x9 board, a character you turn and walk, and a
treasure that moves to a new square whenever you step on it. The character
shows which way it faces as `^ > v <`. Collect ten treasures to win.

## Run

Needs Python 3 with `curses` (Linux, macOS or WSL - not native Windows) and a
real terminal. `pilot` is a package, so run it as a module from the repository
root, not as `python3 pilot/main.py`:

    python3 -m pilot.main

## Keys

| Key | Action |
| --- | --- |
| `a` / `d` | turn left / right on the spot |
| `s` | step straight ahead |
| `h` `j` `k` `l` | move left / down / up / right |
| arrow keys | move left / down / up / right |
| `q` | quit |

The board, the tally and the controls line are redrawn in place each turn.
Walking off the edge of the board is blocked and turns you 180 degrees.
Escape sequences the game does not use (Home, End, function keys) are read
whole and ignored, and running out of input quits cleanly with the tally.

## Test

    python3 -m pilot.test

## Screenshot

`docs/demo.svg` is the animation above and `docs/demo-frames.txt` is the text
of its frames, both generated from the game's own output by

    python3 docs/make_screenshot.py       # needs nothing but Python

Vector text, so it stays crisp at any zoom and carries no image codec, and the
frames are plain text so a diff shows exactly what changed. `python3 -m
pilot.test` regenerates the SVG and fails unless it matches the committed file
byte for byte, so the picture cannot drift from the program.

## Licence

Functional Source License 1.1, MIT future licence - see LICENSE.md.
