import os
from texturemanager import TextureManager
import xml.etree.ElementTree as ET
import os
from OpenGL.GL import *

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

class TilemapLayer:
	def __init__(self, tileWidth, tileHeight, element):
		self.tileWidth = tileWidth
		self.tileHeight = tileHeight
		self.width = int(element.attrib['width'])
		self.height = int(element.attrib['height'])
		dataEl = element.find('data')
		self.tileGIDs = []
		for tileEl in dataEl.iterfind('tile'):
			self.tileGIDs.append(int(tileEl.attrib['gid']))
		assert len(self.tileGIDs) == self.width*self.height

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
		for tilesetEl in rootEl.iterfind('tileset'):
			ts = TileSet(tilesetEl)
			assert ts.tileWidth == self.tileWidth
			assert ts.tileHeight == self.tileHeight
			self.tilesets.append(ts)
		for layerEl in rootEl.iterfind('layer'):
			layer = TilemapLayer(self.tileWidth, self.tileHeight, layerEl)
			assert layer.width == self.width
			assert layer.height == self.height
			self.layers.append(layer)
		self.uvCache = {}

	def getCoords(self, gid):
		result = self.uvCache.get(gid)
		if result is None:
			iidx = gid-1
			u0 = (iidx % 2)/2.0
			u1 = u0 + 0.5
			v0 = (iidx / 2)/2.0
			v1 = v0 + 0.5
			v0 = 1-v0
			v1 = 1-v1
			result = (u0,u1,v0,v1)
			self.uvCache[gid] = result
		return result

	def draw(self, bounds):
		self.tilesets[0].texture.bind()
		glColor4f(1,1,1,1)
		glBegin(GL_QUADS)
		tw = self.tileWidth
		th = self.tileHeight

		minX = int(bounds.left / float(tw))
		minY = int(bounds.top / float(th))
		maxX = int(bounds.right / float(tw))
		maxY = int(bounds.bottom / float(th))
		if minX < 0:
			minX = 0
		if minY < 0:
			minY = 0
		if maxX > self.width-1:
			maxX = self.width-1
		if maxY > self.height-1:
			maxY = self.height-1

		for layer in self.layers:
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
