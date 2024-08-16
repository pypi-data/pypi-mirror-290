# SPDX-License-Identifier: MIT
# Copyright © 2023-2024 Dylan Baker

"""An implementation of a Result type."""

from __future__ import annotations
from functools import wraps
from typing import TYPE_CHECKING, TypeVar, ParamSpec, Generic
from dataclasses import dataclass

if TYPE_CHECKING:
    from typing import Awaitable, Callable

    from .maybe import Maybe

P = ParamSpec('P')
R = TypeVar('R')
T = TypeVar('T')
U = TypeVar('U')
E = TypeVar('E')
F = TypeVar('F')

__all__ = [
    'Error',
    'ErrorWrapper',
    'Result',
    'Success',
    'UnwrapError',
    'stop',
    'stop_async',
    'unwrap_result',
    'unwrap_result_async',
    'wrap_result',
    'wrap_result_async',
]


class UnwrapError(Exception):
    """Error thrown when unwrapping is invalid."""


class ErrorWrapper(Exception):
    """wraps non Exception Errors"""


class Propagation(Generic[E], Exception):
    """Uses exception handling to propagate up."""

    def __init__(self, err: E) -> None:
        super().__init__('Uncaught Propogation, did you forget to decorate '
                         'function with @simple_monads.result.stop?')
        self.err = err


