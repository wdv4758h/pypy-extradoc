class Class(object):
    def __init__(self, name):
        self.name = name
        self.methods = {}

    def instantiate(self):
        return Instance(self)

    def find_method(self, name):
        result = self.methods.get(name)
        if result is not None:
            return result
        raise AttributeError(name)

    def change_method(self, name, value):
        self.methods[name] = value


class Instance(object):
    def __init__(self, cls):
        self.cls = cls
        self.attributes = {}

    def getfield(self, name):
        result = self.attributes.get(name)
        if result is not None:
            return result
        raise AttributeError(name)

    def write_attribute(self, name, value):
        self.attributes[name] = value

    def getattr(self, name):
        try:
            return self.getfield(name)
        except AttributeError:
            return self.cls.find_method(name)
