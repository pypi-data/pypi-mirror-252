# from __future__ import annotations
# from typing import Generic, Union
# import typing

# T = typing.TypeVar("T")
# _P = typing.ParamSpec("_P")


# @typing.dataclass_transform()
# class Method(Generic[T]):
#     key: typing.Any
#     i: int


# class DecoratedMethod(Method[T], Generic[T, _P]):
#     b: bytes = b"a"

#     @typing.overload
#     def __new__(cls, key: typing.Any, **arguments) -> KeyedMethod[T]:
#         ...

#     @typing.overload
#     def __new__(cls, key: **arguments) -> Decorator[T, _P]:
#         ...

#     def __call__(self, *args: _P.args, **arguments: _P.kwargs) -> Union[T, None]:
#         ...


# class KeyedMethod(Method[T,_P]):
#     a: float = 4.3

#     @typing.overload
#     def __new__(cls, key: typing.Any, **arguments) -> KeyedMethod[T]:
#         ...

#     @typing.overload
#     def __new__(cls, **arguments) -> Decorator[T, _P]:
#         ...

#     @typing.overload
#     def __call__(self, /, set_value: T, **arguments) -> None:
#         ...

#     @typing.overload
#     def __call__(self, **arguments) -> T:
#         ...


# class Decorator(Method[T]):
#     def __call__(self, func: typing.Callable[_P, typing.Union[None, T]]) -> DecoratedMethod[T, _P]:
#         ...


# # def func(set_value, ):
# #     print(func)
# # key_desc = Method()

# # dec_desc = Method()
# # dec_desc


# # # wrapped = dec_desc(func)


# # # wrapped = desc()
# # # wrapped()

# # # desc_key = _MethodDataClass(4)

# # class A:
# #     a=4
# #     pass


# # class B:
# #     b='hi'
# #     pass

# # # # C = Callable[_P, T]
# # # # print(dir(C))
# # import typing
# # from labbench.paramattr import _types
# # from labbench.paramattr._bases import Method
# # class C:
# #     @typing.overload
# #     def __new__(
# #         self,
# #         key: typing.Any,
# #         help: str='',
# #         label: str='',
# #         sets: bool=True,
# #         gets: bool=True,
# #         cache: bool=False,
# #         only: tuple=(),
# #         allow_none: bool=False,
# #         arguments: typing.Dict={}
# #     ) -> A:
# #         ...

# #     @typing.overload
# #     def __new__(
# #         cls,
# #         help: str='',
# #         label: str='',
# #         sets: bool=True,
# #         gets: bool=True,
# #         cache: bool=False,
# #         only: tuple=(),
# #         allow_none: bool=False,
# #         arguments: typing.Dict={}
# #     ) -> B:
# #         ...

# # obj = C(key=4)
