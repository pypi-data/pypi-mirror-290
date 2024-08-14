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
from ...types.data import crime_data_fetch_params
from ..._base_client import make_request_options
from ...types.data.crime_data_response import CrimeDataResponse

__all__ = ["CrimeDataResource", "AsyncCrimeDataResource"]


class CrimeDataResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CrimeDataResourceWithRawResponse:
        return CrimeDataResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CrimeDataResourceWithStreamingResponse:
        return CrimeDataResourceWithStreamingResponse(self)

    def _fetch(
        self,
        *,
        addresses: Iterable[crime_data_fetch_params.Address],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CrimeDataResponse:
        """
        Fetch crime percentile rankings for county and nation

        Args:
          addresses: An array of address objects, each specifying a property location.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/data/crime-data",
            body=maybe_transform({"addresses": addresses}, crime_data_fetch_params.CrimeDataFetchParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CrimeDataResponse,
        )


class AsyncCrimeDataResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCrimeDataResourceWithRawResponse:
        return AsyncCrimeDataResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCrimeDataResourceWithStreamingResponse:
        return AsyncCrimeDataResourceWithStreamingResponse(self)

    async def _fetch(
        self,
        *,
        addresses: Iterable[crime_data_fetch_params.Address],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CrimeDataResponse:
        """
        Fetch crime percentile rankings for county and nation

        Args:
          addresses: An array of address objects, each specifying a property location.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/data/crime-data",
            body=await async_maybe_transform({"addresses": addresses}, crime_data_fetch_params.CrimeDataFetchParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CrimeDataResponse,
        )


class CrimeDataResourceWithRawResponse:
    def __init__(self, crime_data: CrimeDataResource) -> None:
        self._crime_data = crime_data

        self._fetch = to_raw_response_wrapper(
            crime_data._fetch,
        )


class AsyncCrimeDataResourceWithRawResponse:
    def __init__(self, crime_data: AsyncCrimeDataResource) -> None:
        self._crime_data = crime_data

        self._fetch = async_to_raw_response_wrapper(
            crime_data._fetch,
        )


class CrimeDataResourceWithStreamingResponse:
    def __init__(self, crime_data: CrimeDataResource) -> None:
        self._crime_data = crime_data

        self._fetch = to_streamed_response_wrapper(
            crime_data._fetch,
        )


class AsyncCrimeDataResourceWithStreamingResponse:
    def __init__(self, crime_data: AsyncCrimeDataResource) -> None:
        self._crime_data = crime_data

        self._fetch = async_to_streamed_response_wrapper(
            crime_data._fetch,
        )
