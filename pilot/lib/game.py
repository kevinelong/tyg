import sys
from random import randrange

from pilot.lib.board import Board
from pilot.lib.character import Character
from pilot.lib.position import Position
from pilot.lib.treasure import Treasure

HOME = "\033[H"                        # cursor to the top left corner
CLEAR_TO_EOL = "\033[K"                # wipe whatever the last frame left
CONTROLS = "a/d turn  s step  h j k l or arrows move  q quit"


class Game:
    """Board, character and treasure, with blocking, pickups and a goal."""

    def __init__(self, width=9, height=9, goal=10):
        self.board = Board(width, height)
        self.character = Character(width // 2, height // 2)
        self.treasure = Treasure(0, 0)
        self.goal = goal
        self.collected = 0
        self.board.add_item(self.character)
        self.board.add_item(self.treasure)
        self.move_treasure()

    @property
    def won(self):
        return self.collected >= self.goal

    def summary(self):
        """The closing line: the goal if it was reached, else the tally."""
        if self.won:
            return "All {0} treasures found.".format(self.goal)
        return "Treasures found: {0} of {1}.".format(self.collected, self.goal)

    def draw(self, stream=None):
        """Redraw the whole frame in place: board, tally, then controls.

        The frame goes home first and leaves the cursor at the end of its last
        line, so a redraw overwrites the previous one instead of scrolling.
        """
        stream = stream or sys.stdout
        rows = self.board.rows()
        rows.append("Treasures: {0} of {1}".format(self.collected, self.goal))
        rows.append(CONTROLS)
        stream.write(HOME + "".join(row + CLEAR_TO_EOL + "\r\n" for row in rows[:-1])
                     + rows[-1] + CLEAR_TO_EOL)
        stream.flush()

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
            self.collected += 1
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
