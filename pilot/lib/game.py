from pilot.lib.board import Board
from pilot.lib.character import Character
from pilot.lib.treasure import Treasure
from pilot.lib.board import Board


class Game:
    def __init__(self, width=9, height=9):
        self.board = Board(width, height)
        self.character = Character(width // 2, height // 2)
        self.treasure = Treasure(2, 2)
        self.board.add_item(self.treasure)
        self.board.add_item(self.character)

    def draw(self):
        self.board.draw()
