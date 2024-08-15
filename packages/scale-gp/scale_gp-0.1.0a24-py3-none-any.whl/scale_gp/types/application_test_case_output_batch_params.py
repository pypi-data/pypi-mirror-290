# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, TypedDict

from .shared_params.result_schema_generation import ResultSchemaGeneration

__all__ = ["ApplicationTestCaseOutputBatchParams", "Item"]


class ApplicationTestCaseOutputBatchParams(TypedDict, total=False):
    items: Required[Iterable[Item]]


class Item(TypedDict, total=False):
    account_id: Required[str]
    """The ID of the account that owns the given entity."""

    application_variant_id: Required[str]

    evaluation_dataset_version_num: Required[int]

    output: Required[ResultSchemaGeneration]

    schema_type: Required[Literal["GENERATION"]]
    """An enumeration."""

    test_case_id: Required[str]

    application_interaction_id: str
