#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

from setuptools import setup, Extension

from ifconfigpy import get_version

modules = []

if os.uname()[0].lower().startswith('freebsd'):
    modules.append(
        Extension(
            'ifconfigpy/driver/_freebsd',
            sources=['ifconfigpy/driver/_freebsd.c'],
            extra_compile_args=["-Wall"],
        )
    )

setup(
    name='ifconfigpy',
    version=get_version(),
    url='https://github.com/williambr/ifconfigpy',
    license='BSD',
    author='William Grzybowski',
    author_email='wg@FreeBSD.org',
    description=('ifconfigpy is a python library to manipulate interfaces '
                 'like ifconfig(8)'),
    long_description=open(
        os.path.join(os.path.dirname(__file__),
        'README')).read(),
    keywords='ifconfig',
    packages=('ifconfigpy', 'ifconfigpy.driver'),
    platforms='any',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: BSD :: FreeBSD',
        'Programming Language :: Python',
    ],
    ext_modules=modules,
)
