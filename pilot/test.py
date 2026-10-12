"""
Requirements:
SETUP:
1. Show Map of specified width and height, default to 9x9.
2. Show Character center of the Map.
3. Place and show a treasure on the map in random position that is not next to or on the player.

TURN:
4. Ask user to if the they want to turn A--rotate-left, D--Rotate-Right or S-MOve-straight.
5. Rotate or move character Move character in specified direction
6. Block moves that would go off the map. If blocked then turn 180 degrees.
7. if player and treasure collide then remove treasure and add a new one in a blank square.
8. Arrow keys and HJKL also move: each one faces and steps a square in the
   direction pressed. Any other key is ignored, and Q quits.

Run from the repository root: python3 -m pilot.test
"""
from pilot.lib.character import DOWN, LEFT, RIGHT, UP
from pilot.lib.controls import handle
from pilot.lib.game import Game

WIDTH = HEIGHT = 9
CENTER = WIDTH // 2


def new_game():
    """A game with the treasure parked in a corner, out of the way."""
    game = Game()
    game.treasure.position.x = 0
    game.treasure.position.y = 0
    return game


# SETUP
g = Game()
assert(g is not None)
assert(g.board.width == WIDTH)
assert(g.board.height == HEIGHT)
assert(g.character.position.x == CENTER)
assert(g.character.position.y == CENTER)
assert(0 <= g.treasure.position.x <= WIDTH - 1)
assert(0 <= g.treasure.position.y <= HEIGHT - 1)
assert(max(abs(g.treasure.position.x - CENTER),
           abs(g.treasure.position.y - CENTER)) > 1)

# FACING: direction 0..3 renders as ^ > v < clockwise
assert(g.character.direction == UP)
assert(g.character.symbol == '^')
g.character.turnRight()
assert(g.character.direction == RIGHT)
assert(g.character.symbol == '>')
g.character.turnRight()
assert(g.character.direction == DOWN)
assert(g.character.symbol == 'v')
g.character.turnRight()
assert(g.character.direction == LEFT)
assert(g.character.symbol == '<')
g.character.turnRight()
assert(g.character.direction == UP)
assert(g.character.symbol == '^')
g.character.turnLeft()
assert(g.character.direction == LEFT)
g.character.turnRight()
assert(g.character.direction == UP)
g.character.turnRight()
g.character.turnRight()
g.character.turnRight()
g.character.turnRight()
assert(g.character.direction == UP)

# KEYS: a and d turn, s steps forward
g = new_game()
assert(handle(g, 'a') is True)
assert(g.character.direction == LEFT)
assert(handle(g, 'd') is True)
assert(g.character.direction == UP)
assert(handle(g, 'd') is True)
assert(g.character.direction == RIGHT)
assert(handle(g, 's') is True)
assert((g.character.position.x, g.character.position.y) == (CENTER + 1, CENTER))

# KEYS: arrows and hjkl face and step one square
g = new_game()
assert(handle(g, 'h') is True)
assert((g.character.position.x, g.character.position.y) == (CENTER - 1, CENTER))
assert(g.character.symbol == '<')
assert(handle(g, 'j') is True)
assert((g.character.position.x, g.character.position.y) == (CENTER - 1, CENTER + 1))
assert(g.character.symbol == 'v')
assert(handle(g, 'k') is True)
assert((g.character.position.x, g.character.position.y) == (CENTER - 1, CENTER))
assert(g.character.symbol == '^')
assert(handle(g, 'l') is True)
assert((g.character.position.x, g.character.position.y) == (CENTER, CENTER))
assert(g.character.symbol == '>')
assert(handle(g, 'LEFT') is True)
assert((g.character.position.x, g.character.position.y) == (CENTER - 1, CENTER))
assert(handle(g, 'UP') is True)
assert((g.character.position.x, g.character.position.y) == (CENTER - 1, CENTER - 1))
assert(handle(g, 'DOWN') is True)
assert(handle(g, 'RIGHT') is True)
assert((g.character.position.x, g.character.position.y) == (CENTER, CENTER))
assert(handle(g, 'z') is True)
assert(handle(g, 'q') is False)

# EDGES: a blocked move does not move and turns the character 180 degrees
g = new_game()
g.character.position.y = 0
g.character.face(UP)
assert(g.forward() is False)
assert((g.character.position.x, g.character.position.y) == (CENTER, 0))
assert(g.character.direction == DOWN)
assert(g.character.symbol == 'v')
assert(g.forward() is True)
assert(g.character.position.y == 1)

g = new_game()
g.character.position.y = HEIGHT - 1
g.character.face(DOWN)
assert(g.forward() is False)
assert(g.character.direction == UP)

g = new_game()
g.character.position.x = 0
g.character.face(LEFT)
assert(g.forward() is False)
assert(g.character.direction == RIGHT)

g = new_game()
g.character.position.x = WIDTH - 1
g.character.face(RIGHT)
assert(g.forward() is False)
assert(g.character.direction == LEFT)

# PICKUP: stepping onto the treasure moves it to a blank square
g = new_game()
g.treasure.position.x = CENTER + 1
g.treasure.position.y = CENTER
assert(g.move(RIGHT) is True)
assert((g.character.position.x, g.character.position.y) == (CENTER + 1, CENTER))
assert((g.treasure.position.x, g.treasure.position.y) != (CENTER + 1, CENTER))
assert(max(abs(g.treasure.position.x - (CENTER + 1)),
           abs(g.treasure.position.y - CENTER)) > 1)
