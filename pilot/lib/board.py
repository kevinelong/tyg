class Board:

    def __init__(self, width=9, height=9):
        self.width = width
        self.height = height
        self.content = []

    def add_item(self, item):
        self.content.append(item)

    def symbol_at(self, x, y):
        symbol = "."
        for item in self.content:
            if item.position.x == x and item.position.y == y:
                symbol = item.symbol
        return symbol

    def rows(self):
        """The board as one printable row per y, top row first."""
        return [" ".join(self.symbol_at(x, y) for x in range(self.width))
                for y in range(self.height)]
