# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ...._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ...._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ...._compat import cached_property
from ...._resource import SyncAPIResource, AsyncAPIResource
from ...._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...._base_client import make_request_options
from ....types.application_trace import ApplicationTrace
from ....types.applications.interactions import span_retrieve_params

__all__ = ["SpansResource", "AsyncSpansResource"]


class SpansResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SpansResourceWithRawResponse:
        return SpansResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SpansResourceWithStreamingResponse:
        return SpansResourceWithStreamingResponse(self)

    def retrieve(
        self,
        application_interaction_id: str,
        *,
        application_spec_id: str,
        account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ApplicationTrace:
        """
        Get Application Interaction Spans

        Args:
          account_id: Account ID used for authorization

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_spec_id:
            raise ValueError(
                f"Expected a non-empty value for `application_spec_id` but received {application_spec_id!r}"
            )
        if not application_interaction_id:
            raise ValueError(
                f"Expected a non-empty value for `application_interaction_id` but received {application_interaction_id!r}"
            )
        return self._get(
            f"/v4/applications/{application_spec_id}/interactions/{application_interaction_id}/spans",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform({"account_id": account_id}, span_retrieve_params.SpanRetrieveParams),
            ),
            cast_to=ApplicationTrace,
        )


class AsyncSpansResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSpansResourceWithRawResponse:
        return AsyncSpansResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSpansResourceWithStreamingResponse:
        return AsyncSpansResourceWithStreamingResponse(self)

    async def retrieve(
        self,
        application_interaction_id: str,
        *,
        application_spec_id: str,
        account_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ApplicationTrace:
        """
        Get Application Interaction Spans

        Args:
          account_id: Account ID used for authorization

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_spec_id:
            raise ValueError(
                f"Expected a non-empty value for `application_spec_id` but received {application_spec_id!r}"
            )
        if not application_interaction_id:
            raise ValueError(
                f"Expected a non-empty value for `application_interaction_id` but received {application_interaction_id!r}"
            )
        return await self._get(
            f"/v4/applications/{application_spec_id}/interactions/{application_interaction_id}/spans",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform({"account_id": account_id}, span_retrieve_params.SpanRetrieveParams),
            ),
            cast_to=ApplicationTrace,
        )


class SpansResourceWithRawResponse:
    def __init__(self, spans: SpansResource) -> None:
        self._spans = spans

        self.retrieve = to_raw_response_wrapper(
            spans.retrieve,
        )


class AsyncSpansResourceWithRawResponse:
    def __init__(self, spans: AsyncSpansResource) -> None:
        self._spans = spans

        self.retrieve = async_to_raw_response_wrapper(
            spans.retrieve,
        )


class SpansResourceWithStreamingResponse:
    def __init__(self, spans: SpansResource) -> None:
        self._spans = spans

        self.retrieve = to_streamed_response_wrapper(
            spans.retrieve,
        )


class AsyncSpansResourceWithStreamingResponse:
    def __init__(self, spans: AsyncSpansResource) -> None:
        self._spans = spans

        self.retrieve = async_to_streamed_response_wrapper(
            spans.retrieve,
        )
