import sux

def test_sys_on_python2():
    p2sys = sux.to_use('sys')
    assert p2sys.version_info.major == 2
