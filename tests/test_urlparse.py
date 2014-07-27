import sux


def test_urlparse(py2venv):
    up = sux.to_use('urlparse')
    assert {} == up.parse_qs("")
    assert 'http://www.cwi.nl/%7Eguido/FAQ.html' == up.urljoin('http://www.cwi.nl/%7Eguido/Python.html', 'FAQ.html')
