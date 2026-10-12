from pilot.lib.character import DOWN, LEFT, RIGHT, UP

TURN_KEYS = {'a': -1, 'd': 1}

MOVE_KEYS = {
    'k': UP,
    'l': RIGHT,
    'j': DOWN,
    'h': LEFT,
    'UP': UP,
    'RIGHT': RIGHT,
    'DOWN': DOWN,
    'LEFT': LEFT,
}


def handle(game, key):
    """Apply one keypress to the game; return False when the player quits.

    a and d turn on the spot, s steps straight ahead, and the arrow keys and
    hjkl face and step one square in the direction pressed. Any other key is
    ignored.
    """
    if key == 'q':
        return False
    if key in TURN_KEYS:
        game.turn(TURN_KEYS[key])
    elif key == 's':
        game.forward()
    elif key in MOVE_KEYS:
        game.move(MOVE_KEYS[key])
    return True
