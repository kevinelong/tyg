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
"""
from video_game import Game

# Tests
g = Game()
assert(g is not None)
assert(g.board.width == 9)
assert(g.board.height == 9)
assert(g.character.position.x == 4)
assert(g.character.position.y == 4)
assert(g.treasure.position.x != 4)
assert(g.treasure.position.y != 4)
assert(g.treasure.position.x >= 0)
assert(g.treasure.position.x <= 8)
assert(g.treasure.position.y >= 0)
assert(g.treasure.position.y <= 8)
assert(g.treasure.position.x != 4)
assert(g.treasure.position.y != 4)
assert(g.character.direction == 0)
g.character.turnRight()
assert(g.character.direction == 1)
g.character.turnRight()
g.character.turnRight()
g.character.turnRight()
assert(g.character.direction == 0)
