# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from .._models import BaseModel
from .application_trace_span import ApplicationTraceSpan
from .application_configuration import ApplicationConfiguration
from .applications.application_interaction import ApplicationInteraction

__all__ = [
    "ApplicationTrace",
    "ApplicationVariant",
    "ApplicationVariantConfiguration",
    "ApplicationVariantConfigurationOfflineApplicationConfiguration",
]


class ApplicationVariantConfigurationOfflineApplicationConfiguration(BaseModel):
    metadata: Optional[object] = None
    """User defined metadata about the offline application"""

    output_schema_type: Optional[Literal["completion_only", "context_string", "context_chunks"]] = None
    """An enumeration."""


ApplicationVariantConfiguration: TypeAlias = Union[
    ApplicationConfiguration, ApplicationVariantConfigurationOfflineApplicationConfiguration
]


class ApplicationVariant(BaseModel):
    id: str

    account_id: str
    """The ID of the account that owns the given entity."""

    application_spec_id: str

    configuration: ApplicationVariantConfiguration

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by_user_id: str
    """The user who originally created the entity."""

    name: str

    version: Literal["OFFLINE", "V0"]
    """
    An enum representing the version states of an application and its nodes'
    schemas. Attributes: V0: The initial version of an application schema.
    """

    description: Optional[str] = None
    """Optional description of the application variant"""


class ApplicationTrace(BaseModel):
    application_variant: ApplicationVariant
    """Application variant"""

    interaction: ApplicationInteraction
    """Interaction details"""

    feedback: Optional[Literal["positive", "negative"]] = None
    """An enumeration."""

    feedback_comment: Optional[str] = None
    """Feedback comment"""

    metadata: Optional[object] = None
    """Trace metadata"""

    spans: Optional[List[ApplicationTraceSpan]] = None
    """List of Span IDs belonging to this trace"""

    thread_interactions: Optional[List[ApplicationInteraction]] = None
    """List of interactions in the same thread"""
