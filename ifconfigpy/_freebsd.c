/*
 Copyright (c) 2012 William Grzybowski
 All rights reserved.

 Redistribution and use in source and binary forms, with or without
 modification, are permitted provided that the following conditions
 are met:
 1. Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.
 2. Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in the
    documentation and/or other materials provided with the distribution.

 THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
 ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
 FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
 DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
 OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
 OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 SUCH DAMAGE.
*/

#include <netinet/in.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <ifaddrs.h>
#include <net/if.h>
#include <net/if_var.h>
#include <netinet6/in6_var.h>
#include <strings.h>
#include <sys/ioctl.h>
#include <sys/sockio.h>

#include <netinet6/nd6.h>       /* Define ND6_INFINITE_LIFETIME */

#include <Python.h>

static PyObject* get_interfaces(PyObject* self) {

    PyObject *interfaces, *interface, *key, *entry, *ips;
    struct ifaddrs *ifap, *ifa;
    struct sockaddr_in *inet;
    char output[200], *dst, address[INET_ADDRSTRLEN], address6[INET6_ADDRSTRLEN];
    int rv;

    getifaddrs(&ifap);

    interfaces = PyDict_New();
    Py_INCREF(interfaces);

    for(ifa=ifap;ifa!=NULL;ifa=ifa->ifa_next) {

        key = PyString_FromString(ifa->ifa_name);
        if(PyDict_Contains(interfaces, key)) {
            interface = PyDict_GetItem(interfaces, key);
	    ips = PyDict_GetItem(interface, PyString_FromString("ips"));
        } else {
            interface = PyDict_New();
            PyDict_SetItem(interfaces, key, interface);
            ips = PyList_New(0);
            PyDict_SetItem(interface, PyString_FromString("ips"), ips);
        }

        inet = (struct sockaddr_in *) ifa->ifa_addr;
        if(inet->sin_family == AF_INET) {

            entry = PyTuple_New(2);
            inet_ntop(inet->sin_family, &inet->sin_addr.s_addr, address, sizeof(address));
            PyTuple_SetItem(entry, 0, PyString_FromString(address));
            inet = (struct sockaddr_in *) ifa->ifa_netmask;
            inet_ntop(inet->sin_family, &inet->sin_addr.s_addr, address, sizeof(address));
            PyTuple_SetItem(entry, 1, PyString_FromString(address));
            PyList_Append(ips, entry);

        } else if(inet->sin_family == AF_INET6) {

            entry = PyTuple_New(2);
            inet_ntop(inet->sin_family, &inet->sin_addr.s_addr, address6, sizeof(address6));
            PyTuple_SetItem(entry, 0, PyString_FromString(address6));
            inet = (struct sockaddr_in *) ifa->ifa_netmask;
            inet_ntop(inet->sin_family, &inet->sin_addr.s_addr, address6, sizeof(address6));
            PyTuple_SetItem(entry, 1, PyString_FromString(address6));
            PyList_Append(ips, entry);

        }

    }

    freeifaddrs(ifap);

    return (PyObject*) interfaces;
}


static PyObject* iface_inet_add(PyObject* self, PyObject* args) {

    PyObject *obj, *attr;
    struct ifaliasreq ifareq;
    struct sockaddr_in *sin;
    int s, rv;
    uint32_t address;
    char *name;

    s = socket(PF_INET, SOCK_DGRAM, 0);

    if(!PyArg_ParseTuple(args, "sO", &name, &obj))
        return NULL;

    bzero(&ifareq, sizeof(struct ifaliasreq));

    strcpy((char *) &ifareq.ifra_name, name);

    attr = PyObject_GetAttrString(obj, "addr");
    inet_pton(AF_INET, PyString_AsString(attr), &address);

    sin = (struct sockaddr_in *) &ifareq.ifra_addr;
    sin->sin_len = sizeof(struct sockaddr_in);
    sin->sin_family = AF_INET;
    sin->sin_addr.s_addr = address;

    attr = PyObject_GetAttrString(obj, "netmask");
    inet_pton(AF_INET, PyString_AsString(attr), &address);

    sin = (struct sockaddr_in *) &ifareq.ifra_mask;
    sin->sin_len = sizeof(struct sockaddr_in);
    sin->sin_family = AF_INET;
    sin->sin_addr.s_addr = address;

    rv = ioctl(s, SIOCAIFADDR, &ifareq);
    close(s);

    if(rv) {
        return PyBool_FromLong(0);
    }

    return PyBool_FromLong(1);

}


