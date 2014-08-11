class Python2Native(object):
    def __init__(self, n):
        self._n = n

    def __sum__(self, other):
        return self._n + other._n
