sux
===

Python 2 compatibility layer for Python 3

For those times when you really need to use a non-python-3-compliant module but don't
want to downgrade your whole system to python 2.

e.g.
import sux
xero = sux.to_be('xero')
xero.auth = sux.to_be('xero.auth')
cred = xero.auth.PublicCredentials(XERO_KEY, XERO_SECRET, callback_uri="http://google.com/")
