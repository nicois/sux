import sux


def test_urlparse(py2venv):
    """
    A trivial test importing a package
    which does not exist in python3
    """
    up = sux.to_use('urlparse')
    assert {} == up.parse_qs("")
    assert 'http://www.cwi.nl/%7Eguido/FAQ.html' == \
        up.urljoin('http://www.cwi.nl/%7Eguido/Python.html', 'FAQ.html')
