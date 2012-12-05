from ifconfigpy import _freebsd
from ifconfigpy.base import Inet, Inet6


class FBSDInterfaces:

    def get_interfaces(self):
        from ifconfigpy.iface import Interface

        interfaces = {}
        for ifname, ips in _freebsd.get_interfaces().items():

            iface = interfaces.get(ifname, None)
            if not iface:
                iface = Interface(ifname)
                interfaces[ifname] = iface

            for addr, netmask in ips:
                if '.' in addr:
                    iface.append(Inet(addr, netmask, new=False))
                else:
                    iface.append(Inet6(addr, netmask, new=False))

        return interfaces


class FBSDInterface:

    def save(self):
        for inet in list(self._removed):

            rv = False
            if isinstance(inet, Inet):
                rv = _freebsd.iface_inet_del(self.name, inet)

            elif isinstance(inet, Inet6):
                rv = _freebsd.iface_inet6_del(self.name, inet)

            if not rv:
                raise ValueError("errno")
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
                raise ValueError("errno")

            inet._modified = False
