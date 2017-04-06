class NestedMixin(object):
    def __init__(self, parent, path, children):
        self.parent = parent
        self.path = str(path).replace('_', '-')
        self.children = children
        self._root = None

    @property
    def root(self):
        if self._root is None:
            if self.parent is None:
                self._root = self
            else:
                self._root = self.parent.root
        return self._root

    @property
    def full_path(self):
        if self.parent is not None:
            return self.parent.full_path + self.path + '/'
        else:
            return self.path + '/'
