"""
Remote execution server, running under python2
"""
from sys import stdin, stdout, stderr, version_info
from pickle import loads, dumps, PicklingError

assert version_info.major == 2


def debug_message(msg):
    stderr.write(msg)
    stderr.write("\n")


counter = iter(xrange(9999999))
_reference_mapping = {}


def process_message(message):
    debug_message(repr(message))
    command = message.pop("command")
    if command == u"import":
        module_name = message.get("module_name")
        result = globals()[module_name] = __import__(module_name)
        return result
    elif command == u"call":
        result = _reference_mapping[message["reference"]](
                *message["args"], **message["kwargs"])
        return result

    elif command == u"getattr":
        if message.get("parent", None) is not None:
            parent = _reference_mapping[message["parent"]]
            debug_message(str(parent))
            return getattr(parent, message["attr"])
        else:
            return globals()[message["attr"]]
    else:
        assert False, message


def main():
    finished = False
    while not finished:
        message_length = int(stdin.readline())
        message = stdin.read(message_length)
        debug_message(repr(message_length))
        unpickled = loads(message)
        response = process_message(unpickled)
        debug_message("2-> {0}".format(repr(response)))
        reference = -1
        try:
            payload = dumps(response, protocol=2)
        except PicklingError:
            reference = str(next(counter))
            _reference_mapping[reference] = response
            payload = "*+*+*+{0}".format(reference)
        debug_message("2A-> {0}".format(repr(payload)))
        stdout.write("{0} {1}\n".format(len(payload), reference))
        stdout.write(payload)
        stdout.flush()


if __name__ == '__main__':
    main()
