import sux


def test_recursive_attribute(py2venv):
    """
    A trivial test proving that we have recursive
    attribute access to a real python2 object.
    """
    p2sys = sux.to_use('sys')
    assert p2sys.version_info.major == 2
