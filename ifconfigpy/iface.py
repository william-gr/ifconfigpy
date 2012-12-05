# Copyright (c) 2012 William Grzybowski
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

import logging
import os

from ifconfigpy.freebsd import FBSDInterfaces, FBSDInterface

log = logging.getLogger('iface')


class MetaInterfaces(object):

    def __new__(cls, name, bases, attrs):
        osname = os.uname()[0].lower()
        if osname == 'freebsd':
            base = type('BaseInterfaces', bases, attrs)
            new_class = type('FBSDInterfaces', (FBSDInterfaces, base), {})
        else:
            raise NotImplementedError
        return new_class

    def __repr__(self):
        return '<Interfaces(%s)>' % type(self).__name__

    def get_interfaces(self):
        raise NotImplementedError


class Interfaces(object):
    __metaclass__ = MetaInterfaces

    def __repr__(self):
        return '<Interfaces(%s)>' % type(self).__name__

    def get_interfaces(self):
        raise NotImplementedError


class MetaInterface(object):

    def __new__(cls, name, bases, attrs):
        osname = os.uname()[0].lower()
        if osname == 'freebsd':
            base = type('BaseInterface', bases, attrs)
            new_class = type('FBSDInterface', (FBSDInterface, base), {})
        else:
            raise NotImplementedError
        return new_class


class Interface(object):

    __metaclass__ = MetaInterface

    def __init__(self, name, **kwargs):
        self.name = name
        self._inets = []
        self._removed = []

    def __repr__(self):
        return '<Interface(%s)>' % self.name

    def __iter__(self):
        for inet in list(self._inets):
            yield inet

    def append(self, inet):
        inet.interface = self
        self._inets.append(inet)

    def remove(self, inet):
        self._inets.remove(inet)
        self._removed.append(inet)

    def find_byaddress(self, addr):
        for inet in self:
            if inet.addr == addr:
                return inet

    def save(self):
        raise NotImplementedError
