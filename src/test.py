#!/usr/bin/env python3

from time import sleep
import sux


def test_fooey():
    xero = sux.to_be('xero')
    xero.auth = sux.to_be('xero.auth')

    assert xero.__file__ == '/tmp/py2-virtualenv/local/lib/python2.7/site-packages/xero/__init__.py'
    assert xero.constants.XERO_BASE_URL == 'https://api.xero.com'
    XERO_KEY = "K4VNBZN0BTV3Y5ZQIV8UN5OM4VEVOZ"
    XERO_SECRET = "WXVXBKVXDR4GEJX1R6WN3XLKJLVJJM"
    cred = xero.auth.PublicCredentials(XERO_KEY, XERO_SECRET, callback_uri="http://google.com/")
    print(cred.state)
    print(cred.url)


if __name__ == '__main__':
    test_fooey()
