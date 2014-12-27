import pytest
import sux


def test_default_env(py2venv):
    """
    Py3 env is not inherited by default
    """
    test_env = sux.to_use('py2sux.envtest')

    with pytest.raises(sux.exceptions.KeyError):
        test_env.get_env('PATH')


def test_override_env(py2venv):
    """
    Env can be supplied
    """
    env = {"FOO": "BAR"}
    test_env = sux.to_use('py2sux.envtest', env=env)
    assert "BAR" == test_env.get_env("FOO").decode('utf-8')
