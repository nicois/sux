import tempfile
import subprocess
import pytest
import sux
import os.path


class Python2VirtualEnv:
    def __init__(self):
        self.dir = tempfile.mkdtemp()
        subprocess.check_call(["virtualenv", "-ppython2", self.dir])
        sux.PYTHON2_VENV = self.dir

    def install(self, package):
        subprocess.check_call([os.path.join(self.dir, "bin/pip"),
                              "install",
                              package])


@pytest.fixture(scope="session")
def py2venv():
    return Python2VirtualEnv()
