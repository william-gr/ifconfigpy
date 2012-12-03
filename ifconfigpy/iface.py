import logging
import os
import sys

log = logging.getLogger('iface')


class BaseInterfaces(object):

    def __new__(cls, name, bases, attrs):
        osname = os.uname()[0].lower()
        if osname == 'freebsd':
            from .freebsd import FBSDInterfaces
            new_class = FBSDInterfaces
        else:
            raise NotImplementedError
        return new_class


class Interfaces(object):
    __metaclass__ = BaseInterfaces
