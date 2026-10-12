from random import randrange

from pilot.lib.board import Board
from pilot.lib.character import Character
from pilot.lib.position import Position
from pilot.lib.treasure import Treasure


class Game:
    """Board, character and treasure, with blocking and pickups."""

    def __init__(self, width=9, height=9):
        self.board = Board(width, height)
        self.character = Character(width // 2, height // 2)
        self.treasure = Treasure(0, 0)
        self.board.add_item(self.character)
        self.board.add_item(self.treasure)
        self.move_treasure()

    def draw(self):
        self.board.draw()

    def turn(self, quarters):
        self.character.turn(quarters)

    def forward(self):
        """Step where the character already faces (S)."""
        return self.step(self.character.direction)

    def move(self, direction):
        """Face a direction and step into it (arrow keys and hjkl)."""
        self.character.face(direction)
        return self.step(direction)

    def step(self, direction):
        """Take one step: off the map it is blocked and turns the character 180."""
        target = self.character.ahead()
        if not self.inside(target):
            self.character.turnAround()
            return False
        self.character.position = target
        if self.character.position == self.treasure.position:
            self.move_treasure()
        return True

    def inside(self, position):
        return 0 <= position.x < self.board.width and 0 <= position.y < self.board.height

    def move_treasure(self):
        """Send the treasure to a random blank square clear of the character."""
        self.treasure.position = self.blank_position()

    def blank_position(self):
        character = self.character.position
        squares = [
            (x, y)
            for x in range(self.board.width)
            for y in range(self.board.height)
            if max(abs(x - character.x), abs(y - character.y)) > 1
        ]
        if not squares:
            raise ValueError("board has no blank square for the treasure")
        x, y = squares[randrange(len(squares))]
        return Position(x, y)
