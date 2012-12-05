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

import socket


class InetBase(object):

    def __init__(self, addr, netmask, new=True):
        self.addr = addr
        self.netmask = netmask
        self.interface = None
        self._modified = new

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
        self._modified = True

    @property
    def netmask(self):
        return self._netmask

    @netmask.setter
    def netmask(self, value):
        self._netmask = self.validate_netmask(value)
        self._modified = True

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
