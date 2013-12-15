from rect import Rect
from texturemanager import TextureManager
import pygame
from utils import drawRect, debugRect

class Player:
    def __init__(self, world):
        self.world = world
        self.engine = self.world.engine
        self.texture = TextureManager.get().load('player.png')
        self.x = 7*32
        self.y = 13*32 - 2
        self.faceRight = True

    def getRect(self,x,y):
        return Rect(x-8, y-60, 16,60)

    def update(self, delta):
        speed = 300
        dx = 0
        if self.engine.key_down(pygame.K_LEFT):
            dx -= speed*delta
            self.faceRight = False
        if self.engine.key_down(pygame.K_RIGHT):
            dx += speed*delta
            self.faceRight = True

        self.move(dx,0)

    def move(self, dx, dy):
        map = self.world.map
        startRect = self.getRect(self.x,self.y)
        endRect = self.getRect(self.x+dx,self.y+dy)
        merged = startRect.mergedCopy(endRect)
        print startRect, endRect, merged

        if not map.rectOverlaps(merged):
            self.x += dx
            self.y += dy
            return

    def draw(self):
        #print 'draw %f,%f' % (self.x, self.y)
        drawRect(self.texture, self.x, self.y, anchorX=0.5, anchorY=1, flipX=not self.faceRight)
        debugRect(self.getRect(self.x,self.y), 1,0,0)
