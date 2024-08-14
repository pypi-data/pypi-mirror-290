# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .schema_generation_base_param import SchemaGenerationBaseParam
from .artifact_schema_generation_param import ArtifactSchemaGenerationParam

__all__ = ["TestCaseCreateParams", "TestCaseData"]


class TestCaseCreateParams(TypedDict, total=False):
    schema_type: Required[Literal["GENERATION"]]
    """An enumeration."""

    test_case_data: Required[TestCaseData]
    """The data for the test case in a format matching the provided schema_type"""

    account_id: str
    """The ID of the account that owns the given entity."""

    chat_history: object
    """Used for tracking previous chat interactions for multi-chat test cases"""

    test_case_metadata: object
    """Metadata for the test case"""


TestCaseData: TypeAlias = Union[ArtifactSchemaGenerationParam, SchemaGenerationBaseParam]
