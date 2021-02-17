from pilot.lib.position import Position


class Character:
    def __init__(self, x, y):
        self.position = Position(x, y)
        self.direction = 0
        self.symbol = "^"

    def turnRight(self):
        self.direction = (self.direction + 1) % 4