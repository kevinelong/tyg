import curses

GET_KEY_MAP = {
    (27, 91, 65): 'UP',
    (27, 91, 66): 'DOWN',
    (27, 91, 67): 'RIGHT',
    (27, 91, 68): 'LEFT',
    (27, 91, 51, 126): 'DELETE',
    (27, 91, 53, 126): 'PAGE_UP',
    (27, 91, 54, 126): 'PAGE_DOWN',
}


def get_key(key_map=GET_KEY_MAP):
    keys = []
    keys.append(s.getch())
    if keys[0] == 27:
        keys.append(s.getch())
        if keys[1] == 91:
            keys.append(s.getch())
            if keys[2] in range(50, 59):
                keys.append(s.getch())
    keys = tuple(keys)
    if keys in key_map:
        return key_map[keys]
    else:
        return chr(keys[0])


def end_keyboard():
    """Undo the terminal setup below."""
    curses.nocbreak()
    curses.echo()
    curses.endwin()


s = curses.initscr()
curses.noecho()
curses.cbreak()

if __name__ == '__main__':
    playing = True
    while playing:
        k = get_key()
        print(k, end="", flush=True)
        if k == 'q':
            playing = False
    end_keyboard()
