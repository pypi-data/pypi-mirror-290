"""
Implements a Langchain Runnable wrapper
"""

import typing
from uuid import uuid4
from functools import wraps, partial

from jsonalias import Json
from langchain.schema import BaseMessage
from langchain_core.load import dumpd
from langchain_core.runnables import Runnable

from aalu.interface.base import auto_wrapper
from aalu.backends.file import TEMP_FILE_BACKEND
from aalu.backends.base import BaseBackend, PersistParams


function_targets = [
    "batch",
    "stream",
    "invoke",
    "abatch",
    "astream",
    "ainvoke",
    "astream_log",
    "astream_events",
]


def serializer(
    source: typing.Literal["input", "output", "metadata"], arg: typing.Any
) -> Json:
    """
    Makes LLM interactions Serializable
    """
    if source == "output":
        if (
            isinstance(arg, list)
            and all(isinstance(i, BaseMessage) for i in arg)
            and all(i.is_lc_serializable() for i in arg)
        ):
            return typing.cast(Json, [i.to_json() for i in arg])

    return arg


def wrap(
    namespace: str,
    runnables: Runnable | list[Runnable],
    backends: BaseBackend | list[BaseBackend] | None = TEMP_FILE_BACKEND,
    tags: set[str] | None = None,
) -> Runnable:
    """
    Wraps a given Runnable Object and attaches it to given backends
    """

    if isinstance(runnables, list):
        raise NotImplementedError("Routing not supported yet.")

    if backends is None:
        backends = []
    elif isinstance(backends, BaseBackend):
        backends = [backends]

    if tags is None:
        tags = set()

    if backends:
        persist_funcs = [b.persist_pair for b in backends]
        entrypoint_id = uuid4()
        metadata = {"chain_dump": dumpd(runnables), "entrypoint_id": entrypoint_id.hex}
        for pf in persist_funcs:
            pf("entrypoint", entrypoint_id, None, None, metadata)

        for target_name in function_targets:

            persist_params: PersistParams = {
                "metadata": {"entrypoint_id": entrypoint_id.hex, "tags": list(tags)},
                "namespace": namespace,
                "serializer": serializer,
                "persist_funcs": persist_funcs,
            }

            target_func = getattr(runnables, target_name)
            object.__setattr__(
                runnables,
                target_name,
                wraps(target_func)(auto_wrapper(persist_params, target_func)),
            )

    return runnables
