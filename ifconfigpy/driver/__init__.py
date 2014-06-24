import imp
import os


def load():
    name = os.uname()[0].lower()
    mod = imp.find_module(name, [os.path.dirname(__file__)])
    try:
        return imp.load_module(name, *mod)
    except Exception, e:
        return None
