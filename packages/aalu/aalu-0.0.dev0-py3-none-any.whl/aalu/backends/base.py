"""
Implements all base classes for backends
"""

import typing
from uuid import UUID
from abc import ABC, abstractmethod

from pydantic import BaseModel
from jsonalias import Json


class PersistParams(typing.TypedDict):
    """
    Defines the parameters needed for persustence
    """

    namespace: str
    serializer: typing.Callable[
        [typing.Literal["input", "output", "metadata"], typing.Any], Json
    ]
    persist_funcs: list[typing.Callable]
    metadata: Json


class BaseBackend(ABC, BaseModel):
    """
    Base Class for all backends
    """

    tags: set[str]

    @abstractmethod
    def persist_pair(
        self,
        namespace: str,
        interaction_id: UUID,
        input_message: Json,
        output_message: Json,
        metadata: Json = None,
    ) -> None:
        """
        Implements signature to persist interaction
        """
