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
