sux
===

Python 2 compatibility layer for Python 3

For those times when you really need to use a
non-python-3-compliant module but don't
want to downgrade your whole system to python 2.

Quickstart
----------
In a python3 (virtual) env:

    pip3 install sux

Create your python2 virtualenv and install the
naughty package(s):

    export PY2_VIRTUAL_ENV="/tmp/sux-to-use-python2"
    virtualenv -ppython2 "$PY2_VIRTUAL_ENV"
    "$PY2_VIRTUAL_ENV"/bin/pip install boto

Now, with `PY2_VIRTUAL_ENV` still set, fire up python3
and get to work:

    import sux
    connection = sux.to_use('boto.s3.connection')
    conn = connection.S3Connection('abc', '123')
    conn.create_bucket("foo")

The final command will attempt to connect to S3, and will raise
sux.exceptions.S3ResponseError.

Note that the `to_use` operator expects a package name to be passed.
e.g. with the pyxero package, you might choose to do the following:

    PublicCredentials = sux.to_use('xero.auth').PublicCredentials
    Xero = sux.to_use('xero').Xero

where in a native python2 environment you would have instead used:

    from xero.auth import PublicCredentials
    from xero import Xero


Tell me More!
=============
![CI status](https://travis-ci.org/nicois/sux.svg?branch=master)

Is it safe?
-----------
In my limited testing, I have not yet found anything it can't handle. If you do,
please give me details, and I will do my best to get it working for you. It is
thread-safe, supports function calls with python2 objects as arguments, and more.


Is this fast?
-------------
Every interaction between python2 and python3 uses `pickle` for
transport and is not optimised for speed. Then again, the python2 instance
runs in a separate process, with a separate GIL.

What about exceptions?
----------------------
Any exception raised in the python2 environment
will cause an exception of the same name to be raised in the python3
space. See tests.test_boto for an example.
