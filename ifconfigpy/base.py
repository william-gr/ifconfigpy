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
    def addr_s(self, value):
        self._addr = value
        self._modified = True

    @property
    def network(self):
        return self._network

    @network.setter
    def network_s(self, value):
        self._network = value
        self._modified = True


class Inet(InetBase):
    pass


class Inet6(InetBase):
    pass
