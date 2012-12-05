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

from ifconfigpy import _freebsd
from ifconfigpy.base import Inet, Inet6


class FBSDInterfaces:

    def get_interfaces(self):
        from ifconfigpy.iface import Interface

        interfaces = {}
        for ifname, data in _freebsd.get_interfaces().items():

            iface = interfaces.get(ifname, None)
            if not iface:
                iface = Interface(ifname)
                interfaces[ifname] = iface

            iface._flags = data.get("flags")
            for addr, netmask in data.get("ips", []):
                if '.' in addr:
                    iface.append(Inet(addr, netmask, new=False))
                else:
                    iface.append(Inet6(addr, netmask, new=False))

        return interfaces


class FBSDInterface:

    @property
    def up(self):
        if self._flags:
            return bool(self._flags & _freebsd.IFF_UP)

    @up.setter
    def up(self, value):
        if self._flags:
            if value != self.up:
                self._flags ^= _freebsd.IFF_UP

    def save(self):
        for inet in list(self._removed):

            rv = False
            if isinstance(inet, Inet):
                rv = _freebsd.iface_inet_del(self.name, inet)

            elif isinstance(inet, Inet6):
                rv = _freebsd.iface_inet6_del(self.name, inet)

            if not rv:
                raise ValueError("error")
            self._removed.remove(inet)

        for inet in self:
            if not inet._modified:
                continue

            rv = False

            if isinstance(inet, Inet):
                rv = _freebsd.iface_inet_add(self.name, inet)

            elif isinstance(inet, Inet6):
                rv = _freebsd.iface_inet6_add(self.name, inet)

            if not rv:
                raise ValueError("error")

            inet._modified = False
