import curses
GET_KEY_MAP = {
	(27,91,51,126) : 'DELETE',
	(27,91,53,126) : 'PAGE_UP',
	(27,91,54,126) : 'PAGE_DOWN',
}
def get_key():
	keys = []
	keys.append( s.getch() )
	if keys[0] == 27:
		keys.append( s.getch() )
		if keys[1] == 91:
			keys.append( s.getch() )
			if keys[2] in range(50,59):
				keys.append( s.getch() )
	keys = tuple(keys)
	if keys in GET_KEY_MAP:
		return GET_KEY_MAP[tuple(keys)]
	else:
		return chr(keys[0])

s = curses.initscr()
curses.noecho()
playing = True

if __name__ == '__main__':
	while playing: 
		k = get_key()
		print(k, end="", flush=True)
		if k == 'q': 
			playing = False
	curses.endwin()

