# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Required, TypeAlias, TypedDict

from ...types import shared_params

__all__ = ["ResultSchemaGeneration", "GenerationExtraInfo"]

GenerationExtraInfo: TypeAlias = Union[shared_params.ChunkExtraInfoSchema, shared_params.StringExtraInfoSchema]


class ResultSchemaGeneration(TypedDict, total=False):
    generation_output: Required[str]

    generation_extra_info: GenerationExtraInfo
