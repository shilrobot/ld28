

class GameObject(object):

	def __init__(self, world):
		self.x = 0
		self.y = 0
		self.world = world
		self.engine = world.engine

	def draw(self):
		pass

	def update(self, delta):
		pass

	def spawn(self, spawn):
		self.x = spawn.x
		self.y = spawn.y
