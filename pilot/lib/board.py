class Board:

    def __init__(self, width=9, height=9):
        self.width = width
        self.height = height
        self.content = []

    def add_item(self, item):
        self.content.append(item)

    def draw(self):
        for y in range(0, self.height):
            for x in range(0, self.width):
                symbol = "."
                for item in self.content:
                    if item.position.x == x and item.position.y == y:
                        symbol = item.symbol
                print(symbol, end=" ")
            print("", end="\r\n")