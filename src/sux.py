"""
"""
from subprocess import Popen, PIPE
from os import environ
from os.path import join, exists, dirname
from functools import partial
import pickle


PYTHON2_VENV = environ.get("PY2_VIRTUAL_ENV")


dumps = partial(pickle.dumps, protocol=2, fix_imports=True)
loads = pickle.loads
NoneType = type(None)
_PYTHON2_HELPER_SCRIPT = join(dirname(__file__), "py2helper.py")


class NotAPickle(Exception):
    pass


class Python2Engine:
    def __init__(self, venv):
        python2_exe = join(PYTHON2_VENV, "bin/python")
        assert exists(python2_exe)
        self.process = Popen([python2_exe, _PYTHON2_HELPER_SCRIPT],
                stdin=PIPE, stdout=PIPE)

    def query_object(self, name, parent=None):
        response = self.send(command="query", name=name, parent=parent)
        return response

    def send(self, **kwargs):
        payload = dumps(kwargs)
        self.process.stdin.write("{0}\n".format(len(payload)).encode('utf-8'))
        self.process.stdin.write(payload)
        self.process.stdin.flush()

        message_length = int(self.process.stdout.readline())
        message = self.process.stdout.read(message_length)

        try:
            return loads(message)
        except Exception as ex:
            raise NotAPickle(message)


_engine = None


class Mock:
    _remote_reference = None

    def __init__(self, name, parent=None, remote_reference=None):
        self._name = name
        self._parent = parent
        self._remote_reference = remote_reference
        if self._remote_reference is None:
            self._remote_reference = _engine.send(
                command="retrieve reference",
                name=name,
                parent=None if parent is None else parent._remote_reference)

    def __call__(self, *args, **kwargs):
        try:
            return  _engine.send(
                    command="call",
                    name=self._name,
                    args=args,
                    kwargs=kwargs,
                    ref=self._remote_reference)
        except NotAPickle as nap:
            # the remote reference is passed back as the exception body
            print("nap is", nap)
            return Mock(name=self._name, parent=self._parent,
                    remote_reference=nap)

    def __getattr__(self, attribute_name, default=None):
        #  full_attr_name="{0}.{1}".format(self._name, attribute_name)
        try:
            remote_attr = _engine.query_object(name=attribute_name,
                parent=self._remote_reference)
            return remote_attr
        except NotAPickle:
            setattr(self, attribute_name,
                    Mock(name=attribute_name, parent=self))
            return getattr(self, attribute_name)


def to_be(module_name):
    global _engine
    if _engine is None:
        _engine = Python2Engine(PYTHON2_VENV)
    _engine.send(command="import", module_name=module_name)
    return Mock(name=module_name)
