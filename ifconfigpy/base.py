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

import abc
import socket


class InterfacesBase(object):

    __metaclass__ = abc.ABCMeta

    def __repr__(self):
        return '<Interfaces(%s)>' % type(self).__name__

    def get_interfaces(self):
        """Get interfaces available
        """
        raise NotImplementedError


class InterfaceBase(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, name, **kwargs):
        self.name = name
        self._inets = []
        self._removed = []

    def __repr__(self):
        return '<Interface(%s)>' % self.name

    def get_inet(self):
        """Get all available inet for this interface
        :returns list
        """
        raise NotImplementedError

    @property
    def mtu(self):
        """Interface MTU
        returns: integer
        """
        raise NotImplementedError

    @property
    def promiscuous(self):
        """Promiscuous mode
        returns: boolean
        """
        raise NotImplementedError

    @property
    def up(self):
        raise NotImplementedError


class InetBase(object):

    def __init__(self, iface, addr, netmask):
        self.iface = iface
        self._addr = addr
        self._netmask = netmask

    def __repr__(self):
        return '<%s(%s/%s)>' % (
            type(self).__name__,
            self.addr,
            self._netmask,
        )

    @property
    def addr(self):
        return self._addr

    @addr.setter
    def addr(self, value):
        self._addr = self.validate_addr(value)

    @property
    def netmask(self):
        return self._netmask

    @netmask.setter
    def netmask(self, value):
        self._netmask = self.validate_netmask(value)

    def validate_addr(self, addr):
        return addr

    def validate_netmask(self, netmask):
        return netmask


class Inet(InetBase):

    def validate_addr(self, addr):
        try:
            socket.inet_pton(socket.AF_INET, addr)
        except socket.error:
            raise ValueError("Invalid IPv4 Address: %s" % addr)
        return addr

    def validate_netmask(self, netmask):
        return self.validate_addr(netmask)


class Inet6(InetBase):

    def validate_addr(self, addr):
        try:
            socket.inet_pton(socket.AF_INET6, addr)
        except socket.error:
            raise ValueError("Invalid IPv6 Address: %s" % addr)
        return addr

    def validate_netmask(self, netmask):
        return self.validate_addr(netmask)
