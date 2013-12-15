
class GameObjectManager:
    def __init__(self):
        self.objects = []
        self.objectsByName = {}

    def update(self, delta):
        for go in self.objects:
            if go is not None:
                go.update(delta)
        if any([go is None for go in self.objects]):
            self.objects = [x for x in self.objects if x is not None]
            for n,go in enumerate(self.objects):
                go.index = n

    def draw(self):
        sortedObjects = sorted([go for go in self.objects if go.visible], key=lambda go:go.priority)

        for go in sortedObjects:
            go.draw()

    def add(self, go):
        assert go.index == -1
        self.objects.append(go)
        go.index = len(self.objects)-1
        if go.name is not None and go.name not in self.objectsByName:
            self.objectsByName[go.name] = go
        go.onAdded()

    def remove(self, go):
        if go.index == -1:
            return
        assert go.index >= 0 and go.index < len(self.objects)
        assert self.objects[go.index] == go
        go.onRemoving()
        self.objects[go.index] = None
        if go.name is not None and self.objectsByName.get(go.name) == go:
            del self.objectsByName[go.name]
        go.index = -1
        go.onRemoved()

    def get(self, name):
        return go.objectsByName.get(name, None)

    def onMapLoaded(self):
        for go in self.objects:
            go.onMapLoaded()
