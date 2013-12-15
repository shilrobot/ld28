from gameobject import GameObject
from texturemanager import TextureManager
from utils import drawRect

class Oak(GameObject):
    def __init__(self, world):
        GameObject.__init__(self,world)
        self.texture = TextureManager.get().load('OakTree.png')

    def spawn(self,spawn):
        self.x = spawn.rect.centerX
        self.y = spawn.rect.bottom - 1

    def draw(self):
        drawRect(self.texture, self.x, self.y+1, anchorX=0.5, anchorY=1, scale=2)
