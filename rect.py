
class Rect(object):
    def __init__(self, x,y,w,h):
        self.x,self.y,self.w,self.h = x,y,w,h

    def copy(self):
        return Rect(self.x,self.y,self.w,self.h)

    @property
    def left(self):
        return self.x

    @property
    def right(self):
        return self.x + self.w

    @property
    def top(self):
        return self.y

    @property
    def bottom(self):
        return self.y + self.h

    @property
    def centerX(self):
        return self.x + self.w*0.5

    @property
    def centerY(self):
        return self.y + self.h*0.5

    def normalize(self):
        if self.w < 0:
            self.w *= -1
            self.x -= self.w
        if self.h < 0:
            self.h *= -1
            self.y -= self.h

    def normalizedCopy(self):
        c = self.copy()
        c.normalize()
        return c

    def mergedCopy(self, other):
        minX = min(self.x, other.x)
        minY = min(self.y, other.y)
        maxX = max(self.right, other.right)
        maxY = max(self.bottom, other.bottom)
        return Rect(minX, minY, maxX-minX, maxY-minY)

    def intersects(self, other):
        if (self.right < other.left or
            self.left > other.right or
            self.bottom < other.top or
            self.top > other.bottom):
            return False
        else:
            return True

    def __repr__(self):
        return 'Rect(%g,%g,%g,%g)' % (self.x,self.y,self.w,self.h)
