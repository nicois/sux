import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "sux",
    version = "0.0.1",
    author = "Nicholas Farrell",
    author_email = "nicholas.farrell@gmail.com",
    description = ("Use python2 packages from python3, if you really have to"),
    license = "BSD",
    keywords = "python2",
    url = "http://packages.python.org/sux",
    packages=['sux', 'tests'],
    install_requires=[
        'setuptools',
    ],
    #long_description=read('README.md'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
