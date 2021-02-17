from pilot.lib.game import Game
from pilot.lib.keypress import get_key
from pilot.lib.repeat import forever

g = Game()
GET_KEY_MAP = {
    (27, 91, 51, 126): 'DELETE',
    (27, 91, 53, 126): 'PAGE_UP',
    (27, 91, 54, 126): 'PAGE_DOWN',
}


def play():
    print(g.board.content[0].position.y)
    g.draw()
    k = get_key(GET_KEY_MAP)
    print(k)
    if 'q' == k:
        raise


forever(play)