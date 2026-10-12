"""Play the game in a terminal.

Run from the repository root: python3 -m pilot.main
"""
from pilot.lib.controls import handle
from pilot.lib.game import Game
from pilot.lib.keypress import end_keyboard, get_key


def play(game):
    """Draw, read one key, act on it, until the player quits or wins."""
    while True:
        game.draw()
        key = get_key()
        if key is None:
            break
        if not handle(game, key):
            break
        if game.won:
            game.draw()
            break
    return game


if __name__ == '__main__':
    game = Game()
    try:
        play(game)
    finally:
        end_keyboard()
    print()
    print(game.summary())
