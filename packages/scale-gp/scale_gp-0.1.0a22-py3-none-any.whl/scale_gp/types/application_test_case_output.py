# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel
from .shared.result_schema_generation import ResultSchemaGeneration

__all__ = ["ApplicationTestCaseOutput"]


class ApplicationTestCaseOutput(BaseModel):
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
