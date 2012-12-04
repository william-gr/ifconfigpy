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
        self.addresses = []

    def __repr__(self):
        return '<Interface(%s)>' % self.name

    def __iter__(self):
        for addr in list(self.addresses):
            yield addr

    def append(self, addr):
        addr.interface = self
        self.addresses.append(addr)

    def save(self):
        raise NotImplementedError
