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

from distutils.core import setup, Extension

from ifconfigpy import get_version

modules = []

if os.uname()[0].lower().startswith('freebsd'):
    modules.append(
        Extension(
            'ifconfigpy/_freebsd',
            sources=['ifconfigpy/_freebsd.c'],
        )
    )

setup(
    name='ifconfigpy',
    version=get_version(),
    url='http://bitbucket.org/williambr/ifconfigpy',
    license='BSD',
    author='William Grzybowski',
    author_email='william88@gmail.com',
    description=('ifconfigpy is a python library to manipulate interfaces '
                 'like ifconfig'),
    long_description=open(
        os.path.join(os.path.dirname(__file__),
        'README')).read(),
    keywords='ifconfig',
    packages=('ifconfigpy', ),
    #package_data={ 'ifconfigpy': ['ifconfigpy.rst'] },
    platforms='any',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License'
        'Operating System :: POSIX :: BSD :: FreeBSD',
        'Programming Language :: Python',
    ],
    cmdclass={'build_py': build_py},
    ext_modules=modules,
)
