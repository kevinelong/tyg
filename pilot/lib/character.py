from pilot.lib.position import Position

UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3


class Character:
    """A one-cell actor facing one of four compass directions.

    A direction is an index into SYMBOLS, clockwise from UP, so
    (direction + 1) % 4 is a right turn and SYMBOLS[direction] is the glyph
    that shows which way the character faces. The glyph is derived from the
    direction, never stored beside it, so a turn always shows on the board.
    """

    SYMBOLS = "^>v<"
    DIRECTIONS = ((0, -1), (1, 0), (0, 1), (-1, 0))

    def __init__(self, x, y, direction=UP):
        self.position = Position(x, y)
        self.direction = direction % len(self.SYMBOLS)

    @property
    def symbol(self):
        return self.SYMBOLS[self.direction]

    def face(self, direction):
        self.direction = direction % len(self.SYMBOLS)

    def turn(self, quarters):
        """Turn one quarter turn per unit, negative to the left."""
        self.direction = (self.direction + quarters) % len(self.SYMBOLS)

    def turnRight(self):
        self.turn(1)

    def turnLeft(self):
        self.turn(-1)

    def turnAround(self):
        self.turn(2)

    def ahead(self):
        """The position one step in front, without moving."""
        dx, dy = self.DIRECTIONS[self.direction]
        return Position(self.position.x + dx, self.position.y + dy)
