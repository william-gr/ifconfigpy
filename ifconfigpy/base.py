import socket


class InetBase(object):

    def __init__(self, addr, netmask, new=True):
        self.addr = addr
        self.netmask = netmask
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
