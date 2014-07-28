class Python2Native(object):
    def __init__(self, n):
        self._n = n

    @classmethod
    def sum(cls, *args):
        return sum(native._n for native in args)
