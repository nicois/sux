from subprocess import Popen, PIPE
import logging
import atexit
from threading import Lock
from os import environ
from os.path import join, exists, dirname
from functools import partial
import pickle
from pickle import UnpicklingError
from sys import version_info
from .pickle_fixer import bytes_to_unicode


assert version_info.major == 3
PYTHON2_VENV = environ.get("PY2_VIRTUAL_ENV", None)
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
    _cache = {}

    @classmethod
    def new(cls, *args):
        """
        Returns an existing instance if the kwargs
        match those provided earlier. Otherwise,
        create a new instance.
        """
        try:
            return cls._cache[args]
        except KeyError:
            new_instance = cls._cache[args] = cls(*args)
            return new_instance

    def __init__(self, venv, cwd=None):
        self._lock = Lock()
        assert venv is not None, "'PY2_VIRTUAL_ENV' is not defined"
        if cwd is None:
            cwd = venv
        python2_exe = join(venv, "bin/python")
        assert exists(python2_exe), "{0} does not exist!".format(python2_exe)
        logger.debug("Starting Python2 engine in {0}".format(cwd))
        env = {"PYTHONPATH": cwd}
        self.process = Popen([python2_exe, _PYTHON2_HELPER_SCRIPT],
                stdin=PIPE, stdout=PIPE, env=env, cwd=cwd)

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

shutting_down = False


@atexit.register
def notify_engine_of_shutdown():
    global shutting_down
    shutting_down = True


def _value_or_reference(command, engine, **kwargs):
    if shutting_down:
        return None  # this prevent segfaults on termination
    reference = None
    pickled = None
    try:
        reference, pickled = engine.send(command=command,
                                         **kwargs)
        if pickled is not None:
            unpickled = bytes_to_unicode(loads(pickled))
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
    return Mock(remote_reference=reference, engine=engine)


class Mock:
    _remote_reference = None
    _engine = None

    def __init__(self, remote_reference, engine):
        self._engine = engine
        self._remote_reference = remote_reference

    def __call__(self, *args, **kwargs):
        return _value_or_reference(
                    command="call",
                    engine=self._engine,
                    reference=self._remote_reference,
                    args=args,
                    kwargs=kwargs)

    def __getattr__(self, attribute_name):
        if attribute_name.startswith("_"):
            raise AttributeError(attribute_name)
        result = _value_or_reference(command="getattr",
                                    engine=self._engine,
                                    parent=self._remote_reference,
                                    attr=attribute_name)
        return result

    def __del__(self):
        if self._engine is not None:
            _value_or_reference(
                command="del",
                engine=self._engine,
                reference=self._remote_reference)

    def __getnewargs__(self):
        return self._remote_reference,


def to_use(module_name, winge=False, cwd=None):
    engine = Python2Engine.new(PYTHON2_VENV, cwd)
    assert engine is not None
    return _value_or_reference(command="import",
                              engine=engine,
                              module_name=module_name)