class Result(Generic[T, E]):

    """Base Class for Option, do not directly instantiate"""

    @staticmethod
    def is_ok() -> bool:
        """Returns True if this is a Success otherwise False."""
        raise NotImplementedError()

    @staticmethod
    def is_err() -> bool:
        """Returns True if this is an Error otherwise False."""
        raise NotImplementedError()

    def unwrap(self, msg: str | None = None) -> T:
        """Get the held value or throw an Exception.

        :param msg: The error message, otherwise a default is used
        :raises UnwrapError: If this is an Err
        :return: The held value
        """
        raise NotImplementedError()

    def unwrap_or(self, fallback: T) -> T:
        """Return the held value or fallback if this is an Error.

        :param fallback: A value to use incase of Error
        :return: The held value or the fallback
        """
        raise NotImplementedError()

    def unwrap_or_else(self, fallback: Callable[[], T]) -> T:
        """Return the held value or the result of the fallback.

        :param fallback: A callable to generate a result if this in Error
        :return: Either the held value or the fallback value
        """
        raise NotImplementedError()

    async def unwrap_or_else_async(self, fallback: Callable[[], Awaitable[T]]) -> T:
        """Return the held value or the result of the fallback.

        >>> import asyncio
        >>> async def fb():
        ...     return 'bar'
        >>> asyncio.run(Success('foo').unwrap_or_else_async(fb))
        'foo'
        >>> asyncio.run(Error(5).unwrap_or_else_async(fb))
        'bar'

        :param fallback: An async callable to generate a result if this in Error
        :return: Either the held value or the fallback value
        """
        raise NotImplementedError()

    def unwrap_err(self, msg: str | None = None) -> E:
        """Return the Error, or throw an UnwrapError

        :param msg: The message to add to the UnwrapError, otherwise a default is used
        :raises UnwrapError: Thrown if this is a Success
        :return: The held error
        """
        raise NotImplementedError()

    def map(self, cb: Callable[[T], U]) -> Result[U, E]:
        """Transform the held value or return the Error unchanged.

        :param cb: A callback taking the held success type and returning a new one
        :return: A result with the transformed Success or an unchanged Error
        """
        raise NotImplementedError()

    async def map_async(self, cb: Callable[[T], Awaitable[U]]) -> Result[U, E]:
        """Transform the held value or return the Error unchanged.

        >>> import asyncio
        >>> async def cb(v: int) -> str:
        ...     return str(v)
        >>> asyncio.run(Success(5).map_async(cb)).unwrap()
        '5'
        >>> asyncio.run(Error('ah!').map_async(cb)).unwrap_err()
        'ah!'

        :param cb: An async callback taking the held success type and returning
            a new one
        :return: A result with the transformed Success or an unchanged Error
        """
        raise NotImplementedError()

    def map_err(self, cb: Callable[[E], F]) -> Result[T, F]:
        """Transform the held error or return the success unchanged.

        :param cb: A callback taking the held error type and returning a new one
        :return: A result with the transformed Error or an unchanged Success
        """
        raise NotImplementedError()

    async def map_err_async(self, cb: Callable[[E], Awaitable[F]]) -> Result[T, F]:
        """Transform the held error or return the success unchanged,
        asynchronously.

        >>> import asyncio
        >>> async def cb(v: str) -> str:
        ...     return 'oh, no! ' + v
        >>> asyncio.run(Success(5).map_err_async(cb)).unwrap()
        5
        >>> asyncio.run(Error('ah!').map_err_async(cb)).unwrap_err()
        'oh, no! ah!'

        :param cb: An asynchronous callback taking the held error type and returning a new one
        :return: A result with the transformed Error or an unchanged Success
        """
        raise NotImplementedError()

    def map_or(self, default: U, cb: Callable[[T], U]) -> U:
        """Transform the held value or return the default.

        :param default: A value to use of Error
        :param cb: A callback to transform the held value of a Success
        :return: The fallback value or the transformed held value
        """
        raise NotImplementedError()

    async def map_or_async(self, default: U, cb: Callable[[T], Awaitable[U]]) -> U:
        """Transform the held value or return the default.

        >>> import asyncio
        >>> async def cb(v: int) -> int:
        ...     return v + 5
        >>> asyncio.run(Success(5).map_or_async(0, cb))
        10
        >>> asyncio.run(Error('ah!').map_or_async(0, cb))
        0

        :param default: A value to use of Error
        :param cb: An async callback to transform the held value of a Success
        :return: The fallback value or the transformed held value
        """
        raise NotImplementedError()

    def map_or_else(self, default: Callable[[], U], cb: Callable[[T], U]) -> U:
        """Transform the held value or return the calculated default

        :param default: A callable returning a value for Error
        :param cb: A callback to transform the held value of a Success
        :return: The fallback value or the transformed held value
        """
        raise NotImplementedError()

    async def map_or_else_async(
            self, default: Callable[[], Awaitable[U]], cb: Callable[[T], Awaitable[U]]) -> U:
        """Transform the held value or return the calculated default

        >>> import asyncio
        >>> async def cb(v: int) -> int:
        ...     return v + 5
        >>> async def fb() -> int:
        ...     return 0
        >>> asyncio.run(Success(5).map_or_else_async(fb, cb))
        10
        >>> asyncio.run(Error('ah!').map_or_else_async(fb, cb))
        0

        :param default: An async callable returning a value for Error
        :param cb: An async callback to transform the held value of a Success
        :return: The fallback value or the transformed held value
        """
        raise NotImplementedError()

    def and_then(self, cb: Callable[[T], Result[U, E]]) -> Result[U, E]:
        """Run the callback if this is a Success, otherwise return the Err unchanged

        :param cb: A callback run on the held value of a Success
        :return: a new Result with a transformed value or the error
        """
        raise NotImplementedError()

    async def and_then_async(self, cb: Callable[[T], Awaitable[Result[U, E]]]) -> Result[U, E]:
        """Run the callback if this is a Success, otherwise return the Err unchanged

        >>> import asyncio
        >>> async def cb(v: int) -> Result[int, E]:
        ...     return Success(v + 5)
        >>> asyncio.run(Success(5).and_then_async(cb)).unwrap()
        10
        >>> asyncio.run(Error('ah').and_then_async(cb)).unwrap_err()
        'ah'

        :param cb: An async callback run on the held value of a Success
        :return: a new Result with a transformed value or the error
        """
        raise NotImplementedError()

    def or_else(self, cb: Callable[[E], Result[T, F]]) -> Result[T, F]:
        """Run the callback if this is an Error, otherwise return the Success unchanged

        :param cb: A callback run on the held value of a Error
        :return: a new Result with a transformed value or the Success
        """
        raise NotImplementedError()

    async def or_else_async(self, cb: Callable[[E], Awaitable[Result[T, F]]]) -> Result[T, F]:
        """Run the callback if this is an Error, otherwise return the Success unchanged

        >>> import asyncio
        >>> async def cb(e: E) -> Result[int, E]:
        ...     return Success(0)
        >>> asyncio.run(Success(5).or_else_async(cb)).unwrap()
        5
        >>> asyncio.run(Error('ah').or_else_async(cb)).unwrap()
        0

        :param cb: An async callback run on the held value of a Error
        :return: a new Result with a transformed value or the Success
        """
        raise NotImplementedError()

    def err(self) -> Maybe[E]:
        """Transform an Result[T, E] into a Maybe[E]

        A Success will be mapped to Nothing[E], while and Error becomes Something[E]

        :return: A Maybe with the error
        """
        raise NotImplementedError()

    def ok(self) -> Maybe[T]:  # pylint: disable=invalid-name
        """Transform an Result[T, E] into a Maybe[T]

        A Success will be mapped to Something[T], while and Error becomes Nothing[T]

        :return: A Maybe with the held value
        """
        raise NotImplementedError()

    def propagate(self) -> T:
        """Get the value, or propagate an error up the stack.

        This is achieved by throwing a special Exception, which is caught using
        the :func:`stop` decorator. This is ugly and an abuse of Exceptions,
        (control flow through Exceptions, which is bad, m'kay?). However, this
        is the only obvious portable way to implement this in Python.

        :return: The held value of a Success

        >>> @stop
        ... def func() -> Result[bool, int]:
        ...     r: Result[str, int] = Error(5)
        ...     x = r.propagate()  # is now str, or thrown
        ...     return x == 'foo'
        ...
        >>> func()
        Error(5)
        """
        raise NotImplementedError()


