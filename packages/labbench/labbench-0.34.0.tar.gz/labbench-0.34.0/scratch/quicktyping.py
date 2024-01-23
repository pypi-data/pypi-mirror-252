from __future__ import annotations

import typing


class C:
    attr = 5
    """attr doc goes here"""


class D:
    def __new__(cls, *args, **kws):
        print(args, kws)
        obj = object.__new__(cls)
        obj.__init__()
        return obj


class E:
    @typing.overload
    def __new__(cls, key: None) -> G:
        ...

    @typing.overload
    def __new__(cls, key: object) -> F:
        ...

    __new__ = object.__new__
    # def __new__(cls, key):
    # if key is None:
    #     return object.__new__(G)
    # elif isinstance(key, str):
    #     return object.__new__(F)


class F(E):
    is_str = True

    def __call__(self, a, b):
        pass


class G(E):
    is_none = True

    def __call__(self, c):
        pass


obj = E(None)
obj()
