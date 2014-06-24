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

from ifconfigpy.driver import _freebsd
from ifconfigpy import base


class Interfaces(base.InterfacesBase):

    def get_interfaces(self):

        interfaces = {}
        for ifname in _freebsd.get_interfaces():
            iface = Interface(ifname)
            interfaces[ifname] = iface

        return interfaces


class Interface(base.InterfaceBase):

    @property
    def _flags(self):
        return _freebsd.iface_get_flags(self.name)

    @_flags.setter
    def _flags(self, value):
        assert _freebsd.iface_set_flags(self.name, value) is True

    @property
    def mtu(self):
        return _freebsd.iface_get_mtu(self.name)

    @property
    def promiscuous(self):
        flags = self._flags
        if flags:
            return bool(flags & _freebsd.IFF_PROMISC)

    @property
    def up(self):
        if self._flags:
            return bool(self._flags & _freebsd.IFF_UP)

    @up.setter
    def up(self, value):
        flags = self._flags
        if flags:
            if value != self.up:
                self._flags |= _freebsd.IFF_UP

    @property
    def inet(self):
        inets = []
        for inet in _freebsd.iface_inet_get(self.name):
            inets.append(
                base.Inet(self, inet['address'], inet['netmask'])
            )
        return inets

    @inet.setter
    def inet(self, value):
        inet = self.inet
