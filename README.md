# tyg

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

## Licence

Functional Source License 1.1, MIT future licence - see LICENSE.md.
