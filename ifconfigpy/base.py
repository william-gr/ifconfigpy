class BaseInterfaces(object):

    def __repr__(self):
        return '<Interfaces(%s)>' % type(self).__name__

    def get_interfaces(self):
        return NotImplementedError


class Interface(object):

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


class InetBase(object):

    def __init__(self, addr, network):
        self._addr = addr
        self._network = network
        self._modified = False

    def __repr__(self):
        return '<%s(%s/%s)>' % (
            type(self).__name__,
            self.addr,
            self._network,
        )

    @property
    def addr(self):
        return self._addr

    @addr.setter
    def addr(self, value):
        self._addr = value
        self._modified = True


class Inet(InetBase):
    pass


class Inet6(InetBase):
    pass
