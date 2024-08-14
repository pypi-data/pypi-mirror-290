# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

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
from ....types.chat_threads.messages import feedback_update_params
from ....types.applications.chat_threads.chat_thread_feedback import ChatThreadFeedback

__all__ = ["FeedbackResource", "AsyncFeedbackResource"]


class FeedbackResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> FeedbackResourceWithRawResponse:
        return FeedbackResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> FeedbackResourceWithStreamingResponse:
        return FeedbackResourceWithStreamingResponse(self)

    def update(
        self,
        *,
        thread_id: str,
        path_application_interaction_id: str,
        body_application_interaction_id: str,
        chat_thread_id: str,
        description: str,
        sentiment: Literal["positive", "negative"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChatThreadFeedback:
        """
        Add Feedback To Thread Entry

        Args:
          sentiment: An enumeration.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not thread_id:
            raise ValueError(f"Expected a non-empty value for `thread_id` but received {thread_id!r}")
        if not path_application_interaction_id:
            raise ValueError(
                f"Expected a non-empty value for `path_application_interaction_id` but received {path_application_interaction_id!r}"
            )
        return self._put(
            f"/v4/threads/{thread_id}/messages/{path_application_interaction_id}/feedback",
            body=maybe_transform(
                {
                    "application_interaction_id": body_application_interaction_id,
                    "chat_thread_id": chat_thread_id,
                    "description": description,
                    "sentiment": sentiment,
                },
                feedback_update_params.FeedbackUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChatThreadFeedback,
        )

    def delete(
        self,
        application_interaction_id: str,
        *,
        thread_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Delete Interaction Feedback

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not thread_id:
            raise ValueError(f"Expected a non-empty value for `thread_id` but received {thread_id!r}")
        if not application_interaction_id:
            raise ValueError(
                f"Expected a non-empty value for `application_interaction_id` but received {application_interaction_id!r}"
            )
        return self._delete(
            f"/v4/threads/{thread_id}/messages/{application_interaction_id}/feedback",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class AsyncFeedbackResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncFeedbackResourceWithRawResponse:
        return AsyncFeedbackResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncFeedbackResourceWithStreamingResponse:
        return AsyncFeedbackResourceWithStreamingResponse(self)

    async def update(
        self,
        *,
        thread_id: str,
        path_application_interaction_id: str,
        body_application_interaction_id: str,
        chat_thread_id: str,
        description: str,
        sentiment: Literal["positive", "negative"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChatThreadFeedback:
        """
        Add Feedback To Thread Entry

        Args:
          sentiment: An enumeration.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not thread_id:
            raise ValueError(f"Expected a non-empty value for `thread_id` but received {thread_id!r}")
        if not path_application_interaction_id:
            raise ValueError(
                f"Expected a non-empty value for `path_application_interaction_id` but received {path_application_interaction_id!r}"
            )
        return await self._put(
            f"/v4/threads/{thread_id}/messages/{path_application_interaction_id}/feedback",
            body=await async_maybe_transform(
                {
                    "application_interaction_id": body_application_interaction_id,
                    "chat_thread_id": chat_thread_id,
                    "description": description,
                    "sentiment": sentiment,
                },
                feedback_update_params.FeedbackUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChatThreadFeedback,
        )

    async def delete(
        self,
        application_interaction_id: str,
        *,
        thread_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> object:
        """
        Delete Interaction Feedback

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not thread_id:
            raise ValueError(f"Expected a non-empty value for `thread_id` but received {thread_id!r}")
        if not application_interaction_id:
            raise ValueError(
                f"Expected a non-empty value for `application_interaction_id` but received {application_interaction_id!r}"
            )
        return await self._delete(
            f"/v4/threads/{thread_id}/messages/{application_interaction_id}/feedback",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=object,
        )


class FeedbackResourceWithRawResponse:
    def __init__(self, feedback: FeedbackResource) -> None:
        self._feedback = feedback

        self.update = to_raw_response_wrapper(
            feedback.update,
        )
        self.delete = to_raw_response_wrapper(
            feedback.delete,
        )


class AsyncFeedbackResourceWithRawResponse:
    def __init__(self, feedback: AsyncFeedbackResource) -> None:
        self._feedback = feedback

        self.update = async_to_raw_response_wrapper(
            feedback.update,
        )
        self.delete = async_to_raw_response_wrapper(
            feedback.delete,
        )


class FeedbackResourceWithStreamingResponse:
    def __init__(self, feedback: FeedbackResource) -> None:
        self._feedback = feedback

        self.update = to_streamed_response_wrapper(
            feedback.update,
        )
        self.delete = to_streamed_response_wrapper(
            feedback.delete,
        )


class AsyncFeedbackResourceWithStreamingResponse:
    def __init__(self, feedback: AsyncFeedbackResource) -> None:
        self._feedback = feedback

        self.update = async_to_streamed_response_wrapper(
            feedback.update,
        )
        self.delete = async_to_streamed_response_wrapper(
            feedback.delete,
        )
