class LazyMixin(object):
    def __init__(self):
        self._value = None

    @property
    def value(self):
        if self._value is None:
            self._value = self.retrieve()
        return self._value

    def __getitem__(self, key):
        return self.value.__getitem__(key)

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return repr(self.value)

    def __len__(self):
        return len(self.value)