@dataclass(slots=True, frozen=True)
class Error(Result[T, E]):

    """A Result holding an Error."""

    _held: E

    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:
        return f'Error({self._held!r})'

    @staticmethod
    def is_ok() -> bool:
        return False

    @staticmethod
    def is_err() -> bool:
        return True

    def unwrap(self, msg: str | None = None) -> T:
        e: Exception
        if isinstance(self._held, Exception):
            e = self._held
        else:
            e = ErrorWrapper(self._held)
        raise UnwrapError(msg or 'Attempted to unwrap an Error') from e

    def unwrap_or(self, fallback: T) -> T:
        return fallback

    def unwrap_or_else(self, fallback: Callable[[], T]) -> T:
        return fallback()

    async def unwrap_or_else_async(self, fallback: Callable[[], Awaitable[T]]) -> T:
        return await fallback()

    def unwrap_err(self, msg: str | None = None) -> E:
        return self._held

    def map(self, cb: Callable[[T], U]) -> Result[U, E]:
        return Error(self._held)

    async def map_async(self, cb: Callable[[T], Awaitable[U]]) -> Result[U, E]:
        return Error(self._held)

    def map_err(self, cb: Callable[[E], F]) -> Result[T, F]:
        return Error(cb(self._held))

    async def map_err_async(self, cb: Callable[[E], Awaitable[F]]) -> Result[T, F]:
        return Error(await cb(self._held))

    def map_or(self, default: U, cb: Callable[[T], U]) -> U:
        return default

    async def map_or_async(self, default: U, cb: Callable[[T], Awaitable[U]]) -> U:
        return default

    def map_or_else(self, default: Callable[[], U], cb: Callable[[T], U]) -> U:
        return default()

    async def map_or_else_async(
            self, default: Callable[[], Awaitable[U]], cb: Callable[[T], Awaitable[U]]) -> U:
        return await default()

    def and_then(self, cb: Callable[[T], Result[U, E]]) -> Result[U, E]:
        return Error(self._held)

    async def and_then_async(self, cb: Callable[[T], Awaitable[Result[U, E]]]) -> Result[U, E]:
        return Error(self._held)

    def or_else(self, cb: Callable[[E], Result[T, F]]) -> Result[T, F]:
        return cb(self._held)

    async def or_else_async(self, cb: Callable[[E], Awaitable[Result[T, F]]]) -> Result[T, F]:
        return await cb(self._held)

    def err(self) -> Maybe[E]:
        from .maybe import Something  # pylint: disable=import-outside-toplevel
        return Something(self._held)

    def ok(self) -> Maybe[T]:
        from .maybe import Nothing  # pylint: disable=import-outside-toplevel
        return Nothing()

    def propagate(self) -> T:
        raise Propagation(self._held)


