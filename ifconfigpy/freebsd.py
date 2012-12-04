import ctypes
import logging
import socket

from ifconfigpy.base import Inet, Inet6

LIBC = ctypes.CDLL('libc.so.7', use_errno=True)

log = logging.getLogger('freebsd')

"""
Start TODO: Possibly move to a Python C Module
"""
IFNAMSIZ = 16
IOC_IN = 0x80000000
IOC_VOID = 0x20000000
IOC_OUT = 0x40000000
IOCPARM_SHIFT = 13
IOCPARM_MASK = ((1 << IOCPARM_SHIFT) - 1)


def _IOC(inout, group, num, _len):
    return (
        (inout) |
        ((((_len) & IOCPARM_MASK) << 16) | (ord(group) << 8) | (num))
    )


def _IOW(g, n, t):
    return _IOC(IOC_IN, g, n, ctypes.sizeof(t))
"""
End TODO
"""


class in_addr(ctypes.Structure):
    _fields_ = [
        ("s_addr", ctypes.c_uint32),
    ]


class sockaddr_in(ctypes.Structure):
    _fields_ = [
        ('sin_len', ctypes.c_uint8),
        ("sin_family", ctypes.c_uint8),
        ("sin_port", ctypes.c_uint16),
        ("sin_addr", in_addr),
        ("sin_zero", ctypes.c_char * 8),
    ]


class in6_u(ctypes.Union):
    _fields_ = [
        ("u6_addr8", (ctypes.c_uint8 * 16)),
        ("u6_addr16", (ctypes.c_uint16 * 8)),
        ("u6_addr32", (ctypes.c_uint32 * 4))
    ]


class in6_addr(ctypes.Structure):
    _fields_ = [
        ("in6_u", in6_u),
    ]


class sockaddr_in6(ctypes.Structure):
    _fields_ = [
        ('sin6_len', ctypes.c_uint8),
        ("sin6_family", ctypes.c_uint8),
        ("sin6_port", ctypes.c_uint16),
        ("sin6_flowinfo", ctypes.c_uint32),
        ("sin6_addr", in6_addr),
        ("sin6_scope_id", ctypes.c_uint32),
    ]


class struct_sockaddr(ctypes.Structure):
    _fields_ = [
        ('sa_len', ctypes.c_byte),
        ('sa_family_t', ctypes.c_uint8),
        ('sa_data', ctypes.c_char * 14),
    ]


class struct_ifaddrs(ctypes.Structure):
    pass
struct_ifaddrs._fields_ = [
    ('ifa_next', ctypes.POINTER(struct_ifaddrs)),
    ('ifa_name', ctypes.c_char_p),
    ('ifa_flags', ctypes.c_uint),
    ('ifa_addr', ctypes.POINTER(struct_sockaddr)),
    ('ifa_netmask', ctypes.POINTER(struct_sockaddr)),
    ('ifa_broadaddr', ctypes.POINTER(struct_sockaddr)),
    ('ifa_dstaddr', ctypes.POINTER(struct_sockaddr)),
    ('ifa_data', ctypes.c_void_p),
]


class struct_ifaliasreq(ctypes.Structure):
    _fields_ = [
        ("ifra_name", ctypes.c_char * IFNAMSIZ),
        ("ifra_addr", struct_sockaddr),
        ("ifra_broadaddr", struct_sockaddr),
        ("ifra_mask", struct_sockaddr),
        ("ifra_vhid", ctypes.c_int),
    ]


class FBSDInterfaces:

    def get_interfaces(self):
        from ifconfigpy.iface import Interface
        ifap = ctypes.POINTER(struct_ifaddrs)()
        LIBC.getifaddrs(ctypes.byref(ifap))

        interfaces = {}
        ifa = ifap
        while True:

            iface = interfaces.get(ifa.contents.ifa_name, None)
            if not iface:
                iface = Interface(ifa.contents.ifa_name)
                interfaces[iface.name] = iface

            family = ifa.contents.ifa_addr.contents.sa_family_t
            if family == socket.AF_INET:
                addr = sockaddr_in.from_address(
                    ctypes.addressof(ifa.contents.ifa_addr.contents)
                )
                ipv4addr = socket.inet_ntop(family, addr.sin_addr)
                addr = sockaddr_in.from_address(
                    ctypes.addressof(ifa.contents.ifa_netmask.contents)
                )
                ipv4network = socket.inet_ntop(family, addr.sin_addr)
                iface.append(Inet(ipv4addr, ipv4network))
            elif family == socket.AF_INET6:
                addr = sockaddr_in6.from_address(
                    ctypes.addressof(ifa.contents.ifa_addr.contents)
                )
                ipv6addr = socket.inet_ntop(family, addr.sin6_addr)
                addr = sockaddr_in6.from_address(
                    ctypes.addressof(ifa.contents.ifa_netmask.contents)
                )
                ipv6network = socket.inet_ntop(family, addr.sin6_addr)
                iface.append(Inet6(ipv6addr, ipv6network))
            # AF_LINK
            elif family == 18:
                pass
            else:
                log.debug("Unhandled family: %d", family)

            ifa = ifa.contents.ifa_next
            if not ifa:
                break

        LIBC.freeifaddrs(ifap)

        return interfaces


class FBSDInterface:

    def save(self):
        for inet in self:
            if not inet._modified:
                continue

            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
            ifaliasreq = struct_ifaliasreq()
            ifaliasreq.ifra_name = self.name

            if isinstance(inet, Inet):
                ip = sockaddr_in()
                ip.sin_family = socket.AF_INET
                ip.sin_len = ctypes.sizeof(sockaddr_in)
                ip.sin_addr.s_addr = LIBC.inet_addr(inet.addr)

                network = sockaddr_in()
                network.sin_family = socket.AF_INET
                network.sin_len = ctypes.sizeof(sockaddr_in)
                network.sin_addr.s_addr = LIBC.inet_addr(inet.network)

            elif isinstance(inet, Inet6):
                ip = sockaddr_in6()
                ip.sin6_family = socket.AF_INET6
                ip.sin6_len = ctypes.sizeof(sockaddr_in6)
                ip.sin6_addr.s_addr = LIBC.inet_addr(inet.addr)

                network = sockaddr_in6()
                network.sin6_family = socket.AF_INET6
                network.sin6_len = ctypes.sizeof(sockaddr_in6)
                network.sin6_addr.s_addr = LIBC.inet_addr(inet.network)

            ifaliasreq.ifra_addr = struct_sockaddr.from_address(
                ctypes.addressof(ip)
            )

            ifaliasreq.ifra_mask = struct_sockaddr.from_address(
                ctypes.addressof(network)
            )

            rv = LIBC.ioctl(
                s.fileno(),
                _IOW('i', 43, struct_ifaliasreq),  # SIOCAIFADDR
                ctypes.byref(ifaliasreq)
            )
            s.close()
            if rv != 0:
                raise ValueError("errno %d" % ctypes.get_errno())
