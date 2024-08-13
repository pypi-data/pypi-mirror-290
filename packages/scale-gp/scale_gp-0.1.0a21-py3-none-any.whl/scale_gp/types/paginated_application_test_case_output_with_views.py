# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel
from .application_metric_score import ApplicationMetricScore
from .evaluation_datasets.test_case import TestCase
from .shared.result_schema_generation import ResultSchemaGeneration
from .applications.application_interaction_with_spans import ApplicationInteractionWithSpans

__all__ = ["PaginatedApplicationTestCaseOutputWithViews", "Item"]


class Item(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    application_variant_id: str

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    evaluation_dataset_id: str

    output: ResultSchemaGeneration

    schema_type: Literal["GENERATION"]
    """An enumeration."""

    test_case_id: str

    application_interaction_id: Optional[str] = None

    interaction: Optional[ApplicationInteractionWithSpans] = None

    metric_scores: Optional[List[ApplicationMetricScore]] = None

    test_case_version: Optional[TestCase] = None


class PaginatedApplicationTestCaseOutputWithViews(BaseModel):
    current_page: int
    """The current page number."""

    items: List[Item]
    """The data returned for the current page."""

    items_per_page: int
    """The number of items per page."""

    total_item_count: int
    """The total number of items of the query"""
