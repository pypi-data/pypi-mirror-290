# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .schema_generation_base_param import SchemaGenerationBaseParam
from .artifact_schema_generation_param import ArtifactSchemaGenerationParam

__all__ = ["TestCaseBatchParams", "Item", "ItemTestCaseData"]


class TestCaseBatchParams(TypedDict, total=False):
    items: Required[Iterable[Item]]


ItemTestCaseData: TypeAlias = Union[ArtifactSchemaGenerationParam, SchemaGenerationBaseParam]


class Item(TypedDict, total=False):
    schema_type: Required[Literal["GENERATION"]]
    """An enumeration."""

    test_case_data: Required[ItemTestCaseData]
    """The data for the test case in a format matching the provided schema_type"""

    account_id: str
    """The ID of the account that owns the given entity."""

    chat_history: object
    """Used for tracking previous chat interactions for multi-chat test cases"""

    test_case_metadata: object
    """Metadata for the test case"""
