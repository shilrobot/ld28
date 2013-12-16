from gameobject import GameObject
from texturemanager import TextureManager
from utils import drawRect,debugRect,sweepMovement
from rect import Rect

STATE_ATTACHED = 1
STATE_UNATTACHED = 2
STATE_HELD = 3

GRAVITY_ACCEL = 1500
TERMINAL_VELOCITY = 1000

class Button(GameObject):

    FACING_LEFT = 'FACING_LEFT'
    FACING_RIGHT = 'FACING_RIGHT'
    FACING_FORWARD = 'FACING_FORWARD'

    def __init__(self, world):
        super(Button,self).__init__(world)
        self.texSide = TextureManager.get().load('TheButton.png')
        self.texFacing = TextureManager.get().load('ButtonFacing.png')
        self.facing = Button.FACING_FORWARD
        self.state = STATE_UNATTACHED
        self.attachedTo = None
        self.name = 'button'
        self.vy = 0

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
            attachTo = self.world.goMgr.get(self.spawn.properties['attachedTo'])
            if attachTo is not None:
                self.attachTo(attachTo)

    def draw(self):
        #debugRect(self.getRect(), 0,1,1)

        if self.state == STATE_HELD:
            return

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
        if self.state == STATE_ATTACHED:
            self.attachedTo.activate()

    def becomeHeld(self):
        self.state = STATE_HELD
        self.facing = Button.FACING_FORWARD

    def isOnGround(self):
        return sweepMovement(self.world, self.getRect(), 0, 0.5)[0]

    def update(self, delta):
        if self.state == STATE_UNATTACHED:
            self.vy += GRAVITY_ACCEL * delta
            collided, mx, my = sweepMovement(self.world, self.getRect(), 0, self.vy*delta)
            self.x += mx
            self.y += my
            if collided:
                self.vy = 0

    def popOff(self):
        self.state = STATE_UNATTACHED
        self.attachedTo = None
        self.vy = 0

    def isHeld(self):
        return self.state == STATE_HELD

    def attachTo(self, attachTo):
        if attachTo is not None:
            self.state = STATE_ATTACHED
            self.facing,self.x,self.y = attachTo.getButtonMountInfo()
            self.attachedTo = attachTo
