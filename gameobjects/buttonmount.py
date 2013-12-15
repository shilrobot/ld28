from gameobject import GameObject
from texturemanager import TextureManager
from utils import drawRect

class ButtonMount(GameObject):
    def __init__(self, world):
        super(ButtonMount,self).__init__(world)
        self.texture = TextureManager.get().load('ButtonMount.png')
        self.proxyFor = None

    def spawn(self,spawn):
        super(ButtonMount,self).spawn(spawn)
        self.x = spawn.rect.centerX
        self.y = spawn.rect.centerY

    def onMapLoaded(self):
        if 'proxy' in self.spawn.properties:
            self.proxyFor = self.world.goMgr.get(self.spawn.properties['proxy'])

    def activate(self):
        if self.proxyFor is not None:
            self.proxyFor.activate()

    def draw(self):
        drawRect(self.texture, self.x, self.y, anchorX=0.5, anchorY=0.5)
