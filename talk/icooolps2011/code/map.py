class Map(object):
    def __init__(self):
        self.indexes = {}
        self.other_maps = {}

    @purefunction
    def getindex(self, name):
        return self.indexes.get(name, -1)

    @purefunction
    def add_attribute(self, name):
        if name not in self.other_maps:
            newmap = Map()
            newmap.indexes.update(self.indexes)
            newmap.indexes[name] = len(self.indexes)
            self.other_maps[name] = newmap
        return self.other_maps[name]

EMPTY_MAP = Map()

class Instance(object):
    def __init__(self, cls):
        self.cls = cls
        self.map = EMPTY_MAP
        self.storage = []

    def getfield(self, name):
        map = hint(self.map, promote=True)
        index = map.getindex(name)
        if index != -1:
            return self.storage[index]
        raise AttributeError(name)

    def write_attribute(self, name, value):
        map = hint(self.map, promote=True)
        index = map.getindex(name)
        if index != -1:
            self.storage[index] = value
            return
        self.map = map.add_attribute(name)
        self.storage.append(value)

    def getattr(self, name):
        try:
            return self.getfield(name)
        except AttributeError:
            return self.cls.find_method(name)