static PyObject* iface_inet6_add(PyObject* self, PyObject* args) {

    PyObject *obj, *attr;
    struct in6_aliasreq ifareq;
    struct in6_addrlifetime ifra_lifetime = { 0, 0, ND6_INFINITE_LIFETIME, ND6_INFINITE_LIFETIME };
    struct sockaddr_in6 *sin;
    int s, rv;
    uint32_t address[4];
    char *name;

    s = socket(PF_INET6, SOCK_DGRAM, 0);

    if(!PyArg_ParseTuple(args, "sO", &name, &obj))
        return NULL;

    bzero(&ifareq, sizeof(struct in6_aliasreq));
    memcpy(&ifareq.ifra_lifetime, &ifra_lifetime, sizeof(struct in6_addrlifetime));

    strcpy((char *) &ifareq.ifra_name, name);

    attr = PyObject_GetAttrString(obj, "addr");
    inet_pton(AF_INET6, PyString_AsString(attr), &address);

    sin = (struct sockaddr_in6 *) &ifareq.ifra_addr;
    sin->sin6_len = sizeof(struct sockaddr_in6);
    sin->sin6_family = AF_INET6;
    memcpy(&sin->sin6_addr, address, sizeof(address));

    attr = PyObject_GetAttrString(obj, "netmask");
    inet_pton(AF_INET6, PyString_AsString(attr), &address);

    sin = (struct sockaddr_in6 *) &ifareq.ifra_prefixmask;
    sin->sin6_len = sizeof(struct sockaddr_in6);
    sin->sin6_family = AF_INET6;
    memcpy(&sin->sin6_addr, address, sizeof(address));

    rv = ioctl(s, SIOCAIFADDR_IN6, &ifareq);
    close(s);

    if(rv) {
        return PyBool_FromLong(0);
    }

    return PyBool_FromLong(1);

}


static PyObject* iface_inet_del(PyObject* self, PyObject* args) {

    PyObject *obj, *attr;
    struct ifreq ifreq;
    struct sockaddr_in *sin;
    int s, rv;
    uint32_t address;
    char *name;

    s = socket(PF_INET, SOCK_DGRAM, 0);

    if(!PyArg_ParseTuple(args, "sO", &name, &obj))
        return NULL;

    bzero(&ifreq, sizeof(struct ifreq));

    strcpy((char *) &ifreq.ifr_name, name);

    attr = PyObject_GetAttrString(obj, "addr");
    inet_pton(AF_INET, PyString_AsString(attr), &address);

    sin = (struct sockaddr_in *) &ifreq.ifr_addr;
    sin->sin_len = sizeof(struct sockaddr_in);
    sin->sin_family = AF_INET;
    sin->sin_addr.s_addr = address;

    attr = PyObject_GetAttrString(obj, "netmask");
    inet_pton(AF_INET, PyString_AsString(attr), &address);

    rv = ioctl(s, SIOCDIFADDR, &ifreq);
    close(s);

    if(rv) {
        return PyBool_FromLong(0);
    }

    return PyBool_FromLong(1);

}


static PyObject* iface_inet6_del(PyObject* self, PyObject* args) {

    PyObject *obj, *attr;
    struct in6_ifreq ifreq;
    struct sockaddr_in6 *sin;
    int s, rv;
    uint32_t address[4];
    char *name;

    s = socket(PF_INET6, SOCK_DGRAM, 0);

    if(!PyArg_ParseTuple(args, "sO", &name, &obj))
        return NULL;

    bzero(&ifreq, sizeof(struct in6_ifreq));

    strcpy((char *) &ifreq.ifr_name, name);

    attr = PyObject_GetAttrString(obj, "addr");
    inet_pton(AF_INET6, PyString_AsString(attr), &address);

    sin = (struct sockaddr_in6 *) &ifreq.ifr_addr;
    sin->sin6_len = sizeof(struct sockaddr_in6);
    sin->sin6_family = AF_INET6;
    memcpy(&sin->sin6_addr, address, sizeof(address));

    attr = PyObject_GetAttrString(obj, "netmask");
    inet_pton(AF_INET6, PyString_AsString(attr), &address);

    rv = ioctl(s, SIOCDIFADDR_IN6, &ifreq);
    close(s);

    if(rv) {
        return PyBool_FromLong(0);
    }

    return PyBool_FromLong(1);

}


static PyMethodDef FreeBSDMethods[] = {
    {"get_interfaces", (PyCFunction) get_interfaces, METH_NOARGS, "Get interfaces"},
    {"iface_inet_add", (PyCFunction) iface_inet_add, METH_VARARGS, "Add IPv4 to interface"},
    {"iface_inet_del", (PyCFunction) iface_inet_del, METH_VARARGS, "Delete IPv4 from interface"},
    {"iface_inet6_add", (PyCFunction) iface_inet6_add, METH_VARARGS, "Add IPv6 to interface"},
    {"iface_inet6_del", (PyCFunction) iface_inet6_del, METH_VARARGS, "Delete IP from interface"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


PyMODINIT_FUNC
init_freebsd(void) {
    PyObject *m;

    m = Py_InitModule("_freebsd", FreeBSDMethods);
    if (m == NULL)
        return;

}
