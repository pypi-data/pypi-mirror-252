from __future__ import annotations

import dataclasses
import typing

AttrType = typing.TypeVar('AttrType', bound='C', covariant=True)
ValueTypeTuple = typing.TypeVarTuple('ValueTypeTuple')
ValueType = typing.TypeVar('ValueType')
ValueTypeWithNone = typing.TypeVar('ValueTypeWithNone')

NotAcceptNoneType = typing.TypeVar('NotAcceptNoneType')
AcceptNoneType = typing.TypeVar('AcceptNoneType')

# AllowNone = typing.TypeVar('AllowNone', bound=bool, covariant=True)
# T_co = typing.TypeVarTuple('T_co', covariant=True)
# C_co = typing.Generic["C_co[T_co, AllowNone]"]

# AttrType: typing.TypeAlias() = "C[ValueType]"
# C2 = typing.TypeVar('C2', bound="ValueType", covariant=True)


class NoneTypeProtocol(typing.Protocol[NotAcceptNoneType, AcceptNoneType]):
    # python typing does not yet support functions that return expanded type scope,
    # see https://github.com/python/typing/issues/548.
    # for now we can work around with this somewhat-hardcoded "switch" metaclass:

    @typing.overload
    def __call__(self: type[AcceptNoneType], *args, allow_none: typing.Literal[True], **kwargs) -> AcceptNoneType:
        ...

    @typing.overload
    def __call__(self: type[AcceptNoneType], *args, allow_none: typing.Literal[False], **kwargs) -> NotAcceptNoneType:
        ...

    @typing.overload
    def __call__(self: type[NotAcceptNoneType], *args, allow_none: typing.Literal[True], **kwargs) -> AcceptNoneType:
        ...

    @typing.overload
    def __call__(
        self: type[NotAcceptNoneType], *args, allow_none: typing.Literal[False], **kwargs
    ) -> NotAcceptNoneType:
        ...

    # @typing.overload
    # @classmethod
    # def __call__(cls: typing.Type[typing.Self], *args, allow_none: bool = False, **kwargs) -> C[T_co]:
    #     ...


#     # @typing.overload
#     # def __new__(cls, *args, allow_none: bool = False, **kwargs) -> typing.Union[P[T_co],P[typing.Union[T_co,None]]]:
#     #     ...


class Meta(NoneTypeProtocol[NotAcceptNoneType, AcceptNoneType], type):
    pass


@dataclasses.dataclass
class C(typing.Generic[ValueType], metaclass=Meta):
    allow_none: bool = False

    def set(self, value: ValueType):
        pass


class MixIn:
    a = 4


class D(C[ValueType], MixIn):
    potato: int = 4


class MyStr(D, metaclass=Meta['MyStr[str]', 'MyStr[str|None]']):
    pass


s = MyStr(allow_none=True)
s.set()

typing.reveal_type(s)
