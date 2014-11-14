import sux
from os.path import join, dirname, abspath

py2sux_dir = abspath(join(dirname(__file__), "py2sux"))


def test_sys_on_python2(py2venv):
    p2sys = sux.to_use('sys', cwd=py2sux_dir)
    assert p2sys.version_info.major == 2
