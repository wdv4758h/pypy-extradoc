class VersionTag(object):
    pass

class Class(object):
    def __init__(self, name):
        self.name = name
        self.methods = {}
        self.version = VersionTag()

    def find_method(self, name):
        self = hint(self, promote=True)
        version = hint(self.version, promote=True)
        result = self._find_method(name, version)
        if result is not None:
            return result
        raise AttributeError(name)

    @purefunction
    def _find_method(self, name, version):
        return self.methods.get(name)

    def change_method(self, name, value):
        self.methods[name] = value
        self.version = VersionTag()
