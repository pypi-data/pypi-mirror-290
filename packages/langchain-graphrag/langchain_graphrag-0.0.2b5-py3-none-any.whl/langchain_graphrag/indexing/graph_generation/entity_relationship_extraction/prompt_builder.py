from pathlib import Path
from typing import Any

from langchain_core.prompts import BasePromptTemplate, PromptTemplate
from typing_extensions import Unpack

from langchain_graphrag.types.prompts import PromptBuilder

from .default_prompts import DEFAULT_ER_EXTRACTION_PROMPT

DEFAULT_TUPLE_DELIMITER = "<|>"
DEFAULT_RECORD_DELIMITER = "##"
DEFAULT_COMPLETION_DELIMITER = "<|COMPLETE|>"
DEFAULT_ENTITY_TYPES = ["organization", "person", "geo", "event"]


class EntityExtractionPromptBuilder(PromptBuilder):
    def __init__(
        self,
        *,
        prompt: str | None = None,
        prompt_path: Path | None = None,
        entity_types: list[str] = DEFAULT_ENTITY_TYPES,
        tuple_delimiter: str = DEFAULT_TUPLE_DELIMITER,
        record_delimiter: str = DEFAULT_RECORD_DELIMITER,
        completion_delimiter: str = DEFAULT_COMPLETION_DELIMITER,
    ):
        self._prompt: str | None
        if prompt is None and prompt_path is None:
            self._prompt = DEFAULT_ER_EXTRACTION_PROMPT
        else:
            self._prompt = prompt

        self._prompt_path = prompt_path

        self._entity_types = entity_types
        self._tuple_delimiter = tuple_delimiter
        self._record_delimiter = record_delimiter
        self._completion_delimiter = completion_delimiter

    def build(self) -> BasePromptTemplate:
        if self._prompt:
            prompt_template = PromptTemplate.from_template(self._prompt)
        else:
            assert self._prompt_path is not None
            prompt_template = PromptTemplate.from_file(self._prompt_path)

        return prompt_template.partial(
            completion_delimiter=self._completion_delimiter,
            tuple_delimiter=self._tuple_delimiter,
            record_delimiter=self._record_delimiter,
            entity_types=",".join(self._entity_types),
        )

    def prepare_chain_input(self, **kwargs: Unpack[dict[str, Any]]) -> dict[str, str]:
        text: str = kwargs.get("text", None)
        if text is None:
            raise ValueError("text is required")

        return dict(input_text=text)
