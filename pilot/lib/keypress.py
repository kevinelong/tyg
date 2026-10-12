import curses

from pilot.lib.keys import GET_KEY_MAP, read_key

s = curses.initscr()
curses.noecho()
curses.cbreak()


def get_key(key_map=GET_KEY_MAP, screen=s):
    """Read one keypress from the terminal.

    Returns a mapped name, the character itself, 'ESCAPE' for an escape run
    that is not mapped, or None when there is nothing to read at all.
    """
    return read_key(screen, key_map)


def end_keyboard():
    """Undo the terminal setup above."""
    curses.nocbreak()
    curses.echo()
    curses.endwin()


if __name__ == '__main__':
    playing = True
    while playing:
        key = get_key()
        if key is None:
            playing = False
        else:
            print(key, end="", flush=True)
            if key == 'q':
                playing = False
    end_keyboard()
