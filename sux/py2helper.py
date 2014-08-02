"""
Remote execution server, running under python2
"""
from traceback import format_tb
import imp
from sys import stdin, stdout, stderr, version_info, modules
from pickle import loads, dumps, PicklingError

assert version_info.major == 2


class Mock(object):
    def __new__(cls, reference_id):
        return _reference_mapping[reference_id]


_sux = imp.new_module('sux')
vars(_sux).update({'Mock': Mock})
modules["sux"] = _sux


counter = iter(xrange(9999999))
_reference_mapping = {}


def debug(msg):
    #stderr.write(str(msg) + "\n")
    pass


def process_message(message):
    debug(message)
    command = message.pop("command")
    if command == u"import":
        module_name = message.get("module_name")
        result = globals()[module_name] = __import__(
                module_name, fromlist=["foo"])
        return result
    elif command == u"call":
        result = _reference_mapping[message["reference"]](
                *message["args"], **message["kwargs"])
        return result
    elif command == u"del":
        del _reference_mapping[message["reference"]]
        return "OK"
    elif command == u"getattr":
        if message.get("parent", None) is not None:
            parent = _reference_mapping[message["parent"]]
            return getattr(parent, message["attr"])
        else:
            return globals()[message["attr"]]
    else:
        # unhandled command
        assert False, message


def main():
    finished = False
    while not finished:
        try:
            message_length = int(stdin.readline())
            message = stdin.read(message_length)
        except ValueError:
            finished = True
            break
        try:
            unpickled = loads(message)
            response = process_message(unpickled)
        except Exception as ex:
            debug(format_tb)
            # ensure the exception is unpicklable at the other end
            response = Exception(ex.__class__.__name__, ex.message)
        reference = str(next(counter))
        _reference_mapping[reference] = response
        length = 0
        debug(response)
        try:
            payload = dumps(response, protocol=2)
            length = len(payload)
        except PicklingError:
            payload = "*+*+*+"  # invalid pickle format
        stdout.write("{0} {1}\n".format(length, reference))
        if length > 0:
            stdout.write(payload)
        stdout.flush()


if __name__ == '__main__':
    main()