@dataclass(slots=True, frozen=True)
class Success(Result[T, E]):

    """A Result holding an value."""

    _held: T

    def __bool__(self) -> bool:
        return True

    def __repr__(self) -> str:
        return f'Success({self._held!r})'

    @staticmethod
    def is_ok() -> bool:
        return True

    @staticmethod
    def is_err() -> bool:
        return False

    def unwrap(self, msg: str | None = None) -> T:
        return self._held

    def unwrap_or(self, fallback: T) -> T:
        return self._held

    def unwrap_or_else(self, fallback: Callable[[], T]) -> T:
        return self._held

    async def unwrap_or_else_async(self, fallback: Callable[[], Awaitable[T]]) -> T:
        return self._held

    def unwrap_err(self, msg: str | None = None) -> E:
        if msg is None:
            msg = 'Attempted to unwrap the error from a Success'
        raise UnwrapError(msg)

    def map(self, cb: Callable[[T], U]) -> Result[U, E]:
        return Success(cb(self._held))

    async def map_async(self, cb: Callable[[T], Awaitable[U]]) -> Result[U, E]:
        return Success(await cb(self._held))

    def map_err(self, cb: Callable[[E], F]) -> Result[T, F]:
        return Success(self._held)

    async def map_err_async(self, cb: Callable[[E], Awaitable[F]]) -> Result[T, F]:
        return Success(self._held)

    def map_or(self, default: U, cb: Callable[[T], U]) -> U:
        return cb(self._held)

    async def map_or_async(self, default: U, cb: Callable[[T], Awaitable[U]]) -> U:
        return await cb(self._held)

    def map_or_else(self, default: Callable[[], U], cb: Callable[[T], U]) -> U:
        return cb(self._held)

    async def map_or_else_async(
            self, default: Callable[[], Awaitable[U]], cb: Callable[[T], Awaitable[U]]) -> U:
        return await cb(self._held)

    def and_then(self, cb: Callable[[T], Result[U, E]]) -> Result[U, E]:
        return cb(self._held)

    async def and_then_async(self, cb: Callable[[T], Awaitable[Result[U, E]]]) -> Result[U, E]:
        return await cb(self._held)

    def or_else(self, cb: Callable[[E], Result[T, F]]) -> Result[T, F]:
        return Success(self._held)

    async def or_else_async(self, cb: Callable[[E], Awaitable[Result[T, F]]]) -> Result[T, F]:
        return Success(self._held)

    def err(self) -> Maybe[E]:
        from .maybe import Nothing  # pylint: disable=import-outside-toplevel
        return Nothing()

    def ok(self) -> Maybe[T]:
        from .maybe import Something  # pylint: disable=import-outside-toplevel
        return Something(self._held)

    def propagate(self) -> T:
        return self._held


def wrap_result(catch: type[Exception] | tuple[type[Exception], ...] = Exception
                ) -> Callable[[Callable[P, R]], Callable[P, Result[R, Exception]]]:
    """Decorator for wrapping throwing functions to return a Result instead

    This is meant for simple cases only, if you wish to have more complex error
    handling than simply catching all exceptions and putting them in the Result
    you will need to handle that yourself.

    :param f: A callable to wrap
    :param catch: A Exeption or tuple of Exceptions to catch, defaults to Exception
    :return: A result of T or the caught Exception(s) as E
    """

    def wrapper(f: Callable[P, R]) -> Callable[P, Result[R, Exception]]:
        @wraps(f)
        def inner(*args: P.args, **kwargs: P.kwargs) -> Result[R, Exception]:
            try:
                return Success(f(*args, **kwargs))
            except catch as e:  # pylint: disable=broad-exception-caught
                return Error(e)

        return inner

    return wrapper


