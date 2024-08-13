# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from ..._models import BaseModel
from .application_interaction import ApplicationInteraction

__all__ = ["InteractionListResponse", "Details", "Evaluation"]


class Details(BaseModel):
    feedback_response: Optional[str] = None

    feedback_sentiment: Optional[Literal["positive", "negative"]] = None
    """An enumeration."""

    tokens_used: Optional[int] = None


class Evaluation(BaseModel):
    id: str
    """The unique identifier of the entity."""

    application_interaction_id: str

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    answer_relevance_score: Optional[float] = None

    faithfulness_score: Optional[float] = None


class InteractionListResponse(BaseModel):
    interaction: ApplicationInteraction

    details: Optional[Details] = None

    evaluation: Optional[Evaluation] = None

    grader: Optional[str] = None

    metrics: Optional[List[object]] = None

    variant_name: Optional[str] = None
