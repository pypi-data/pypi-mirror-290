# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional

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
from ...types.data import rental_comps_fetch_params
from ..._base_client import make_request_options
from ...types.data.rental_comps_response import RentalCompsResponse

__all__ = ["RentalCompsResource", "AsyncRentalCompsResource"]


class RentalCompsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> RentalCompsResourceWithRawResponse:
        return RentalCompsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RentalCompsResourceWithStreamingResponse:
        return RentalCompsResourceWithStreamingResponse(self)

    def _fetch(
        self,
        *,
        addresses: Iterable[rental_comps_fetch_params.Address],
        filters: Optional[rental_comps_fetch_params.Filters] | NotGiven = NOT_GIVEN,
        num_comps: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> RentalCompsResponse:
        """
        Fetch rental comps for addresses

        Args:
          addresses: An array of address objects, each specifying a property location.

          filters: An _optional_ object containing criteria to refine the rental comps search, such
              as date range, price, number of bedrooms, etc. If no filters are provided, the
              search will include all available comps.

          num_comps: An _optional_ int containing the number of rental comps to return per subject
              address. The minimum value is 1 and the maximum value is 50. If no value is
              provided, we will return our top 10 comps.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/data/rental-comps",
            body=maybe_transform(
                {
                    "addresses": addresses,
                    "filters": filters,
                    "num_comps": num_comps,
                },
                rental_comps_fetch_params.RentalCompsFetchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RentalCompsResponse,
        )


class AsyncRentalCompsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncRentalCompsResourceWithRawResponse:
        return AsyncRentalCompsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRentalCompsResourceWithStreamingResponse:
        return AsyncRentalCompsResourceWithStreamingResponse(self)

    async def _fetch(
        self,
        *,
        addresses: Iterable[rental_comps_fetch_params.Address],
        filters: Optional[rental_comps_fetch_params.Filters] | NotGiven = NOT_GIVEN,
        num_comps: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> RentalCompsResponse:
        """
        Fetch rental comps for addresses

        Args:
          addresses: An array of address objects, each specifying a property location.

          filters: An _optional_ object containing criteria to refine the rental comps search, such
              as date range, price, number of bedrooms, etc. If no filters are provided, the
              search will include all available comps.

          num_comps: An _optional_ int containing the number of rental comps to return per subject
              address. The minimum value is 1 and the maximum value is 50. If no value is
              provided, we will return our top 10 comps.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/data/rental-comps",
            body=await async_maybe_transform(
                {
                    "addresses": addresses,
                    "filters": filters,
                    "num_comps": num_comps,
                },
                rental_comps_fetch_params.RentalCompsFetchParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=RentalCompsResponse,
        )


class RentalCompsResourceWithRawResponse:
    def __init__(self, rental_comps: RentalCompsResource) -> None:
        self._rental_comps = rental_comps

        self._fetch = to_raw_response_wrapper(
            rental_comps._fetch,
        )


class AsyncRentalCompsResourceWithRawResponse:
    def __init__(self, rental_comps: AsyncRentalCompsResource) -> None:
        self._rental_comps = rental_comps

        self._fetch = async_to_raw_response_wrapper(
            rental_comps._fetch,
        )


class RentalCompsResourceWithStreamingResponse:
    def __init__(self, rental_comps: RentalCompsResource) -> None:
        self._rental_comps = rental_comps

        self._fetch = to_streamed_response_wrapper(
            rental_comps._fetch,
        )


class AsyncRentalCompsResourceWithStreamingResponse:
    def __init__(self, rental_comps: AsyncRentalCompsResource) -> None:
        self._rental_comps = rental_comps

        self._fetch = async_to_streamed_response_wrapper(
            rental_comps._fetch,
        )
