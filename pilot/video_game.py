from keypress import get_key

class Board:
	
	def __init__(self, width = 9, height = 9 ):
		self.width = width
		self.height = height
		self.content = []

	def addItem(self, item):
		self.content.append(item)

	def draw(self):
		for y in range(0, self.height):
			for x in range(0, self.width):
				symbol = "."
				for item in self.content:
					if item.position.x == x and item.position.y == y:
						symbol = item.symbol			
				print(symbol,end=" ")
			print("", end="\r\n")

				
class Position():
	def __init__(self, x, y):
		self.x = x
		self.y = y

class Character:
	def __init__(self, x, y):
		self.position = Position(x,y)
		self.direction = 0
		self.symbol = "^"

	def turnRight(self):
		self.direction = (self.direction + 1) % 4


class Treasure:
	def __init__(self, x, y):
		self.position = Position(x,y)
		self.symbol = "x"

class Game:
	def __init__(self, width = 9, height = 9):
		self.board = Board(width, height)
		self.character = Character(width//2, height//2)
		self.treasure = Treasure(2,2)
		self.board.addItem(self.treasure)
		self.board.addItem(self.character)

	def draw(self):
		self.board.draw()

if __name__ == '__main__':
	g = Game()
	playing = True
	while playing:
		print(g.board.content[0].position.y)
		g.draw()
		k = get_key()
		if 'q' == k:
			playing = False
