"""Play the game in a terminal.

Run from the repository root: python3 -m pilot.main
"""
from pilot.lib.controls import handle
from pilot.lib.game import Game
from pilot.lib.keypress import end_keyboard, get_key


def play(game):
    """Draw, read one key, act on it, until the player quits."""
    while True:
        game.draw()
        if not handle(game, get_key()):
            return game


if __name__ == '__main__':
    try:
        play(Game())
    finally:
        end_keyboard()
