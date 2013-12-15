from OpenGL.GL import *

__all__ = ['clamp', 'drawRect']

def clamp(x,a,b):
    if a > b:
        a,b = b,a
    if x < a:
        return a
    elif x > b:
        return b
    else:
        return x

def drawRect(texture, x, y, anchorX=0, anchorY=0, flipX=False, flipY=False):
    u0 = 0
    u1 = 1
    v0 = 1
    v1 = 0
    localX0 = -texture.width * anchorX
    localX1 = localX0 + texture.width
    localY0 = -texture.height * anchorY
    localY1 = localY0 + texture.height

    if flipX:
        localX0 *= -1
        localX1 *= -1
    if flipY:
        localY0 *= -1
        localY1 *= -1

    x0 = x + localX0
    x1 = x + localX1
    y0 = y + localY0
    y1 = y + localY1

    #print "U",u0,u1,"V",v0,v1,"X",x0,x1,"Y",y0,y1
    texture.bind()
    glColor4f(1,1,1,1)
    glBegin(GL_QUADS)
    glTexCoord2f(u0,v0)
    glVertex2f(x0,y0)
    glTexCoord2f(u1,v0)
    glVertex2f(x1,y0)
    glTexCoord2f(u1,v1)
    glVertex2f(x1,y1)
    glTexCoord2f(u0,v1)
    glVertex2f(x0,y1)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, 0)
    glBegin(GL_LINES)
    glColor4f(1,0,0,1)
    glVertex2f(x-5,y)
    glVertex2f(x+5,y)
    glVertex2f(x,y-5)
    glVertex2f(x,y+5)
    glEnd()
