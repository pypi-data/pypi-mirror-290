# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from typing_extensions import Required, TypeAlias, TypedDict

from ...types import shared_params

__all__ = ["ArtifactSchemaGenerationParam", "ExpectedExtraInfo"]

ExpectedExtraInfo: TypeAlias = Union[shared_params.ChunkExtraInfoSchema, shared_params.StringExtraInfoSchema]


class ArtifactSchemaGenerationParam(TypedDict, total=False):
    artifact_ids_filter: Required[List[str]]

    input: Required[str]

    expected_extra_info: ExpectedExtraInfo

    expected_output: str
