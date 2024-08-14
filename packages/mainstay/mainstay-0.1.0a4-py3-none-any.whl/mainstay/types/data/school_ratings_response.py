# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel

__all__ = ["SchoolRatingsResponse", "Result"]


class Result(BaseModel):
    address_token: str

    token: Optional[str] = None
    """The user-supplied token submitted for the address."""

    avg_ratings: Optional[float] = None
    """
    The average of the given property's schools' (elementary, middle, and high
    school) ratings.
    """

    error_message: Optional[str] = None
    """The error message if the system was unable to process this address."""


class SchoolRatingsResponse(BaseModel):
    results: List[Result]
    """The list of school ratings for each address."""
