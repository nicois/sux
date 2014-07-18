"""
Remote execution server, running under python2
"""
from sys import stdin, stdout, stderr, version_info
from pickle import loads, dumps


assert version_info.major == 2

def debug_message(msg):
    stderr.write(msg + "\n")


def main():
    finished = False
    while not finished:
        debug_message("waiting...")
        message_length = stdin.readline()
        debug_message("2L <- {0}".format(message_length))
        message = stdin.readline()
        debug_message("2 <- {0}".format(repr(message)))
        unpickled = loads(message)
        if len(message_length) == 0:
            stderr.write("giving up reading stdin\n")
            finished = True
        response = ("yeah", unpickled)
        debug_message("2-> {0}".format(repr(response)))
        stdout.write(dumps(response, protocol=2))
        stdout.write("\n")
        stdout.flush()


if __name__ == '__main__':
    main()
