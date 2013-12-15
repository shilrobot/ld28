import pygame
from OpenGL.GL import *
import os
from rect import Rect
from texturemanager import TextureManager
from tilemap import Tilemap
import time
from utils import clamp

class Engine:

    @staticmethod
    def get():
        return Engine.instance

    def __init__(self):
        Engine.instance = self
        self.screenWidth = 1280
        self.screenHeight = 720
        pygame.init()
        if hasattr(pygame, 'GL_SWAP_CONTROL'):
            pygame.display.gl_set_attribute(pygame.GL_SWAP_CONTROL,1)
        pygame.display.set_mode((self.screenWidth, self.screenHeight),pygame.OPENGL | pygame.DOUBLEBUF)
        pygame.display.set_caption('LD28')

        # GL setup
        glEnable(GL_BLEND)
        glEnable(GL_TEXTURE_2D)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glDisable(GL_CULL_FACE)

        TextureManager()

        self.keysDown = pygame.key.get_pressed()
        self.keysDownLastFrame = self.keysDown
        from world import World
        self.world = World()

    def key_down(self, k):
        return self.keysDown[k]

    def key_pressed(self, k):
        return self.keysDown[k] and not self.keysDownLastFrame[k]

    def update(self, delta):
        self.keysDownLastFrame = self.keysDown
        self.keysDown = pygame.key.get_pressed()
        self.world.update(delta)

    def draw(self):
        #glClearColor(0,0,0,1)
        glClearColor(128/255.0,215/255.0,255/255.0,1)
        glClear(GL_COLOR_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.screenWidth, self.screenHeight, 0, -10, 10)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        self.world.draw()

        pygame.display.flip()

    def run(self):
        last_time = time.time()
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

            now = time.time()
            if now < last_time:
                last_time = now
            delta = now - last_time
            delta = clamp(delta, 0, 0.1)
            last_time = now
            self.update(delta)

            self.draw()

__all__ = [
    'Engine',
    'Texture',
    'Textures'
]
