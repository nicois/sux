import gc
import sux


def test_multiple_refs(py2venv):
    py2venv.install("boto==2.31.1")
    connection = sux.to_use('boto.s3.connection')
    # create two references to the same object
    conn1 = connection.S3Connection
    conn2 = connection.S3Connection
    # decrement one refcount to zero and let it be garbage collected
    del conn1
    gc.collect()
    # confirm we can still perform remote operations on this object
    conn2("abc", "123")
