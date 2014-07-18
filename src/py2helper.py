"""
Remote execution server, running under python2
"""
from sys import stdin, stdout


def main():
    finished = False
    while not finished:
        line = stdin.readline()
        stdout.write("ok - {0}\n".format(line))


if __name__ == '__main__':
    main()
