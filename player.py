from rect import Rect
from texturemanager import TextureManager
import pygame
from utils import drawRect, debugRect

WALK_SPEED = 300.0
ANIM_STAND = 0
ANIM_WALK = 1
GRAVITY_ACCEL = 1000
TERMINAL_VELOCITY = 1000

WALK_FRAME_TIME = 10/60.0

class Player:
    def __init__(self, world):
        self.world = world
        self.engine = self.world.engine
        self.texStand = TextureManager.get().load('player.png')
        self.texWalk1 = TextureManager.get().load('playerwalk1.png')
        self.texWalk2 = TextureManager.get().load('playerwalk2.png')
        self.anim = ANIM_STAND
        self.animTime = 0
        self.x = 7*32
        self.y = 13*32 - 2
        self.faceRight = True
        self.vy = 0.0

    def getRect(self,x,y):
        return Rect(x-8, y-60, 16,60)

    def update(self, delta):
        dx = 0
        moving = False

        if self.engine.key_down(pygame.K_LEFT):
            dx -= WALK_SPEED*delta
            self.faceRight = False
            moving = True
        if self.engine.key_down(pygame.K_RIGHT):
            dx += WALK_SPEED*delta
            self.faceRight = True
            moving = True

        self.move(dx,0)

        self.vy += GRAVITY_ACCEL*delta
        if self.vy > TERMINAL_VELOCITY:
            self.vy = TERMINAL_VELOCITY
        collidedMovingDown = self.move(0,self.vy*delta)
        if collidedMovingDown:
            self.vy = 0

        # Update animations

        if moving:
            if self.anim != ANIM_WALK:
                self.anim = ANIM_WALK
                self.animTime = 0
        else:
            self.anim = ANIM_STAND
            self.animTime = 0

        if self.anim == ANIM_WALK:
            self.animTime += delta
            self.animTime = self.animTime % (WALK_FRAME_TIME*2)

    def move(self, dx, dy):
        map = self.world.map
        startRect = self.getRect(self.x,self.y)
        endRect = self.getRect(self.x+dx,self.y+dy)
        merged = startRect.mergedCopy(endRect)

        if not map.rectOverlaps(merged):
            self.x += dx
            self.y += dy
            return False

        minT = 0
        maxT = 1
        for n in range(10):
            testT = (minT+maxT)*0.5
            if map.rectOverlaps(self.getRect(self.x+dx*testT,self.y+dy*testT)):
                maxT = testT
            else:
                minT = testT

        self.x += dx*minT
        self.y += dy*minT
        return minT < 1

    def draw(self):
        #print 'draw %f,%f' % (self.x, self.y)

        if self.anim == ANIM_STAND:
            tex = self.texStand
        elif self.anim == ANIM_WALK:
            if self.animTime < WALK_FRAME_TIME:
                tex = self.texWalk1
            else:
                tex = self.texWalk2

        drawRect(tex, self.x, self.y, anchorX=0.5, anchorY=1, flipX=not self.faceRight)
        #debugRect(self.getRect(self.x,self.y), 1,0,0)
