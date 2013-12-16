from gameobject import GameObject
from texturemanager import TextureManager
from utils import drawRect, debugPoint
from rect import Rect
from gameobjects.button import Button

# 192x256 = 6x8
class Bridge(GameObject):
    def __init__(self, world):
        super(Bridge, self).__init__(world)
        self.texture = TextureManager.get().load('BridgeUpright.png')

    def draw(self):
        face,x,y = self.getButtonMountInfo()
        debugPoint(x,y,0,1,1)
        drawRect(self.texture, self.x, self.y)

    def onAdded(self):
        self.world.buttonMounts.append(self)

    def getButtonMountRect(self):
        return Rect(self.x+40-8,self.y+213,16,43)

    def getButtonMountInfo(self):
        return (Button.FACING_LEFT, self.x+42,self.y+230)
