"""
Implements a backend that saves the interactions to a file
"""

import os
import json
import typing
import tempfile
from uuid import UUID

from loguru import logger
from jsonalias import Json
from smart_open import parse_uri, open as smart_open

from aalu.backends.base import BaseBackend


class FileBackend(BaseBackend):
    """
    Implements a backend to store interactions to a file
    """

    path: str
    transport_params: dict[str, typing.Any] | None = None

    def model_post_init(self, __context: typing.Any) -> None:
        logger.info(f"Storing interactions to {self.path}")
        return super().model_post_init(__context)

    def persist_pair(
        self,
        namespace: str,
        interaction_id: UUID,
        input_message: Json,
        output_message: Json,
        metadata: Json = None,
    ) -> None:
        persist_path = os.path.join(self.path, namespace)
        persist_file = os.path.join(persist_path, f"{interaction_id.hex}.json")

        if parse_uri(persist_path).scheme == "file":
            os.makedirs(persist_path, exist_ok=True)
        with smart_open(
            persist_file, "w", transport_params=self.transport_params
        ) as fout:
            fout.write(
                json.dumps(
                    {
                        "input": input_message,
                        "output": output_message,
                        "metadata": metadata,
                        "backend_tags": list(self.tags),
                    }
                )
            )


TEMP_FILE_BACKEND = FileBackend(
    path=tempfile.TemporaryDirectory().name, tags={"DEFAULT_LOCAL_FILE_BACKEND"}
)
