import os
from texturemanager import TextureManager
import xml.etree.ElementTree as ET
import os
from OpenGL.GL import *
from rect import Rect

class TileSet:
    def __init__(self, element):
        # pixels
        self.tileWidth = int(element.attrib['tilewidth'])
        self.tileHeight = int(element.attrib['tileheight'])
        self.firstGID = int(element.attrib['firstgid'])
        self.name = element.attrib['name']
        imageEl = element.find('image')
        imageFilename = os.path.basename(imageEl.attrib['source'])
        self.texture = TextureManager.get().load(imageFilename)
        self.width = self.texture.width / self.tileWidth
        self.height = self.texture.height / self.tileHeight

class TilemapLayer:
    def __init__(self, tileWidth, tileHeight, element):
        self.tileWidth = tileWidth
        self.tileHeight = tileHeight
        self.width = int(element.attrib['width'])
        self.height = int(element.attrib['height'])
        self.name = element.attrib['name']
        dataEl = element.find('data')
        self.tileGIDs = []
        for tileEl in dataEl.iterfind('tile'):
            self.tileGIDs.append(int(tileEl.attrib['gid']))
        assert len(self.tileGIDs) == self.width*self.height

class Spawn:
    def __init__(self, element):
        self.name = element.attrib.get('name',None)
        self.type = element.attrib.get('type',None)
        self.x = int(element.attrib['x'])
        self.y = int(element.attrib['y'])
        self.width = int(element.attrib['width'])
        self.height = int(element.attrib['height'])
        self.rect = Rect(self.x,self.y, self.width,self.height)
        self.properties = {}
        propertiesEl = element.find('properties')
        if propertiesEl is not None:
            for propertyEl in propertiesEl.iterfind('properties'):
                key = propertyEl.attrib['name']
                value = propertyEl.attrib['value']
                self.properties[key] = value

class Tilemap:
    def __init__(self, name):
        tree = ET.parse(os.path.join('maps',name+'.tmx'))
        rootEl = tree.getroot()
        self.tileWidth = int(rootEl.attrib['tilewidth'])
        self.tileHeight = int(rootEl.attrib['tileheight'])
        self.width = int(rootEl.attrib['width'])
        self.height = int(rootEl.attrib['height'])
        self.layers = []
        self.tilesets = []
        self.collideLayers = []
        for tilesetEl in rootEl.iterfind('tileset'):
            ts = TileSet(tilesetEl)
            assert ts.tileWidth == self.tileWidth
            assert ts.tileHeight == self.tileHeight
            self.tilesets.append(ts)
        for layerEl in rootEl.iterfind('layer'):
            layer = TilemapLayer(self.tileWidth, self.tileHeight, layerEl)
            assert layer.width == self.width
            assert layer.height == self.height
            if 'collide' in layer.name:
                self.collideLayers.append(layer)
            self.layers.append(layer)
        self.uvCache = {}
        self.tileset = self.tilesets[0]
        self.spawns = []
        for objectGroupEl in rootEl.iterfind('objectgroup'):
            for objectEl in objectGroupEl.iterfind('object'):
                self.spawns.append(Spawn(objectEl))

    def getCoords(self, gid):
        result = self.uvCache.get(gid)
        if result is None:
            iidx = gid-1
            u0 = (iidx % self.tileset.width)/float(self.tileset.width)
            u1 = u0 + 1.0/self.tileset.width
            v0 = (iidx / self.tileset.height)/float(self.tileset.height)
            v1 = v0 + 1.0/self.tileset.height
            v0 = 1-v0
            v1 = 1-v1
            result = (u0,u1,v0,v1)
            self.uvCache[gid] = result
        return result

    def draw(self, bounds, prefix):
        self.tilesets[0].texture.bind()
        glColor4f(1,1,1,1)
        glBegin(GL_QUADS)
        tw = self.tileWidth
        th = self.tileHeight

        minX,minY,maxX,maxY = self.getTileBoundsInclusive(bounds)

        for layer in self.layers:
            if not layer.name.startswith(prefix):
                continue
            for y in range(minY,maxY+1):
                for x in range(minX,maxX+1):
                    idx = x + y*layer.width
                    gid = layer.tileGIDs[idx]
                    if gid != 0:
                        u0,u1,v0,v1 = self.getCoords(gid)
                        glTexCoord2f(u0, v0)
                        glVertex2f(x*tw, y*th)
                        glTexCoord2f(u1, v0)
                        glVertex2f((x+1)*tw, y*th)
                        glTexCoord2f(u1, v1)
                        glVertex2f((x+1)*tw, (y+1)*th)
                        glTexCoord2f(u0, v1)
                        glVertex2f(x*tw, (y+1)*th)
        glEnd()

    def getTileBoundsInclusive(self, rect):
        tw = self.tileWidth
        th = self.tileHeight
        minX = int(rect.left / float(tw))
        minY = int(rect.top / float(th))
        maxX = int(rect.right / float(tw))
        maxY = int(rect.bottom / float(th))
        if minX < 0:
            minX = 0
        if minY < 0:
            minY = 0
        if maxX > self.width-1:
            maxX = self.width-1
        if maxY > self.height-1:
            maxY = self.height-1
        return minX,minY,maxX,maxY

    def rectOverlaps(self, rect):
        minX,minY,maxX,maxY = self.getTileBoundsInclusive(rect)

        for layer in self.collideLayers:

            for y in range(minY,maxY+1):
                for x in range(minX,maxX+1):
                    idx = x + y*layer.width
                    if layer.tileGIDs[idx] != 0:
                        return True
        return False
