import importlib
import sys
from functools import wraps
from threading import RLock


class single_threaded_call_lock:
    """decorates a function to ensure it is only executed by one thread at a time"""

    def __new__(cls, func):
        obj = super().__new__(cls)
        obj.func = func
        obj.lock = RLock()
        obj.retval = None
        obj = wraps(func)(obj)
        return obj

    def __call__(self, *args, **kws):
        print('call!')
        if self.lock.acquire(False):
            # no other threads are running self.func; invoke it in this one
            try:
                ret = self.retval = self.func(*args, **kws)
            finally:
                self.lock.release()
        else:
            # another thread is running self.func; return its result
            self.lock.acquire(True)
            ret = self.retval
            self.lock.release()

        return ret


# otherwise turns out not to be thread-safe
@single_threaded_call_lock
def lazy_import(name):
    """postponed import of the module with the specified name.

    The import is not performed until the module is accessed in the code. This
    reduces the total time to import labbench by waiting to import the module
    until it is used.
    """
    # see https://docs.python.org/3/library/importlib.html#implementing-lazy-imports
    try:
        ret = sys.modules[name]
        return ret
    except KeyError:
        pass

    spec = importlib.util.find_spec(name)
    if spec is None:
        raise ImportError(f'no module found named "{name}"')
    spec.loader = importlib.util.LazyLoader(spec.loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module, spec


pd, spec = lazy_import('pandas')

# d = pd.DataFrame()
