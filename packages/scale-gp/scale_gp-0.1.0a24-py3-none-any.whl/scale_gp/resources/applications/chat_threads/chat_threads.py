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
from ....pagination import SyncTopLevelArray, AsyncTopLevelArray
from ...._base_client import AsyncPaginator, make_request_options
from ....types.chat_thread import ChatThread
from ....types.applications import chat_thread_create_params

__all__ = ["ChatThreadsResource", "AsyncChatThreadsResource"]


class ChatThreadsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ChatThreadsResourceWithRawResponse:
        return ChatThreadsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ChatThreadsResourceWithStreamingResponse:
        return ChatThreadsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        path_application_variant_id: str,
        account_id: str,
        body_application_variant_id: str,
        title: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChatThread:
        """
        Create New Application Thread

        Args:
          account_id: The ID of the account that owns the given entity.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not path_application_variant_id:
            raise ValueError(
                f"Expected a non-empty value for `path_application_variant_id` but received {path_application_variant_id!r}"
            )
        return self._post(
            f"/v4/applications/{path_application_variant_id}/threads",
            body=maybe_transform(
                {
                    "account_id": account_id,
                    "application_variant_id": body_application_variant_id,
                    "title": title,
                },
                chat_thread_create_params.ChatThreadCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChatThread,
        )

    def list(
        self,
        application_variant_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncTopLevelArray[ChatThread]:
        """
        List Application Threads

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_variant_id:
            raise ValueError(
                f"Expected a non-empty value for `application_variant_id` but received {application_variant_id!r}"
            )
        return self._get_api_list(
            f"/v4/applications/{application_variant_id}/threads",
            page=SyncTopLevelArray[ChatThread],
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            model=ChatThread,
        )


class AsyncChatThreadsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncChatThreadsResourceWithRawResponse:
        return AsyncChatThreadsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncChatThreadsResourceWithStreamingResponse:
        return AsyncChatThreadsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        path_application_variant_id: str,
        account_id: str,
        body_application_variant_id: str,
        title: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ChatThread:
        """
        Create New Application Thread

        Args:
          account_id: The ID of the account that owns the given entity.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not path_application_variant_id:
            raise ValueError(
                f"Expected a non-empty value for `path_application_variant_id` but received {path_application_variant_id!r}"
            )
        return await self._post(
            f"/v4/applications/{path_application_variant_id}/threads",
            body=await async_maybe_transform(
                {
                    "account_id": account_id,
                    "application_variant_id": body_application_variant_id,
                    "title": title,
                },
                chat_thread_create_params.ChatThreadCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChatThread,
        )

    def list(
        self,
        application_variant_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[ChatThread, AsyncTopLevelArray[ChatThread]]:
        """
        List Application Threads

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_variant_id:
            raise ValueError(
                f"Expected a non-empty value for `application_variant_id` but received {application_variant_id!r}"
            )
        return self._get_api_list(
            f"/v4/applications/{application_variant_id}/threads",
            page=AsyncTopLevelArray[ChatThread],
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            model=ChatThread,
        )


class ChatThreadsResourceWithRawResponse:
    def __init__(self, chat_threads: ChatThreadsResource) -> None:
        self._chat_threads = chat_threads

        self.create = to_raw_response_wrapper(
            chat_threads.create,
        )
        self.list = to_raw_response_wrapper(
            chat_threads.list,
        )


class AsyncChatThreadsResourceWithRawResponse:
    def __init__(self, chat_threads: AsyncChatThreadsResource) -> None:
        self._chat_threads = chat_threads

        self.create = async_to_raw_response_wrapper(
            chat_threads.create,
        )
        self.list = async_to_raw_response_wrapper(
            chat_threads.list,
        )


class ChatThreadsResourceWithStreamingResponse:
    def __init__(self, chat_threads: ChatThreadsResource) -> None:
        self._chat_threads = chat_threads

        self.create = to_streamed_response_wrapper(
            chat_threads.create,
        )
        self.list = to_streamed_response_wrapper(
            chat_threads.list,
        )


class AsyncChatThreadsResourceWithStreamingResponse:
    def __init__(self, chat_threads: AsyncChatThreadsResource) -> None:
        self._chat_threads = chat_threads

        self.create = async_to_streamed_response_wrapper(
            chat_threads.create,
        )
        self.list = async_to_streamed_response_wrapper(
            chat_threads.list,
        )
