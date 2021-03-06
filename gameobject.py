

class GameObject(object):

	PRIORITY_BELOW_FG = 0
	PRIORITY_FG = 50
	PRIORITY_BELOW_PLAYER = 100
	PRIORITY_BUTTON = 150
	PRIORITY_PLAYER = 200
	PRIORITY_ABOVE_PLAYER = 300

	def __init__(self, world):
		global serialNumberGenerator
		self.x = 0
		self.y = 0
		self.world = world
		self.engine = world.engine
		self.priority = GameObject.PRIORITY_BELOW_PLAYER
		self.visible = True
		self.index = -1
		self.name = None

	def draw(self):
		pass

	def update(self, delta):
		pass

	def spawn(self, spawn):
		self.spawn = spawn
		self.name = spawn.name
		self.x = spawn.x
		self.y = spawn.y

	def onMapLoaded(self):
		pass

	def onAdded(self):
		pass

	def onRemoving(self):
		pass

	def onRemoved(self):
		pass

	def activate(self):
		pass