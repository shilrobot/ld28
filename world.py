from tilemap import Tilemap
from engine import Engine
import pygame
from OpenGL.GL import *
from rect import Rect
from gameobjects.player import Player
from gameobjects.oak import Oak
from gameobjects.willow import Willow

class World:

    def __init__(self):
        self.engine = Engine.get()
        self.scrollX = 0
        self.scrollY = 0
        self.map = Tilemap('test')
        self.objects = []
        self.player = None
        for spawn in self.map.spawns:
            self.doSpawn(spawn)
        #self.player = Player(self)

    def doSpawn(self, spawn):
        go = None
        if spawn.type == 'oak':
            go = Oak(self)
        elif spawn.type == 'willow':
            go = Willow(self)
        elif spawn.type == 'player':
            go = Player(self)
        if go is not None:
            go.spawn(spawn)
            self.objects.append(go)

    def update(self, delta):

        if self.engine.key_down(pygame.K_s):
            delta *= 0.25
        elif self.engine.key_down(pygame.K_f):
            delta *= 4
        #self.player.update(delta)
        # scrollSpeed = 300
        for go in self.objects:
            go.update(delta)

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

        if self.player is not None:
            self.scrollX = self.player.x - self.engine.screenWidth*0.5
            self.scrollY = self.player.y - self.engine.screenHeight*0.5

        glTranslate(-self.scrollX, -self.scrollY, 0)

        boundRect = Rect(self.scrollX,
                        self.scrollY,
                        self.engine.screenWidth,
                        self.engine.screenHeight)
        self.map.draw(boundRect,'bg')
        self.map.draw(boundRect,'fg')

        sortedObjects = sorted(self.objects, key=lambda go:go.priority)

        for go in sortedObjects:
            # TODO: pass in bounds
            go.draw()

        #self.player.draw()
