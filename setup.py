import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="sux",
    version="0.1.1",
    author="Nicholas Farrell",
    author_email="nicholas.farrell@gmail.com",
    description=("Transparently use python2 packages from python3"),
    license = "BSD",
    keywords = "python2",
    packages=['sux', 'tests'],
    install_requires=[
        'setuptools',
    ],
    url="https://github.com/nicois/sux/blob/master/README.md",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development",
        "License :: OSI Approved :: BSD License",
    ],
)
