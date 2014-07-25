from subprocess import Popen, PIPE
import logging
from threading import Lock
from os import environ
from os.path import join, exists, dirname
from functools import partial
import pickle
from pickle import UnpicklingError
from sys import version_info

assert version_info.major == 3
PYTHON2_VENV = environ["PY2_VIRTUAL_ENV"]
dumps = partial(pickle.dumps, protocol=2, fix_imports=True)
loads = partial(pickle.loads, encoding="bytes")
NoneType = type(None)
_PYTHON2_HELPER_SCRIPT = join(dirname(__file__), "py2helper.py")
logger = logging.getLogger("sux")


class Python2Exception(Exception):
    pass


class __Exceptions:
    def __getattr__(self, name):
        new_exception = type(name, (Python2Exception,), {})
        setattr(self, name, new_exception)
        return new_exception


exceptions = __Exceptions()


class Python2Engine:
    def __init__(self, venv):
        self._lock = Lock()
        python2_exe = join(PYTHON2_VENV, "bin/python")
        assert exists(python2_exe)
        self.process = Popen([python2_exe, _PYTHON2_HELPER_SCRIPT],
                stdin=PIPE, stdout=PIPE)

    def send(self, **kwargs):
        with self._lock:
            logger.debug("Sending {0}".format(kwargs))
            payload = dumps(kwargs)
            self.process.stdin.write(
                    "{0}\n".format(len(payload)).encode('utf-8'))
            self.process.stdin.write(payload)
            self.process.stdin.flush()
            line = self.process.stdout.readline()
            message_length, reference = line.decode('utf-8').strip().split(" ")
            message_length = int(message_length)
            if message_length != 0:
                message = self.process.stdout.read(message_length)
            else:
                # only got a reference back; was not picklable at the py2 end
                message = None
            logger.debug("Received back: {0}, {1}".format(reference, message))
            return reference, message


_engine = None


def value_or_reference(command, **kwargs):

    reference = None
    pickled = None
    try:
        reference, pickled = _engine.send(command=command,
                                          **kwargs)
        if pickled is not None:
            unpickled = loads(pickled)
            if isinstance(unpickled, Exception):
                exception_name, exception_text = unpickled.args
                raise getattr(exceptions,
                        exception_name.decode('utf-8'))(exception_text)
            else:
                return unpickled
    except (ImportError, UnpicklingError):
        # A valid pickle, but couldn't unpickle
        pass
    assert reference != -1
    return Mock(remote_reference=reference)


class Mock:
    _remote_reference = None

    def __init__(self, remote_reference):
        self._remote_reference = remote_reference

    def __call__(self, *args, **kwargs):
        return value_or_reference(
                    command="call",
                    reference=self._remote_reference,
                    args=args,
                    kwargs=kwargs)

    def __getattr__(self, attribute_name):
        if attribute_name.startswith("_"):
            raise AttributeError(attribute_name)
        result = value_or_reference(command="getattr",
                                    parent=self._remote_reference,
                                    attr=attribute_name)
        return result

    def __del__(self):
        value_or_reference(
            command="del",
            reference=self._remote_reference)

    def __getnewargs__(self):
        return self._remote_reference,


def to_use(module_name, winge=False):
    global _engine
    if _engine is None:
        _engine = Python2Engine(PYTHON2_VENV)
    return value_or_reference(command="import",
                              module_name=module_name)
