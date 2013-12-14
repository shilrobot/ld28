import pygame
from OpenGL.GL import *
import os

def isPOT(x):
    return x > 0 and (x & (x-1)) == 0

class Texture:
    def __init__(self, path):
        surf = pygame.image.load(os.path.join('images',path))
        data = pygame.image.tostring(surf, "RGBA", 1)
        w,h = surf.get_width(), surf.get_height()
        if not isPOT(w) or not isPOT(h):
            print "WARNING: Texture %s is not power of 2 (%d,%d)" % (path, w,h)
        self.texID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texID)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
        glBindTexture(GL_TEXTURE_2D, 0)
        self.width = w
        self.height = h

    def bind(self):
        glBindTexture(GL_TEXTURE_2D, self.texID)

class TextureManager:
    def __init__(self):
        TextureManager.instance = self
        self.textures = {}

    def load(self,filename):
        tex = self.textures.get(filename)
        if tex is None:
            tex = Texture(filename)
            self.textures[filename] = tex
        return tex

    @staticmethod
    def get():
        return TextureManager.instance
