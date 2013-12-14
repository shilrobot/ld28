
class Rect:
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
