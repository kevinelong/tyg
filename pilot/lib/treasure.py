from pilot.lib.position import Position


class Treasure:
    def __init__(self, x, y):
        self.position = Position(x, y)
        self.symbol = "x"