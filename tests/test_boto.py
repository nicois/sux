from pytest import raises
import sux


def test_connection(py2venv):
    py2venv.install("boto==2.31.1")
    connection = sux.to_use('boto.s3.connection')
    conn = connection.S3Connection('abc', '123')
    exception_info = raises(sux.exceptions.S3ResponseError,
            conn.create_bucket, "foo")
    assert "AWS Access Key Id" in str(exception_info)
