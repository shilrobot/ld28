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

        TextureManager()

        self.map = Tilemap('test')
        self.scrollX = 0
        self.scrollY = 0
        self.keysDown = pygame.key.get_pressed()
        self.keysDownLastFrame = self.keysDown

    def key_down(self, k):
        return self.keysDown[k]

    def key_pressed(self, k):
        return self.keysDown[k] and not self.keysDownLastFrame[k]

    def update(self, delta):
        self.keysDownLastFrame = self.keysDown
        self.keysDown = pygame.key.get_pressed()

        scrollSpeed = 300

        if self.key_down(pygame.K_LEFT):
            self.scrollX -= scrollSpeed * delta
        if self.key_down(pygame.K_RIGHT):
            self.scrollX += scrollSpeed * delta
        if self.key_down(pygame.K_UP):
            self.scrollY -= scrollSpeed * delta
        if self.key_down(pygame.K_DOWN):
            self.scrollY += scrollSpeed * delta

    def draw(self):
        glClearColor(0,0,0,1)
        glClear(GL_COLOR_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.screenWidth, self.screenHeight, 0, -10, 10)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslate(-self.scrollX, -self.scrollY, 0)

        # tiles = TextureManager.get().load('tiles.png')
        # tiles.bind()

        boundRect = Rect(self.scrollX,
                        self.scrollY,
                        self.screenWidth,
                        self.screenHeight)
        self.map.draw(boundRect)

        # glBindTexture(GL_TEXTURE_2D, 0)
        # glColor3f(1,0,0)
        # glBegin(GL_LINES)
        # glVertex2f(boundRect.left, boundRect.top)
        # glVertex2f(boundRect.right, boundRect.top)

        # glVertex2f(boundRect.right, boundRect.top)
        # glVertex2f(boundRect.right, boundRect.bottom)

        # glVertex2f(boundRect.right, boundRect.bottom)
        # glVertex2f(boundRect.left, boundRect.bottom)

        # glVertex2f(boundRect.left, boundRect.bottom)
        # glVertex2f(boundRect.left, boundRect.top)
        # glEnd()
        # glColor4f(1,1,1,0.5)
        # glBegin(GL_QUADS)
        # # top left
        # glTexCoord2f(0,1)
        # glVertex3f(50,50,0)
        # # top right
        # glTexCoord2f(1,1)
        # glVertex3f(100,50,0)
        # # bottom left
        # glTexCoord2f(1,0)
        # glVertex3f(100,100,0)
        # # bottom right
        # glTexCoord2f(0,0)
        # glVertex3f(50,100,0)
        # glEnd()

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
