from pytest import raises
import sux


connection = sux.to_use('boto.s3.connection')


def test_connection():
    conn = connection.S3Connection('abc', '123')
    exception_info = raises(Exception, conn.create_bucket, "foo")
    assert "403 Forbidden" in str(exception_info)

