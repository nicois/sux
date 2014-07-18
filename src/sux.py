"""
"""
from subprocess import Popen, PIPE
from os.path import join, exists, dirname
from json import dumps

NoneType = type(None)


PYTHON2_VENV = '/tmp/py2'
_PYTHON2_HELPER_SCRIPT = join(dirname(__file__), "py2helper.py")


class Python2Engine:
    def __init__(self, venv):
        python2_exe = join(PYTHON2_VENV, "bin/python")
        assert exists(python2_exe)
        self.process = Popen([python2_exe, _PYTHON2_HELPER_SCRIPT],
                stdin=PIPE, stdout=PIPE)

    def query_object(self, name, parent=None):
        response = self.send("query", name=name, parent=parent)
        return response

    def send(self, *args, **kwargs):
        payload = dumps(args, kwargs)
        self.process.stdin.write("{0}\n".format(payload).encode('utf-8'))
        return "FOOOO"


_engine = None


class Mock:
    _remote_reference = None

    def __init__(self, name, parent=None):
        self._name = name
        self._parent = parent
        self.__remote_reference = _engine.retrieve_reference(
                name=name,
                parent=parent._remote_reference)

    def __call__(self, x):
        raise NotImplementedError

    def _is_safe(self, obj):
        print(self._name, "is", repr(obj))
        if isinstance(obj, (str, NoneType)):
            return True
        return False

    def __getattr__(self, attribute_name, default=None):
        #  full_attr_name="{0}.{1}".format(self._name, attribute_name)
        remote_attr = _engine.query_object(name=attribute_name,
                parent=self._remote_reference)
        if self._is_safe(remote_attr):
            return remote_attr
        else:
            setattr(self, attribute_name,
                    Mock(name="{0}.{1}".format(self._name, attribute_name)))
            return getattr(self, attribute_name)


def to_be(module_name):
    global _engine
    if _engine is None:
        _engine = Python2Engine(PYTHON2_VENV)
    return Mock(name=module_name)
