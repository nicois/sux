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

Now, with `PY2_VIRTUAL_ENV` still set, fire up python3
and get to work:

    import sux
    connection = sux.to_use('boto.s3.connection')
    conn = connection.S3Connection('abc', '123')
    conn.create_bucket("foo")
