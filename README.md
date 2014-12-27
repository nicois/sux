sux
===

Python 2 compatibility layer for Python 3

For those times when you really need to use a
non-python-3-compliant module but don't
want to downgrade your whole system to python 2.

Are you crazy?
--------------
Yes, a little, but this actually works!

How could this possibly work?
-----------------------------
Simply install your python2 packages as you would normally, in a python2 (virtual)
environment. Then, in your python3 space, you will install and invoke `sux`, and it
will provide a "tunnel" through to python2, relaying your interactions between the
two environments.


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

What works?
-----------
* Importing a python2 package
* Accessing attributes in that package (recursively)
* Invoking functions and methods on the python2 objects
* Handling exceptions
* Garbage collection

What doesn't (yet) work?
------------------
* Simultaneous operations from multiple threads.
* Passing python3 objects to python2 space. (e.g. registering a 'hook' function with a python2 object)
* Accessing the special class methods starting with  double-underscore.

Is it thread-safe?
------------------
Yes. However, only one thread can be operating on a python2 object
at a time. So if you make a long-running call via sux, if another
thread attempts to use a python2 object, it will block.

How are exceptions handled?
---------------------------
Any exception raised in the python2 environment
will cause an exception of the same name (to be raised in the python3
space. See tests.test_boto for an example.

I want to control the environment of the python2 instance!
----------------------------------------------------------
OK:

    bf = sux.to_use('bioformats', env=os.environ)

or, if you are not afraid of accessing private attributes:

    bf = sux.to_use('bioformats', env=os.environ.__dict__['_data'])

Is this fast?
-------------
Every interaction between python2 and python3 uses `pickle` for
transport and is not optimised for speed. Then again, the python2 instance
runs in a separate process, with a separate GIL.
