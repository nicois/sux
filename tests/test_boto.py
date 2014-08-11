from pytest import raises
import sux


def test_proper_exception_raised(py2venv):
    """
    Using boto, demonstrate that the right exception
    is raised, with both the same name and text
    as the original exception.
    """
    py2venv.install("boto==2.31.1")
    connection = sux.to_use('boto.s3.connection')
    conn = connection.S3Connection('abc', '123')
    exception_info = raises(sux.exceptions.S3ResponseError,
            conn.create_bucket, "foo")
    assert "AWS Access Key Id" in str(exception_info)
