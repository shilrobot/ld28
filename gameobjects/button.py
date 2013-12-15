from gameobject import GameObject
from texturemanager import TextureManager
from utils import drawRect

class Button(GameObject):

    FACING_LEFT = 'FACING_LEFT'
    FACING_RIGHT = 'FACING_RIGHT'
    FACING_FORWARD = 'FACING_FORWARD'

    def __init__(self, world):
        print 'BUTTON'
        super(Button,self).__init__(world)
        self.texSide = TextureManager.get().load('TheButton.png')
        self.texFacing = TextureManager.get().load('ButtonFacing.png')
        self.facing = Button.FACING_FORWARD
        self.attachedTo = None
        self.name = 'button'

    def spawn(self,spawn):
        super(Button,self).spawn(spawn)
        self.x = spawn.rect.centerX
        self.y = spawn.rect.centerY

    def draw(self):
        if self.facing == Button.FACING_LEFT:
            drawRect(self.texSide, self.x, self.y, anchorX=1, anchorY=0.5)
        elif self.facing == Button.FACING_RIGHT:
            drawRect(self.texSide, self.x, self.y, anchorX=1, anchorY=0.5, flipX=True)
        elif self.facing == Button.FACING_FORWARD:
            drawRect(self.texFacing, self.x, self.y, anchorX=0.5, anchorY=0.5)
