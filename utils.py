from OpenGL.GL import *
from rect import Rect

__all__ = ['clamp', 'drawRect']

def lerp(a,b,t):
    return a + (b-a)*t

def clamp(x,a,b):
    if a > b:
        a,b = b,a
    if x < a:
        return a
    elif x > b:
        return b
    else:
        return x

def noTexture():
    glDisable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, 0)

def debugRect(rect, r,g,b,a=1):
    noTexture()


    glBegin(GL_LINES)
    glColor4f(r,g,b,a)

    glVertex2f(rect.left,rect.top)
    glVertex2f(rect.right,rect.top)

    glVertex2f(rect.right,rect.top)
    glVertex2f(rect.right,rect.bottom)

    glVertex2f(rect.right,rect.bottom)
    glVertex2f(rect.left,rect.bottom)

    glVertex2f(rect.left,rect.bottom)
    glVertex2f(rect.left,rect.top)


    glEnd()

def drawRect(texture, x, y, anchorX=0, anchorY=0, flipX=False, flipY=False, scale=1):
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

    localX0 *= scale
    localX1 *= scale
    localY0 *= scale
    localY1 *= scale

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

    # noTexture()
    # glBegin(GL_LINES)
    # glColor4f(1,0,0,1)
    # glVertex2f(x-5,y)
    # glVertex2f(x+5,y)
    # glVertex2f(x,y-5)
    # glVertex2f(x,y+5)
    # glEnd()


def sweepMovement(world, rect, dx, dy):
    startRect = rect.copy()
    endRect = rect.copy()
    endRect.x += dx
    endRect.y += dy
    merged = startRect.mergedCopy(endRect)

    if not world.rectOverlaps(merged):
        return (False, dx, dy)

    minT = 0
    maxT = 1
    for n in range(10):
        testT = (minT+maxT)*0.5
        testRect = rect.copy()
        testRect.x += dx*testT
        testRect.y += dy*testT
        if world.rectOverlaps(testRect):
            maxT = testT
        else:
            minT = testT

    if minT >= 1:
        return (False, dx, dy)
    else:
        return (True, dx*minT, dy*minT)
