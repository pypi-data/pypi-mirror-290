# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel
from .application_trace_span import ApplicationTraceSpan
from .application_metric_score import ApplicationMetricScore
from .evaluation_datasets.test_case import TestCase
from .shared.result_schema_generation import ResultSchemaGeneration

__all__ = ["ApplicationTestCaseOutputRetrieveResponse", "Interaction"]


class Interaction(BaseModel):
    id: str

    application_spec_id: str

    application_variant_id: str

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    duration_ms: int
    """How much time the step took in milliseconds(ms)"""

    input: object

    operation_status: Literal["SUCCESS", "ERROR"]
    """An enumeration."""

    output: object

    start_timestamp: datetime

    chat_thread_id: Optional[str] = None

    interaction_source: Optional[Literal["EXTERNAL_AI", "EVALUATION", "SGP_CHAT"]] = None
    """An enumeration."""

    operation_metadata: Optional[object] = None
    """The JSON representation of the metadata insights emitted through the execution.

    This can differ based on different types of operations
    """

    trace_spans: Optional[List[ApplicationTraceSpan]] = None


class ApplicationTestCaseOutputRetrieveResponse(BaseModel):
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

    interaction: Optional[Interaction] = None

    metric_scores: Optional[List[ApplicationMetricScore]] = None

    test_case_version: Optional[TestCase] = None
