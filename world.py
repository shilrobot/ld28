from tilemap import Tilemap
from engine import Engine
import pygame
from OpenGL.GL import *
from rect import Rect
from player import Player

class World:

    def __init__(self):
        self.engine = Engine.get()
        self.scrollX = 0
        self.scrollY = 0
        self.map = Tilemap('test')
        self.player = Player(self)

    def update(self, delta):

        if self.engine.key_down(pygame.K_s):
            delta *= 0.25
        elif self.engine.key_down(pygame.K_f):
            delta *= 4
        self.player.update(delta)
        # scrollSpeed = 300

        # if self.engine.key_down(pygame.K_LEFT):
        #     self.scrollX -= scrollSpeed * delta
        # if self.engine.key_down(pygame.K_RIGHT):
        #     self.scrollX += scrollSpeed * delta
        # if self.engine.key_down(pygame.K_UP):
        #     self.scrollY -= scrollSpeed * delta
        # if self.engine.key_down(pygame.K_DOWN):
        #     self.scrollY += scrollSpeed * delta

    def draw(self):
        glClearColor(128/255.0,215/255.0,255/255.0,1)
        glClear(GL_COLOR_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        self.scrollX = self.player.x - self.engine.screenWidth*0.5
        self.scrollY = self.player.y - self.engine.screenHeight*0.5

        glTranslate(-self.scrollX, -self.scrollY, 0)

        boundRect = Rect(self.scrollX,
                        self.scrollY,
                        self.engine.screenWidth,
                        self.engine.screenHeight)
        self.map.draw(boundRect,'bg')
        self.map.draw(boundRect,'fg')
        self.player.draw()
