#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
if not hasattr(sys, 'version_info') or sys.version_info < (2, 4, 0, 'final'):
    raise SystemExit("Mercurial requires python 2.4 or later.")

try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='ifconfigpy',
    version='0.1alpha',
    url='http://bitbucket.org/williambr/ifconfigpy',
    license='BSD',
    author='William Grzybowski',
    author_email='william8@gmail.com',
    description=('ifconfigpy is a python library to manipulate interfaces '
                 'like ifconfig'),
    long_description=open(
        os.path.join(os.path.dirname(__file__),
        'README')).read(),
    keywords='ifconfig',
    packages=('ifconfigpy', ),
    #package_data={ 'ifconfigpy': ['ifconfigpy.rst'] },
    platforms='any',
    install_requires=[],
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
    ],
    cmdclass={'build_py': build_py},
)
