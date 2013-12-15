from gameobject import GameObject
from texturemanager import TextureManager
from utils import drawRect,debugRect
from rect import Rect

class Button(GameObject):

    FACING_LEFT = 'FACING_LEFT'
    FACING_RIGHT = 'FACING_RIGHT'
    FACING_FORWARD = 'FACING_FORWARD'

    def __init__(self, world):
        super(Button,self).__init__(world)
        self.texSide = TextureManager.get().load('TheButton.png')
        self.texFacing = TextureManager.get().load('ButtonFacing.png')
        self.facing = Button.FACING_FORWARD
        self.attachedTo = None
        self.name = 'button'

    def getRect(self):
        if self.facing == Button.FACING_LEFT:
            return Rect(self.x-8,self.y-8,8,16)
        elif self.facing == Button.FACING_RIGHT:
            return Rect(self.x,self.y-8,8,16)
        elif self.facing == Button.FACING_FORWARD:
            return Rect(self.x-8,self.y-8,16,16)
        assert False

    def spawn(self,spawn):
        super(Button,self).spawn(spawn)
        self.x = spawn.rect.centerX
        self.y = spawn.rect.centerY

    def onMapLoaded(self):
        if 'attachedTo' in self.spawn.properties:
            self.attachedTo = self.world.goMgr.get(self.spawn.properties['attachedTo'])

    def draw(self):
        if self.facing == Button.FACING_LEFT:
            drawRect(self.texSide, self.x, self.y, anchorX=1, anchorY=0.5)
        elif self.facing == Button.FACING_RIGHT:
            drawRect(self.texSide, self.x, self.y, anchorX=1, anchorY=0.5, flipX=True)
        elif self.facing == Button.FACING_FORWARD:
            drawRect(self.texFacing, self.x, self.y, anchorX=0.5, anchorY=0.5)
        else:
            assert False
        # debugRect(self.getRect(), 0,1,0)

    def activate(self):
        print 'BUTTON ACTIVATE'
        if self.attachedTo is not None:
            self.attachedTo.activate()
