import pygame
from OpenGL.GL import *
import os
from rect import Rect
from texturemanager import TextureManager
from tilemap import Tilemap

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

    def draw(self):
        glClearColor(0,0,0,1)
        glClear(GL_COLOR_BUFFER_BIT)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, self.screenWidth, self.screenHeight, 0, -10, 10)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # tiles = TextureManager.get().load('tiles.png')
        # tiles.bind()

        boundRect = Rect(0,0,self.screenWidth,self.screenHeight)
        self.map.draw(boundRect)

        glBindTexture(GL_TEXTURE_2D, 0)
        glColor3f(1,0,0)
        glBegin(GL_LINES)
        glVertex2f(boundRect.left, boundRect.top)
        glVertex2f(boundRect.right, boundRect.top)

        glVertex2f(boundRect.right, boundRect.top)
        glVertex2f(boundRect.right, boundRect.bottom)

        glVertex2f(boundRect.right, boundRect.bottom)
        glVertex2f(boundRect.left, boundRect.bottom)

        glVertex2f(boundRect.left, boundRect.bottom)
        glVertex2f(boundRect.left, boundRect.top)
        glEnd()
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
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
            self.draw()

__all__ = [
    'Engine',
    'Texture',
    'Textures'
]