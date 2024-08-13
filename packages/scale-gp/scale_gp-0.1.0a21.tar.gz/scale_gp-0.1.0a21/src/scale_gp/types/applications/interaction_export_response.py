# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from ..application_interaction_export import ApplicationInteractionExport

__all__ = ["InteractionExportResponse"]

InteractionExportResponse: TypeAlias = List[ApplicationInteractionExport]
