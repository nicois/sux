"""
Remote execution server, running under python2
"""
from sys import stdin, stdout, stderr, version_info
from pickle import loads, dumps, PicklingError
import os

assert version_info.major == 2


def debug_message(msg):
    stderr.write(msg)
    stderr.write("\n")


counter = iter(xrange(9999999))
_reference_mapping = {}


def process_message(message):
    debug_message(repr(message))
    command = message.pop("command")
    if command == u"retrieve reference":
        n = next(counter)
        debug_message("nn: {0}".format(n))
        if message["parent"] is None:
            _reference_mapping[n] = eval(message["name"])
        else:
            _reference_mapping[n] = getattr(
                    _reference_mapping[message["parent"]],
                    message["name"])
        return n

    elif command == u"import":
        module_name = message.get("module_name")
        globals()[module_name] = __import__(module_name)
    elif command == u"query":
        return getattr(_reference_mapping[message["parent"]], message["name"])
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
        try:
            pickled_response = dumps(response, protocol=2)
            stdout.write(pickled_response)
        except PicklingError:
            stdout.write("   N O T  A  P I C K L E !!")
        stdout.write("\n")
        stdout.flush()


if __name__ == '__main__':
    main()
