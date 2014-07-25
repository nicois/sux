"""
Remote execution server, running under python2
"""
from sys import stdin, stdout, version_info
from pickle import loads, dumps, PicklingError

assert version_info.major == 2


counter = iter(xrange(9999999))
_reference_mapping = {}


def process_message(message):
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
        message_length = int(stdin.readline())
        message = stdin.read(message_length)
        try:
            unpickled = loads(message)
            response = process_message(unpickled)
        except Exception as ex:
            # ensure the exception is unpicklable at the other end
            response = Exception(str(ex))
        reference = str(next(counter))
        _reference_mapping[reference] = response
        length = 0
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
