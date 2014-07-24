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
        result = globals()[module_name] = __import__(module_name, fromlist=["foo"])
        return result
    elif command == u"call":
        debug_message("M is {0}".format(message))
        debug_message("R is {0}".format(_reference_mapping[message["reference"]]))
        debug_message("Invoking {0} with args={1} and kw={2}"
                .format(message["reference"], message["args"], message["kwargs"]))
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
        # unhandled command
        assert False, message


def main():
    finished = False
    while not finished:
        message_length = int(stdin.readline())
        message = stdin.read(message_length)
        debug_message(repr(message_length))
        try:
            unpickled = loads(message)
            response = process_message(unpickled)
        except Exception as ex:
            response = Exception(str(ex))  # ensure the exception is unpicklable at the other end
        debug_message("2-> {0}".format(repr(response)))
        reference = str(next(counter))
        _reference_mapping[reference] = response
        length = 0
        try:
            payload = dumps(response, protocol=2)
            length = len(payload)
        except PicklingError:
            payload = "*+*+*+"  # invalid pickle format
        debug_message("2A-> {0}".format(repr(payload)))
        stdout.write("{0} {1}\n".format(length, reference))
        if length > 0:
            stdout.write(payload)
        stdout.flush()


if __name__ == '__main__':
    main()
