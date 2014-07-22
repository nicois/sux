#!/usr/bin/env python3

from time import sleep
import sux

def test_urlparse():
    up = sux.to_be('urlparse')
    assert "urlparse" == up.__name__
    assert {} == up.parse_qs("")
    assert 'http://www.cwi.nl/%7Eguido/FAQ.html' == up.urljoin('http://www.cwi.nl/%7Eguido/Python.html', 'FAQ.html')




if __name__ == '__main__':
    test_fooey()
