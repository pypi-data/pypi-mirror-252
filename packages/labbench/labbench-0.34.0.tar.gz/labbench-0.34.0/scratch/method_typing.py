# # from __future__ import annotations
# # import typing
# # from typing import (
# #     Callable,
# #     TypeVar,
# #     Dict,
# #     Tuple,
# #     Type,
# #     List,
# #     Sequence,
# #     cast,
# #     get_type_hints,
# #     Concatenate,
# #     Any,
# #     Protocol,
# # )
# # from typing_extensions import TypeVarTuple, Unpack, ParamSpec
# # import functools
# # import labbench as lb
# # from labbench import paramattr as attr
# # from dataclasses import dataclass, make_dataclass

# # Ts = TypeVarTuple("Ts")
# # P = ParamSpec("P")


# # def whatever(*args, **kws):
# #     """docs"""
# #     pass


# # def method_factory(*args: Unpack[Ts]) -> Callable[[Unpack[Ts]]]:
# #     @functools.wraps(whatever)
# #     def myfunc(*a):
# #         return 7

# #     return myfunc


# # func = method_factory(attr.value.str.__init__, attr.value.bytes)


# # print(func.__annotations__)

# # from typing_extensions import dataclass_transform

# # # The ``ModelMeta`` metaclass and ``ModelBase`` class are defined by
# # # a library. This could be in a type stub or inline.
# # @dataclass_transform()
# # class ModelMeta(type): ...

# # class ModelBase(metaclass=ModelMeta): ...

# # # The ``ModelBase`` class can now be used to create new model
# # # subclasses, like this:
# # class CustomerModel(ModelBase):
# #     id: int
# #     name: str


# # class SpecializedModel(CustomerModel):
# #     other: float

# import typing

# class C:
#     role = None
#     extra: str = 'hi'

#     def validate(self):
#         return False

# class SubRole(C):
#     role = 'specific'

# class Type(C):
#     def validate(self):
#         return True


# class RoleType(SubRole, Type):
#     pass


# # print(typing.get_type_hints(lb.Device))
# import labbench as lb
# from typing import overload, Optional, Callable, Literal, Any

# # @overload
# def model_field(
#         *,
#         default: Optional[Any],
#         # resolver: Callable[[], Any],
#         # init: Literal[False] = False,
#     ):
#     pass

# class model_field(lb.paramattr._bases.Value, lb.paramattr._bases.Int):
#     pass
#     # def __init__(self, default: Optional[Any]):
#     #     pass

#     ...
# @overload
# def model_field(
#         *,
#         default: Optional[Any] = ...,
#         resolver: None = None,
#         init: bool = True,
#     ) -> Any: ...

# @typing.dataclass_transform(kw_only_default=True, eq_default=False, field_specifiers=lb.paramattr.value._ALL_TYPES)
# class Meta(type):
#     pass

# class Test(metaclass=Meta):
#     p: int = lb.paramattr.value.int(default=4)
#     # q: int = model_field(default=4)

# from labbench.paramattr import HasParamAttrs, HasParamAttrsMeta
# from labbench import paramattr as attr
# from labbench import util
# from typing import dataclass_transform


# # @dataclass_transform(kw_only_default=True, eq_default=False, field_specifiers=attr.value._ALL_TYPES)
# # class _ParamAttrDataClassMeta(HasParamAttrsMeta):
# #     pass


# @dataclass_transform(kw_only_default=True, eq_default=False, field_specifiers=attr.value._ALL_TYPES)
# class _ParamAttrDataClass(HasParamAttrs, util.Ownable):
#     def __init__(self, **kws):
#         pass


# class Device(_ParamAttrDataClass):
#     resource: str = attr.value.str(default="", allow_none=True, cache=True, help="device address or URI")
#     concurrency = attr.value.bool(default=True, sets=False, help="True if the device backend supports threading")

from __future__ import annotations

from collections.abc import Callable
from typing import (
    Generic,
    ParamSpec,
    Protocol,
    TypeVar,
)

import labbench as lb
from labbench import paramattr as attr


@attr.register_key_argument(attr.method_kwarg.int('channel', min=1, max=4))
class SimpleDevice(lb.VISADevice):
    implicit = attr.method.float(key='whatever{channel}')
    """

    Args:
        channel:
            The input channel to use
    """

    prop = attr.property.float(key='whatever{channel}')
    """doc string"""

    @attr.auto_method.int(min=1)
    def explicit(self, set_value: int = lb.Undefined, channel: int = 1):
        pass


d = SimpleDevice()

print(attr.value.int.__annotations__)

t = type(attr._bases.ParamAttr).with_type(int)
print(t)

T = TypeVar('T')
V = TypeVar('V')

U = TypeVar('U')
P = ParamSpec('P')


class A(Generic[T]):
    pass


class B(A[T], Generic[V]):
    pass


class C(B[T, V]):
    pass


from typing import dataclass_transform


@dataclass_transform(eq_default=False)
class C(Generic[T]):
    def __new__(cls, **args) -> C[T]:
        ...


class D(C[int]):
    a: int = 4


from typing import Concatenate

from typing_extensions import StringLiteral

CT_contra = TypeVar('CT_contra', contravariant=True)
RT_co = TypeVar('RT_co', covariant=True)
C = TypeVar('C')
R = TypeVar('R')
N = StringLiteral('N')

P = ParamSpec('P')


class Prot(Protocol[CT_contra, P, RT_co]):
    def __call__(
        self,
        _: CT_contra,  # this would be "self" on the method itself,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> RT_co:
        ...


class ReturnCallable(Protocol[CT_contra, P, N, T]):
    def __call__(
        self,
        _: CT_contra,  # this would be "self" on the method itself,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> RT_co:
        ...


def f1(
    name,
):
    print('f1: ', kws)


def f2(func: Callable[P, R], argument: attr.method_kwarg.Argument[T]) -> Callable[Concatenate[(n, int), P], R]:
    ...
    # @functools.wraps(func)
    # def wrapper(
    #         self: C,
    #         *args: P.args,
    #         **kwargs: P.kwargs
    #     ) -> R:
    #     return func(self, *args, **kwargs)
    # return wrapper


f3 = f2(f1, attr.method_kwarg.int(min=1, max=4))
