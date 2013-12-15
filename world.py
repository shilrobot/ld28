from tilemap import Tilemap
from engine import Engine
import pygame
from OpenGL.GL import *
from rect import Rect
from gameobjectmanager import GameObjectManager

from gameobjects.registry import goRegistry

class World:

    def __init__(self):
        self.engine = Engine.get()
        self.scrollX = 0
        self.scrollY = 0
        self.map = Tilemap('test')
        self.blockers = [self.map]
        self.goMgr = GameObjectManager()
        self.player = None
        for spawn in self.map.spawns:
            self.doSpawn(spawn)
        self.goMgr.onMapLoaded()
        self.services = {}

    def getService(self, name):
        return self.services.get(name)

    def registerService(self, name, service):
        self.services[name] = service

    def doSpawn(self, spawn):
        goClass = goRegistry.get(spawn.type)
        if goClass is not None:
            go = goClass(self)
            go.spawn(spawn)
            self.goMgr.add(go)
        else:
            print 'Unknown GO class: %s' % spawn.type

    def update(self, delta):

        # if self.engine.key_down(pygame.K_s):
        #     delta *= 0.25
        # elif self.engine.key_down(pygame.K_f):
        #     delta *= 4
        self.goMgr.update(delta)

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
        self.goMgr.prepareDraw()
        self.goMgr.drawBelowFG()
        self.map.draw(boundRect,'fg')
        self.goMgr.drawAboveFG()

    def rectOverlaps(self, rect):
        for blocker in self.blockers:
            if blocker.rectOverlaps(rect):
                return True
        return False