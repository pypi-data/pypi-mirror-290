"""
Implements decorators
"""

import typing
import inspect
import functools
from uuid import uuid4

from aalu.core.worker import schedule_task
from aalu.backends.base import PersistParams


def get_default_dict(func: typing.Callable) -> dict:
    """
    Returns the default args of a function
    """

    signature = inspect.signature(func)
    return {
        k: v.default
        for k, v in signature.parameters.items()
        if v.default is not inspect.Parameter.empty
    }


def get_args_dict(func: typing.Callable, *args) -> dict:
    """
    Returns the default args of a function
    """

    return dict(zip(func.__code__.co_varnames, args))


def get_input_dict(func, *args, **kwargs) -> dict[str, typing.Any]:
    """
    Creates and returns a dictionary with all of the provided args
    and kwargs combined with any unspecified default parameters.
    """
    return {
        **get_default_dict(func),
        **get_args_dict(func, args),
        **kwargs,
    }


T = typing.TypeVar("T")
P = typing.ParamSpec("P")


@typing.overload
def auto_wrapper(
    persist_params: PersistParams,
    target_function: typing.Callable[P, typing.Awaitable[T]],
) -> typing.Callable[P, typing.Awaitable[T]]: ...


@typing.overload
def auto_wrapper(
    persist_params: PersistParams,
    target_function: typing.Callable[P, typing.Generator[T, typing.Any, typing.Any]],
) -> typing.Callable[P, typing.Generator[T, typing.Any, typing.Any]]: ...


@typing.overload
def auto_wrapper(
    persist_params: PersistParams,
    target_function: typing.Callable[P, T],
) -> typing.Callable[P, T]: ...


def auto_wrapper(
    persist_params: PersistParams, target_function: typing.Callable[P, T]
) -> (
    typing.Callable[P, T]
    | typing.Callable[P, typing.Awaitable[T]]
    | typing.Callable[P, typing.Generator[T, typing.Any, typing.Any]]
):
    """
    Dynamically wraps the given function
    """

    is_async = inspect.iscoroutinefunction(target_function)
    is_gener = inspect.isgeneratorfunction(target_function)
    serialized_metadata = persist_params["serializer"](
        "metadata", persist_params["metadata"]
    )
    def_args = get_default_dict(target_function)

    def persist_handler(transaction_id, input_message, output_message):
        """
        Queues all backend persist functions
        """
        for pf in persist_params["persist_funcs"]:
            schedule_task(
                pf,
                (
                    persist_params["namespace"],
                    transaction_id,
                    persist_params["serializer"]("input", {**def_args, **input_message}),
                    persist_params["serializer"]("output", output_message),
                    serialized_metadata,
                ),
            )

    if is_async:

        if is_gener:

            @functools.wraps(target_function)
            async def wrapped_func(*args: P.args, **kwargs: P.kwargs):
                target_result = await typing.cast(
                    typing.Awaitable, target_function(*args, **kwargs)
                )
                output_message = []
                async for result in target_result:
                    output_message.append(result)
                    yield result

                persist_handler(
                    uuid4(),
                    {**get_args_dict(target_function, args), **kwargs},
                    output_message,
                )

            return wrapped_func

        else:

            @functools.wraps(target_function)
            async def wrapped_func(*args: P.args, **kwargs: P.kwargs):
                target_result = await typing.cast(
                    typing.Awaitable, target_function(*args, **kwargs)
                )

                persist_handler(
                    uuid4(),
                    {**get_args_dict(target_function, args), **kwargs},
                    [target_result],
                )

                return target_result

            return wrapped_func

    else:

        if is_gener:

            @functools.wraps(target_function)
            def wrapped_func(*args: P.args, **kwargs: P.kwargs):
                target_result = typing.cast(
                    typing.Generator, target_function(*args, **kwargs)
                )
                output_message = []
                for result in target_result:
                    output_message.append(result)
                    yield result

                persist_handler(
                    uuid4(),
                    {**get_args_dict(target_function, args), **kwargs},
                    output_message,
                )

            return wrapped_func

        else:

            @functools.wraps(target_function)
            def wrapped_func(*args: P.args, **kwargs: P.kwargs):
                target_result = target_function(*args, **kwargs)

                persist_handler(
                    uuid4(),
                    {**get_args_dict(target_function, args), **kwargs},
                    [target_result],
                )

                return target_result

            return wrapped_func