def wrap_result_async(catch: type[Exception] | tuple[type[Exception], ...] = Exception
                      ) -> Callable[[Callable[P, Awaitable[R]]],
                                     Callable[P, Awaitable[Result[R, Exception]]]]:
    """Decorator for wrapping throwing functions to return a Result instead

    This is meant for simple cases only, if you wish to have more complex error
    handling than simply catching all exceptions and putting them in the Result
    you will need to handle that yourself.

    :param f: A callable to wrap
    :param catch: A Exeption or tuple of Exceptions to catch, defaults to Exception
    :return: A result of T or the caught Exception(s) as E
    """

    def wrapper(f: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[Result[R, Exception]]]:
        @wraps(f)
        async def inner(*args: P.args, **kwargs: P.kwargs) -> Result[R, Exception]:
            try:
                return Success(await f(*args, **kwargs))
            except catch as e:  # pylint: disable=broad-exception-caught
                return Error(e)

        return inner

    return wrapper


def unwrap_result(f: Callable[P, Result[R, E]]) -> Callable[P, R]:
    """Decorator for unwrapping Result returning functions, return the result or
    throwing the Exception.

    This is meant for simple cases only, if you wish to have more complex error
    handling than simply catching all exceptions and putting them in the Result
    you will need to handle that yourself.

    :param f: A callable to unwrap
    :raises ErrorWrapper: if E is not an Exception type
    :raises E: any values of E that Exceptions
    :return: the valu eof a Success
    """

    @wraps(f)
    def inner(*args: P.args, **kwargs: P.kwargs) -> R:
        result = f(*args, **kwargs)
        if result.is_ok():
            return result.unwrap()
        err = result.unwrap_err()
        if isinstance(err, Exception):
            raise err
        raise ErrorWrapper(err)

    return inner


def unwrap_result_async(f: Callable[P, Awaitable[Result[R, E]]]) -> Callable[P, Awaitable[R]]:
    """Decorator for unwrapping Result returning functions, return the result or
    throwing the Exception.

    This is meant for simple cases only, if you wish to have more complex error
    handling than simply catching all exceptions and putting them in the Result
    you will need to handle that yourself.

    :param f: A callable to unwrap
    :raises ErrorWrapper: if E is not an Exception type
    :raises E: any values of E that Exceptions
    :return: the value of a Success
    """

    @wraps(f)
    async def inner(*args: P.args, **kwargs: P.kwargs) -> R:
        result = await f(*args, **kwargs)
        if result.is_ok():
            return result.unwrap()
        err = result.unwrap_err()
        if isinstance(err, Exception):
            raise err
        raise ErrorWrapper(err)

    return inner


def stop(f: Callable[P, Result[R, E]]) -> Callable[P, Result[R, E]]:
    """Decorator for functions that use :meth:`Result.propagate`.

    This is required to catch the propagated Error, and ensure that it is
    returned instead of continuing to go up the stack.

    >>> def g() -> Result[str, str]:
    ...     return Error('err!')

    >>> @stop
    ... def f() -> Result[int, str]:
    ...     v = g()
    ...     v.propagate()
    ...     x = v.map(int)
    ...     return x.map(lambda x: x + 10).map_err(lambda e: 'got: ' + e)

    >>> f()
    Error('err!')

    :param f: The function to wrap
    :return: The original function wrapped to handle Propagation Exceptions
    """

    @wraps(f)
    def inner(*args: P.args, **kwargs: P.kwargs) -> Result[R, E]:
        try:
            return f(*args, **kwargs)
        except Propagation as e:
            return Error(e.err)

    return inner


def stop_async(f: Callable[P, Awaitable[Result[R, E]]]) -> Callable[P, Awaitable[Result[R, E]]]:
    """Decorator for async functions that use :meth:`Result.propagate`.

    This is required to catch the propagated Error, and ensure that it is
    returned instead of continuing to go up the stack.

    >>> async def g() -> Result[str, str]:
    ...     return Error('err!')

    >>> @stop_async
    ... async def f() -> Result[int, str]:
    ...     v = await g()
    ...     v.propagate()
    ...     x = v.map(int)
    ...     return x.map(lambda x: x + 10).map_err(lambda e: 'got: ' + e)

    >>> import asyncio
    >>> asyncio.run(f())
    Error('err!')

    :param f: The async function to wrap
    :return: The original function wrapped to handle Propagation Exceptions
    """

    @wraps(f)
    async def inner(*args: P.args, **kwargs: P.kwargs) -> Result[R, E]:
        try:
            return await f(*args, **kwargs)
        except Propagation as e:
            return Error(e.err)

    return inner
