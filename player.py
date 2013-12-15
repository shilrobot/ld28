from rect import Rect
from texturemanager import TextureManager
import pygame
from utils import drawRect

class Player:
    def __init__(self, world):
        self.world = world
        self.engine = self.world.engine
        self.texture = TextureManager.get().load('player.png')
        self.x = 7*32
        self.y = 13*32
        self.faceRight = True

    def update(self, delta):
        speed = 300
        if self.engine.key_down(pygame.K_LEFT):
            self.x -= speed*delta
            self.faceRight = False
        if self.engine.key_down(pygame.K_RIGHT):
            self.x += speed*delta
            self.faceRight = True

    def draw(self):
        #print 'draw %f,%f' % (self.x, self.y)
        drawRect(self.texture, self.x, self.y, anchorX=0.5, anchorY=1, flipX=not self.faceRight)
