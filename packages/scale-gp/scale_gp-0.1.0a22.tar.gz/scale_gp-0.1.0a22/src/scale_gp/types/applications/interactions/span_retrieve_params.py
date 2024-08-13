# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["SpanRetrieveParams"]


class SpanRetrieveParams(TypedDict, total=False):
    application_spec_id: Required[str]

    account_id: str
    """Account ID used for authorization"""
