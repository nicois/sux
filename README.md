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
naughty packages:

    export PY2_VIRTUAL_ENV="/tmp/sux-to-use-python2"
    virtualenv -ppython2 "$PY2_VIRTUAL_ENV"
    "$PY2_VIRTUAL_ENV"/bin/pip install boto

Now, with `PY2_VIRTUAL_ENV` still set, fire up python3
and get to work:

    import sux
    connection = sux.to_use('boto.s3.connection')
    conn = connection.S3Connection('abc', '123')
    conn.create_bucket("foo")

The final command will attempt to connect to S3, and will raise a
sux.exceptions.S3ResponseError exception.


Tell me More!
=============
![CI status](https://travis-ci.org/nicois/sux.svg?branch=master)

Is this safe?
-------------
Probably not. All objects created in the python2 environment are
held in memory, so no garbage collection takes place until the
python3 process exits.

Is this fast?
-------------
Nope. Every interaction between python2 and python3 uses `pickle` for
transport and is not optimised for speed.

What is actually happening?
---------------------------
Each time you interact with the `sux` module, it tries to give you back a
native python representation of whatever ran in the python2 space. If
that's not possible, it passes back a proxy object instead. Whenever you
interact with that proxy object

What about exceptions?
----------------------
Any exception raised in the python2 environment
will cause an exception of the same name to be raised in the python3
space. See tests.test_boto for an example.
