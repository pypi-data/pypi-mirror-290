# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from mainstay import Mainstay, AsyncMainstay
from tests.utils import assert_matches_type
from mainstay._utils import parse_date
from mainstay.types.data import RentalCompsResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestRentalComps:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_fetch(self, client: Mainstay) -> None:
        rental_comps = client.data.rental_comps._fetch(
            addresses=[
                {
                    "street": "14042 Kenyte Row",
                    "city": "San Antonio",
                    "state": "TX",
                    "postal_code": "78253",
                }
            ],
        )
        assert_matches_type(RentalCompsResponse, rental_comps, path=["response"])

    @parametrize
    def test_method_fetch_with_all_params(self, client: Mainstay) -> None:
        rental_comps = client.data.rental_comps._fetch(
            addresses=[
                {
                    "street": "14042 Kenyte Row",
                    "city": "San Antonio",
                    "state": "TX",
                    "postal_code": "78253",
                    "unit": "",
                    "token": "123",
                }
            ],
            filters={
                "ownership_profiles": ["<100", "100-1k", "1k-20k"],
                "structure_types": ["single_family", "multi_family", "townhouse"],
                "beds": {
                    "min": 0,
                    "max": 0,
                },
                "bedrooms_total": {
                    "min": 0,
                    "max": 0,
                },
                "baths": {
                    "min": 0,
                    "max": 0,
                },
                "bathrooms_full": {
                    "min": 0,
                    "max": 0,
                },
                "bathrooms_half": {
                    "min": 0,
                    "max": 0,
                },
                "distance": 0,
                "min_similarity_score": 0,
                "living_area_sqft": {
                    "min": 0,
                    "max": 0,
                },
                "date": {
                    "min": parse_date("2019-12-27"),
                    "max": parse_date("2019-12-27"),
                },
                "year_built": {
                    "min": 0,
                    "max": 0,
                },
                "statuses": ["active", "removed", "closed"],
            },
            num_comps=0,
        )
        assert_matches_type(RentalCompsResponse, rental_comps, path=["response"])

    @parametrize
    def test_raw_response_fetch(self, client: Mainstay) -> None:
        response = client.data.rental_comps.with_raw_response._fetch(
            addresses=[
                {
                    "street": "14042 Kenyte Row",
                    "city": "San Antonio",
                    "state": "TX",
                    "postal_code": "78253",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rental_comps = response.parse()
        assert_matches_type(RentalCompsResponse, rental_comps, path=["response"])

    @parametrize
    def test_streaming_response_fetch(self, client: Mainstay) -> None:
        with client.data.rental_comps.with_streaming_response._fetch(
            addresses=[
                {
                    "street": "14042 Kenyte Row",
                    "city": "San Antonio",
                    "state": "TX",
                    "postal_code": "78253",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rental_comps = response.parse()
            assert_matches_type(RentalCompsResponse, rental_comps, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncRentalComps:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_fetch(self, async_client: AsyncMainstay) -> None:
        rental_comps = await async_client.data.rental_comps._fetch(
            addresses=[
                {
                    "street": "14042 Kenyte Row",
                    "city": "San Antonio",
                    "state": "TX",
                    "postal_code": "78253",
                }
            ],
        )
        assert_matches_type(RentalCompsResponse, rental_comps, path=["response"])

    @parametrize
    async def test_method_fetch_with_all_params(self, async_client: AsyncMainstay) -> None:
        rental_comps = await async_client.data.rental_comps._fetch(
            addresses=[
                {
                    "street": "14042 Kenyte Row",
                    "city": "San Antonio",
                    "state": "TX",
                    "postal_code": "78253",
                    "unit": "",
                    "token": "123",
                }
            ],
            filters={
                "ownership_profiles": ["<100", "100-1k", "1k-20k"],
                "structure_types": ["single_family", "multi_family", "townhouse"],
                "beds": {
                    "min": 0,
                    "max": 0,
                },
                "bedrooms_total": {
                    "min": 0,
                    "max": 0,
                },
                "baths": {
                    "min": 0,
                    "max": 0,
                },
                "bathrooms_full": {
                    "min": 0,
                    "max": 0,
                },
                "bathrooms_half": {
                    "min": 0,
                    "max": 0,
                },
                "distance": 0,
                "min_similarity_score": 0,
                "living_area_sqft": {
                    "min": 0,
                    "max": 0,
                },
                "date": {
                    "min": parse_date("2019-12-27"),
                    "max": parse_date("2019-12-27"),
                },
                "year_built": {
                    "min": 0,
                    "max": 0,
                },
                "statuses": ["active", "removed", "closed"],
            },
            num_comps=0,
        )
        assert_matches_type(RentalCompsResponse, rental_comps, path=["response"])

    @parametrize
    async def test_raw_response_fetch(self, async_client: AsyncMainstay) -> None:
        response = await async_client.data.rental_comps.with_raw_response._fetch(
            addresses=[
                {
                    "street": "14042 Kenyte Row",
                    "city": "San Antonio",
                    "state": "TX",
                    "postal_code": "78253",
                }
            ],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        rental_comps = await response.parse()
        assert_matches_type(RentalCompsResponse, rental_comps, path=["response"])

    @parametrize
    async def test_streaming_response_fetch(self, async_client: AsyncMainstay) -> None:
        async with async_client.data.rental_comps.with_streaming_response._fetch(
            addresses=[
                {
                    "street": "14042 Kenyte Row",
                    "city": "San Antonio",
                    "state": "TX",
                    "postal_code": "78253",
                }
            ],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            rental_comps = await response.parse()
            assert_matches_type(RentalCompsResponse, rental_comps, path=["response"])

        assert cast(Any, response.is_closed) is True
