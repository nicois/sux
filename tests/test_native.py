import pytest
import sux


@pytest.mark.xfail
def test_native(py2venv):
    native_args = sux.to_use('py2sux.native_args')

    n1 = native_args.Python2Native(4)
    n2 = native_args.Python2Native(5)
    assert 9 == n1 + n2
