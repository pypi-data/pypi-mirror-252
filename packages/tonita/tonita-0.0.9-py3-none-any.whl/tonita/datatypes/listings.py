from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Optional

# ****************************** AddListings **********************************


@dataclass
class AddSingleListingResult:
    """The outcome of adding/updating a single listing in a corpus.

    Args:
        success (bool): ``True`` if the operation succeeded.
        error_message (str): An error message if ``success`` is ``False``.
            Empty if ``success`` is ``True``.
    """

    success: bool
    error_message: str = ""


@dataclass
class AddListingsResponse:
    """Response to a request to add/update a batch of listings in a corpus.

    Args:
        results (Dict[str, AddSingleListingResult]): Each key is a listing ID.
            The value denotes the outcome of attempting to add/update that
            listing.
    """

    results: Dict[str, AddSingleListingResult]


# ******************************* ListingState ********************************


class State(str, Enum):
    """Gives the possible states of a listing.

    Args:
        INACTIVE: The listing is inactive.
        ACTIVE: The listing is active.
    """

    INACTIVE = "INACTIVE"
    ACTIVE = "ACTIVE"


# ******************************* ListListings ********************************


@dataclass
class ListListingsResponse:
    """Response to a request to enumerate all listing IDs in a corpus.

    Args:
        results (Dict[str, State]): A dict mapping all listing ID's for a
            particular corpus to their state, which will be one of the values
            given by the enum `ListingState`. Note that if the caller provides
            the ``start_listing_id`` or ``limit`` parameters in the request,
            then this dict will only contain a subset of all the listing IDs in
            the corpus. Specifically, it will only contain listing IDs that
            appear after (and including) ``start_listing_id`` in
            lexicographical order. If the ``limit`` parameter is provided, the
            length of this dict is at most ``limit``.
        next_listing_id (Optional[str]): If the ``limit`` parameter is provided
            in the request and the number of listing IDs to return is greater
            than ``limit``, then this field will be set to the listing ID that
            comes immediately after the last element of ``results``, according
            to lexicographical order. This allows the caller to implement
            "pagination".

            For example, the caller might pass ``limit=1000`` and
            ``start_listing_id=None`` in the first call. This will return in
            ``results`` the first 1000 listing IDs and store the 1001-st
            listing ID to return (suppose it's "ajsdfl923") in this
            ``next_listing_id`` field. To page, the caller would then pass in a
            second call ``limit=1000`` and ``start_listing_id="ajsdfl923"``.
            This would return the next 1000 listings, starting with
            "ajsdfl923", and the ID of the 2001-st listing will be stored in
            this ``next_listing_id`` field. If there are no more listings to
            "page" through after the current ``results``, this field will be
            ``None``.
    """

    results: Dict[str, State]
    next_listing_id: Optional[str] = None


# ******************************* GetListings *********************************


@dataclass
class GetSingleListingResult:
    """The outcome of retrieving a single listing for a corpus.

    Args:
        success (bool): ``True`` if this listing was successfully retrieved.
            This is ``False`` if the listing does not exist for this corpus, or
            if there was an error in retrieving it.
        data (Optional[Dict[str, Any]]): The raw data associated with this
            listing. This is the dict that was uploaded via ``add()``. This is
            ``None`` if ``success`` is ``False``.
        state (Optional[State]): The state of this listing. The value must be
            one of the string values given by the enum `ListingState`. This is
            ``None`` if ``success`` is ``False``.
        seconds_to_expiration (Optional[float]): If inactive, the amount of
            time (in seconds) the corpus has left until it can no longer be
            recovered. This is `None` if `success` is ``False`` or if ``state``
            is not "INACTIVE".
        error_message (str): An error message if ``success`` is ``False``.
            Empty if ``success`` is ``True``.
    """

    success: bool
    data: Optional[Dict[str, Any]]
    state: Optional[State]
    seconds_to_expiration: Optional[float]
    error_message: str


@dataclass
class GetListingsResponse:
    """Response to a request to retrieve a batch of listings for a corpus.

    Args:
        results (Dict[str, GetSingleListingResult]): Each key is a listing ID.
            The value contains the data associated with this listing, or error
            information about why it couldn't be retrieved.
    """

    results: Dict[str, GetSingleListingResult]


# ****************************** DeleteListings *******************************


@dataclass
class DeleteSingleListingResult:
    """The outcome of deleting a single listing from a corpus.

    Args:
        success (bool): ``True`` if this listing was successfully deleted. This
            is ``False`` if the listing does not already exist for this corpus,
            or if there was an error in deleting it.
        error_message (str): An error message if ``success`` is ``False``.
            Empty if ``success`` is ``True``.
    """

    success: bool
    error_message: str


@dataclass
class DeleteListingsResponse:
    """Response to a request to delete a batch of listings from a corpus.

    Args:
        results (Dict[str, DeleteSingleListingResult]): Each key is a listing
            ID. The value denotes the outcome of deleting this listing.

    """

    results: Dict[str, DeleteSingleListingResult]


# ****************************** RecoverListings ******************************


@dataclass
class RecoverSingleListingResult:
    """The outcome of recovering a single listing for a corpus.

    Args:
        success (bool): Whether this listing was successfully recovered. This
            is ``False`` if no such listing in the corpus is available to be
            recovered, if it's active, or if there was an error in recovering
            it.
        error_message (str):
            An error message if ``success`` is ``False``. Empty if ``success``
            is ``True``.
    """

    success: bool
    error_message: str


@dataclass
class RecoverListingsResponse:
    """Response to a request to recover a batch of listings for a corpus.

    Args:
        results (Dict[str, RecoverSingleListingResult]): Each key is a listing
            ID. The value denotes the outcome of recovering the corresponding
            listing.
    """

    results: Dict[str, RecoverSingleListingResult]
