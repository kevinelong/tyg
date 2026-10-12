"""Key decoding, independent of the terminal library.

A screen is anything with curses' two methods: getch() returning the next byte
or ERR, and timeout(ms) setting how long getch waits for the rest of an escape
sequence. keypress.py binds a real curses screen; the tests use a fake one.
"""

ERR = -1
ESCAPE = 27
ESCAPE_TIMEOUT = 25          # ms to wait for the rest of an escape sequence
UNKNOWN = 'ESCAPE'           # an escape run that is not in the map

GET_KEY_MAP = {
    (27, 91, 65): 'UP',
    (27, 91, 66): 'DOWN',
    (27, 91, 67): 'RIGHT',
    (27, 91, 68): 'LEFT',
    (27, 91, 51, 126): 'DELETE',
    (27, 91, 53, 126): 'PAGE_UP',
    (27, 91, 54, 126): 'PAGE_DOWN',
}


def match_escape(keys, key_map=GET_KEY_MAP):
    """Decode the bytes read since an ESC.

    keys is the escape byte plus every byte read after it. Returns
    (name, done): the name when keys is a whole entry of key_map, else
    (None, False) to read another byte, or (None, True) when no entry of
    key_map can match any more and the run should be dropped as one key.
    """
    keys = tuple(keys)
    if keys in key_map:
        return key_map[keys], True
    if any(entry[:len(keys)] == keys for entry in key_map):
        return None, False
    return None, True


def read_key(screen, key_map=GET_KEY_MAP):
    """Read one keypress.

    Returns the name of a mapped escape sequence, the character itself,
    UNKNOWN for an escape run that is not mapped, or None when the screen has
    nothing to read at all (end of input or a hangup).
    """
    first = screen.getch()
    if first == ERR:
        return None
    if first != ESCAPE:
        return chr(first)
    return read_escape(screen, key_map)


def read_escape(screen, key_map=GET_KEY_MAP):
    """Read and name the rest of an escape sequence, ESC on its own included."""
    keys = [ESCAPE]
    longest = max(len(entry) for entry in key_map)
    screen.timeout(ESCAPE_TIMEOUT)
    try:
        while len(keys) < longest:
            key = screen.getch()
            if key == ERR:
                break
            keys.append(key)
            name, done = match_escape(keys, key_map)
            if done:
                return name or UNKNOWN
    finally:
        screen.timeout(-1)
    return UNKNOWN
