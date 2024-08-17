#!/usr/bin/env python3

import re
import sys
from setuptools import setup, find_packages

if sys.version_info < (3, 9, 0, 'final', 0):
    raise SystemExit('Python 3.9 or later is required!')

with open('README.rst', encoding='utf-8') as fd:
    long_description = fd.read()

with open('rhodent/__init__.py') as fd:
    lines = '\n'.join(fd.readlines())

version = re.search("__version__ = '(.*)'", lines).group(1)
maintainer = re.search("__maintainer__ = '(.*)'", lines).group(1)
url = re.search("__url__ = '(.*)'", lines).group(1)
license = re.search("__license__ = '(.*)'", lines).group(1)
description = re.search("__description__ = '(.*)'", lines).group(1)

# PyPI name
setup(
    name='rhodent',
    version=version,
    description=description,
    long_description=long_description,
    license=license,
    url=url,
    platforms=['unix'],
    install_requires=[
        'ase',
        'gpaw',
        'numpy',
    ],
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Intended Audience :: Science/Research',
        f'License :: OSI Approved :: {license}',
        'Topic :: Scientific/Engineering :: Physics',
    ],
)
