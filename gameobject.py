

class GameObject(object):

	PRIORITY_BELOW_PLAYER = 100
	PRIORITY_PLAYER = 200
	PRIORITY_ABOVE_PLAYER = 300

	def __init__(self, world):
		global serialNumberGenerator
		self.x = 0
		self.y = 0
		self.world = world
		self.engine = world.engine
		self.priority = GameObject.PRIORITY_BELOW_PLAYER

	def draw(self):
		pass

	def update(self, delta):
		pass

	def spawn(self, spawn):
		self.x = spawn.x
		self.y = spawn.y

