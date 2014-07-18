#!/usr/bin/env python3

from time import sleep
import sux


def test_fooey():
    xero = sux.to_be('xero')

    assert xero.__file__ == '/tmp/py2/local/lib/python2.7/site-packages/xero/__init__.py'
    assert repr(xero) == "<module 'xero' from '/tmp/py2/local/lib/python2.7/site-packages/xero/__init__.py'>"
    assert xero.constants.XERO_BASE_URL == 'https://api.xero.com'
    xero.foo()

    sleep(4)


if __name__ == '__main__':
    test_fooey()
