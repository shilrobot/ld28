from gameobject import GameObject
from texturemanager import TextureManager
from utils import drawRect

FRAME_LENGTH = 30/60.0

class Willow(GameObject):
    def __init__(self, world):
        GameObject.__init__(self,world)
        self.texture = TextureManager.get().load('WillowTree.png')
        self.textureWind1 = TextureManager.get().load('WindyWillow1.png')
        self.textureWind2 = TextureManager.get().load('WindyWillow2.png')
        self.animTime = 0

    def spawn(self,spawn):
        super(Willow,self).spawn(spawn)
        self.x = spawn.rect.centerX
        self.y = spawn.rect.bottom - 1

    def update(self, delta):
        self.animTime += delta
        self.animTime = self.animTime % (FRAME_LENGTH*2)

    def draw(self):
        if self.animTime < FRAME_LENGTH:
            frame = self.textureWind1
        else:
            frame = self.textureWind2
        drawRect(frame, self.x, self.y+1, anchorX=0.5, anchorY=1, scale=2)
