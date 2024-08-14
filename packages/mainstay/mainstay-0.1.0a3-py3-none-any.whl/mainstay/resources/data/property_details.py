# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...types.data import property_details_fetch_params
from ..._base_client import make_request_options
from ...types.data.property_details_response import PropertyDetailsResponse

__all__ = ["PropertyDetailsResource", "AsyncPropertyDetailsResource"]


class PropertyDetailsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PropertyDetailsResourceWithRawResponse:
        return PropertyDetailsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PropertyDetailsResourceWithStreamingResponse:
        return PropertyDetailsResourceWithStreamingResponse(self)

    def _fetch(
        self,
        *,
        addresses: Iterable[property_details_fetch_params.Address],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PropertyDetailsResponse:
        """
        Fetch property details for addresses

        Args:
          addresses: An array of address objects, each specifying a property location.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/data/property-details",
            body=maybe_transform({"addresses": addresses}, property_details_fetch_params.PropertyDetailsFetchParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PropertyDetailsResponse,
        )


class AsyncPropertyDetailsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPropertyDetailsResourceWithRawResponse:
        return AsyncPropertyDetailsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPropertyDetailsResourceWithStreamingResponse:
        return AsyncPropertyDetailsResourceWithStreamingResponse(self)

    async def _fetch(
        self,
        *,
        addresses: Iterable[property_details_fetch_params.Address],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PropertyDetailsResponse:
        """
        Fetch property details for addresses

        Args:
          addresses: An array of address objects, each specifying a property location.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/data/property-details",
            body=await async_maybe_transform(
                {"addresses": addresses}, property_details_fetch_params.PropertyDetailsFetchParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PropertyDetailsResponse,
        )


class PropertyDetailsResourceWithRawResponse:
    def __init__(self, property_details: PropertyDetailsResource) -> None:
        self._property_details = property_details

        self._fetch = to_raw_response_wrapper(
            property_details._fetch,
        )


class AsyncPropertyDetailsResourceWithRawResponse:
    def __init__(self, property_details: AsyncPropertyDetailsResource) -> None:
        self._property_details = property_details

        self._fetch = async_to_raw_response_wrapper(
            property_details._fetch,
        )


class PropertyDetailsResourceWithStreamingResponse:
    def __init__(self, property_details: PropertyDetailsResource) -> None:
        self._property_details = property_details

        self._fetch = to_streamed_response_wrapper(
            property_details._fetch,
        )


class AsyncPropertyDetailsResourceWithStreamingResponse:
    def __init__(self, property_details: AsyncPropertyDetailsResource) -> None:
        self._property_details = property_details

        self._fetch = async_to_streamed_response_wrapper(
            property_details._fetch,
        )
