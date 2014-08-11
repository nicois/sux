import pytest
import sux


@pytest.mark.xfail
def test_dunder_add(py2venv):
    """
    Demonstrate that the __add__ operator is correctly
    relayed to python2 land.
    """
    native_args = sux.to_use('py2sux.native_args')

    n1 = native_args.Python2Native(4)
    n2 = native_args.Python2Native(5)
    assert 9 == n1 + n2
