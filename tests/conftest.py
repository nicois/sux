import tempfile
import subprocess
import pytest
import sux
import os.path

here = os.path.abspath(os.path.dirname(__file__))


class Python2VirtualEnv:
    def __init__(self):
        self.dir = tempfile.mkdtemp()
        subprocess.check_call(["virtualenv", "-ppython2", self.dir])
        sux.PYTHON2_VENV = self.dir
        os.symlink(os.path.join(here, "py2sux"),
                os.path.join(self.dir, "py2sux"))

    def install(self, package):
        subprocess.check_call([os.path.join(self.dir, "bin/pip"),
                              "install",
                              package])


@pytest.fixture(scope="session")
def py2venv():
    return Python2VirtualEnv()
