from gameobject import GameObject
from texturemanager import TextureManager
from utils import drawRect

class Oak(GameObject):
	def __init__(self, world):
		GameObject.__init__(self,world)
		self.texture = TextureManager.get().load('OakTree.png')

	def draw(self):
		drawRect(self.texture, self.x, self.y)