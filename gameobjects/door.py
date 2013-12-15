from gameobject import GameObject
from texturemanager import TextureManager
from utils import drawRect
from rect import Rect

STATE_CLOSED = 1
STATE_OPENING = 2
STATE_OPEN = 3

DOOR_OPEN_TIME = 2.0

class Door(GameObject):
    def __init__(self, world):
        super(Door,self).__init__(world)
        self.texture = TextureManager.get().load('Door.png')
        self.priority = GameObject.PRIORITY_BELOW_FG
        self.state = STATE_CLOSED
        self.startY = 0
        self.animTime = 0        

    def spawn(self,spawn):
        super(Door,self).spawn(spawn)
        self.startY = self.y

    def draw(self):

        drawRect(self.texture, self.x, self.y)

    def onAdded(self):
        print 'Door.onAdded'
        self.world.blockers.append(self)

    def update(self, delta):
        if self.state == STATE_OPENING:
            self.animTime += delta
            if self.animTime >= DOOR_OPEN_TIME:
                self.animTime = DOOR_OPEN_TIME
                self.state = STATE_OPEN

        if self.state == STATE_CLOSED:
            self.y = self.startY
        if self.state == STATE_OPENING:
            self.y = self.startY - 64*self.animTime / DOOR_OPEN_TIME
        elif self.state == STATE_OPEN:
            self.y = self.startY - 64

    def activate(self):
        print 'DOOR ACTIVATE'
        if self.state == STATE_CLOSED:
            self.state = STATE_OPENING

    def rectOverlaps(self, rect):
        r = Rect(self.x,self.y,32,64)
        return r.intersects(rect)