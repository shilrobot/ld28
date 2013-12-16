from gameobject import GameObject
from texturemanager import TextureManager
from utils import drawRect, lerp
from rect import Rect

STATE_STILL = 1
STATE_OPENING = 2

DOOR_OPEN_TIME = 0.5

MAX_ACTIVATES = 6

class BustedDoor(GameObject):
    def __init__(self, world):
        super(BustedDoor,self).__init__(world)
        self.texture = TextureManager.get().load('Door.png')
        self.priority = GameObject.PRIORITY_BELOW_FG
        self.state = STATE_STILL
        self.animTime = 0        
        self.activates = 0

    def spawn(self,spawn):
        super(BustedDoor,self).spawn(spawn)
        self.targetY = self.y - 64*0.8

    def draw(self):
        drawRect(self.texture, self.x, self.y)

    def onAdded(self):
        print 'BustedDoor.onAdded'
        self.world.blockers.append(self)

    def update(self, delta):
        if self.state == STATE_OPENING:
            self.animTime += delta
            self.y = lerp(self.animStartY, self.animEndY, self.animTime/DOOR_OPEN_TIME)
            if self.animTime >= DOOR_OPEN_TIME:
                self.state = STATE_STILL
                self.y = self.animEndY

    def activate(self):
        print 'BUSTED DOOR ACTIVATE'
        if self.activates < MAX_ACTIVATES:
            self.activates += 1
            if self.activates >= MAX_ACTIVATES:
                self.world.goMgr.get('button').popOff()
                return
        if self.state == STATE_STILL:
            self.animStartY = self.y
            self.animEndY = (self.y + self.targetY)*0.5
            self.animTime = 0
            self.state = STATE_OPENING

    def rectOverlaps(self, rect):
        # player collision test
        r = Rect(self.x,self.y,32,64)
        return r.intersects(rect)
