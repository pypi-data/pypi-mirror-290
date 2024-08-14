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
from ...types.data import rent_estimates_fetch_params
from ..._base_client import make_request_options
from ...types.data.rent_estimates_response import RentEstimatesResponse

__all__ = ["RentEstimatesResource", "AsyncRentEstimatesResource"]


class RentEstimatesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> RentEstimatesResourceWithRawResponse:
        return RentEstimatesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RentEstimatesResourceWithStreamingResponse:
        return RentEstimatesResourceWithStreamingResponse(self)

    def _fetch(
        self,
        *,
        addresses: Iterable[rent_estimates_fetch_params.Address],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> RentEstimatesResponse:
        """
        Fetch rent estimates for addresses

        Args:
          addresses: An array of address objects, each specifying a property location.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/data/rent-estimates",
            body=maybe_transform({"addresses": addresses}, rent_estimates_fetch_params.RentEstimatesFetchParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RentEstimatesResponse,
        )


class AsyncRentEstimatesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncRentEstimatesResourceWithRawResponse:
        return AsyncRentEstimatesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRentEstimatesResourceWithStreamingResponse:
        return AsyncRentEstimatesResourceWithStreamingResponse(self)

    async def _fetch(
        self,
        *,
        addresses: Iterable[rent_estimates_fetch_params.Address],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> RentEstimatesResponse:
        """
        Fetch rent estimates for addresses

        Args:
          addresses: An array of address objects, each specifying a property location.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/data/rent-estimates",
            body=await async_maybe_transform(
                {"addresses": addresses}, rent_estimates_fetch_params.RentEstimatesFetchParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RentEstimatesResponse,
        )


class RentEstimatesResourceWithRawResponse:
    def __init__(self, rent_estimates: RentEstimatesResource) -> None:
        self._rent_estimates = rent_estimates

        self._fetch = to_raw_response_wrapper(
            rent_estimates._fetch,
        )


class AsyncRentEstimatesResourceWithRawResponse:
    def __init__(self, rent_estimates: AsyncRentEstimatesResource) -> None:
        self._rent_estimates = rent_estimates

        self._fetch = async_to_raw_response_wrapper(
            rent_estimates._fetch,
        )


class RentEstimatesResourceWithStreamingResponse:
    def __init__(self, rent_estimates: RentEstimatesResource) -> None:
        self._rent_estimates = rent_estimates

        self._fetch = to_streamed_response_wrapper(
            rent_estimates._fetch,
        )


class AsyncRentEstimatesResourceWithStreamingResponse:
    def __init__(self, rent_estimates: AsyncRentEstimatesResource) -> None:
        self._rent_estimates = rent_estimates

        self._fetch = async_to_streamed_response_wrapper(
            rent_estimates._fetch,
        )
