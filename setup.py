#!/usr/bin/env python

from setuptools import setup, find_packages
from get_git_version import get_git_version

setup(name='uiltje',
    version=get_git_version(),
    description='System tray daemon to easily conect to Karpe Noktem\'s'\
          ' services',
    author='Bas Westerbaan',
    author_email='bas@westerbaan.name',
    url='http://github.com/karpenoktem/uiltje',
    packages=['uiltje'],
    package_data={'': ['*.mirte']},
    zip_safe=False,
    package_dir={'uiltje': 'src'},
    install_requires = ['wxpython'] # not sure
        )
