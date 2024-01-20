"""Functions for listing-related operations."""

import logging
import os
import pathlib
from typing import Any, Dict, List, Optional, Union

import requests
from rich.progress import track

from tonita.api._helpers import (
    _get_module_var_value,
    _request,
    _resolve_field_value,
)
from tonita.constants import (
    API_KEY_HTTP_HEADER_FIELD_NAME,
    API_KEY_NAME,
    CORPUS_ID_HTTP_HEADER_FIELD_NAME,
    CORPUS_ID_NAME,
    HTTP_METHOD_POST,
    LISTINGS_PATH_ROOT_NAME,
)
from tonita.datatypes.listings import (
    AddListingsResponse,
    AddSingleListingResult,
    DeleteListingsResponse,
    DeleteSingleListingResult,
    GetListingsResponse,
    GetSingleListingResult,
    ListListingsResponse,
    RecoverListingsResponse,
    RecoverSingleListingResult,
    State,
)

# Defaults to "listings" unless set manually by the user in the environment.
LISTINGS_PATH_ROOT = _get_module_var_value(LISTINGS_PATH_ROOT_NAME)


def _add_directory(
    dir_path: str,
    method: str,
    url_path: str,
    headers: Dict[str, Any],
    session: Optional[requests.Session] = None,
) -> Dict[str, Dict[str, Union[bool, str]]]:
    """A helper function that adds listings from a directory.

    Args:
        dir_path (str): Path to the directory containing JSON files.

            Specifically, all files in the directory (and its subdirectories)
            with file extension ".json" will be assumed to be in valid JSON
            format and will be uploaded. Files without the ".json" extension
            will be ignored. If a JSON file could not be sent to the server for
            any reason, a warning will be logged to the console.

    Returns:
        Dict[str, Dict[str, Union[bool, str]]]: A JSON-ified version of the
            `results` field of the `AddListingsReponse` dataclass for all
            listings in the directory that reached the server. (If some JSON
            was unable to reach the server---e.g., because it did not contain a
            valid JSON---then a warning would have been logged to console, and
            its listings will not appear in this returned structure.)
    """

    # If no session was provided, instantiate one to use for all requests in
    # the following loop.
    if session is None:
        session = requests.Session()

    # Loop through files in the directory, sending each to the server.
    results = {}
    for file_path in track(
        pathlib.Path(dir_path).rglob("*.json"),
        description=f"Uploading listings from {dir_path}...",
    ):
        try:
            http_response = _request(
                json_path=file_path,
                method=method,
                url_path=url_path,
                headers=headers,
                session=session,
            )

            # Merge the current accumulated results and new result.
            results = results | http_response["results"]
        except Exception as e:
            logging.warning(
                f"The following error was raised when attempting to upload "
                f"the file at '{file_path}': '{repr(e)}'."
            )
            continue

    return results


def add(
    data: Optional[Dict[str, Any]] = None,
    json_path: Optional[str] = None,
    corpus_id: Optional[str] = None,
    api_key: Optional[str] = None,
    session: Optional[requests.Session] = None,
) -> AddListingsResponse:
    """Add (or overwrite if already exists) data for a batch of listings.

    Args:
        data (Optional[Dict[str, Any]]): A dict containing listings data.
            Exactly one of ``data`` or ``json_path`` should be provided.
        json_path (Optional[str]): This path can either point to a JSON file or
            to a directory containing JSON files.

            Specifically, if this path points to a directory, all files in the
            directory (and its subdirectories) with file extension ".json" will
            be assumed to be in valid JSON format and will be uploaded. Files
            without the ".json" extension will be skipped. If a JSON file could
            not be sent to the server for any reason, a warning will be logged
            to the console.

            A relative path will be resolved to an absolute one.

            Exactly one of ``data`` or ``json_path`` should be provided.
        corpus_id (Optional[str]): The ID of the corpus this listing belongs
            to. If this argument is ``None``, then the value of
            ``tonita.corpus_id`` will be used.
        api_key (Optional[str]): An API key. If this argument is ``None``, then
            the value of ``tonita.api_key`` will be used.
        session (Optional[requests.Session]): A `requests.Session` object to
            use for the request. If the user does not provide a session, a new
            one will be created.

    Returns:
        AddListingsResponse: See docstring for `AddListingsResponse`.

    Raises:
        TonitaBadRequestError: The request is malformed; see error message for
            specifics.
        TonitaInternalServerError: A server-side error occurred.
        TonitaUnauthorizedError: The API key is missing or invalid.
        ValueError:
            * If neither `data` nor `json_path` are provided.
            * If both `data` and `json_path` are provided.
    """

    # Argument values to be used in every request.
    request_method = HTTP_METHOD_POST
    request_url_path = f"{LISTINGS_PATH_ROOT}/add"
    request_headers = {
        CORPUS_ID_HTTP_HEADER_FIELD_NAME: _resolve_field_value(
            name=CORPUS_ID_NAME, value=corpus_id
        ),
        API_KEY_HTTP_HEADER_FIELD_NAME: _resolve_field_value(
            name=API_KEY_NAME, value=api_key
        ),
    }
    request_session = session

    # Check that exactly one of `data` or `json_path` is provided.
    data_and_path_provided = data is not None and json_path is not None
    data_and_path_not_provided = data is None and json_path is None
    if data_and_path_provided or data_and_path_not_provided:
        raise ValueError(
            "Exactly one of `data` or `json_path` should be provided."
        )

    # If an in-memory data structure was provided...
    if data is not None:
        response = _request(
            data=data,
            method=request_method,
            url_path=request_url_path,
            headers=request_headers,
            session=request_session,
        )

        results = response["results"]

    # Otherwise, a path was provided...
    else:
        # Get the absolute path.
        json_path = os.path.abspath(os.path.expanduser(json_path))

        # Check if it exists.
        if not os.path.exists(json_path):
            raise IOError(
                f"The file or directory at '{json_path}' does not exist."
            )

        # If the path is for a file...
        if os.path.isfile(json_path):
            response = _request(
                json_path=json_path,
                method=request_method,
                url_path=request_url_path,
                headers=request_headers,
                session=request_session,
            )

            results = response["results"]
        # Otherwise, if it's a directory...
        else:
            results = _add_directory(
                dir_path=json_path,
                method=request_method,
                url_path=request_url_path,
                headers=request_headers,
                session=request_session,
            )

    # Create method response.
    response = AddListingsResponse(results=results)

    # Cast each item of `response.results` from dict to dataclass.
    for listing_id, listing_result in response.results.items():
        response.results[listing_id] = AddSingleListingResult(**listing_result)

    return response


def list(
    start_listing_id: Optional[str] = None,
    limit: int = 1000,
    corpus_id: Optional[str] = None,
    api_key: Optional[str] = None,
) -> ListListingsResponse:
    """List IDs of all listings in corpus given by ``corpus_id``.

    Args:
        start_listing_id (Optional[str]): If provided, then only listings whose
            IDs appear at or after this listing ID according to lexicographical
            order are returned. If ``None``, then listing IDs are returned
            beginning with the first listing ID according to lexicographical
            order.
        limit (int): If provided, then at most this many listing IDs are
            returned (in lexicographical order). The default returns at most
            1000 listing IDs. To return all listing IDs in the corpus, pass -1.
            If there are more listing IDs to return than a positive ``limit``,
            then the ``next_listing_id`` field in the return object will be
            populated with the next listing ID according to lexicographical
            order. The caller can pass this listing ID as ``start_listing_id``
            in a subsequent call to `list()` to "page" through the remaining
            results. If there are no more listing IDs to return, the
            ``next_listing_id`` field in the response will be ``None``.
        corpus_id (Optional[str]): The ID of the corpus this listing belongs to.
            If this argument is ``None``, then the value of
            ``tonita.corpus_id`` will be used.
        api_key (Optional[str]): An API key. If this argument is ``None``, then
            the value of ``tonita.api_key`` will be used.

    Returns:
        ListListingsResponse: See docstring for `ListListingsResponse`.

    Raises:
        TonitaBadRequestError: The request is malformed; see error message for
            specifics.
        TonitaInternalServerError: A server-side error occurred.
        TonitaUnauthorizedError: The API key is missing or invalid.
    """

    response = _request(
        method=HTTP_METHOD_POST,
        url_path=f"{LISTINGS_PATH_ROOT}/list",
        headers={
            CORPUS_ID_HTTP_HEADER_FIELD_NAME: _resolve_field_value(
                name=CORPUS_ID_NAME, value=corpus_id
            ),
            API_KEY_HTTP_HEADER_FIELD_NAME: _resolve_field_value(
                name=API_KEY_NAME, value=api_key
            ),
        },
        data={"start_listing_id": start_listing_id, "limit": limit},
    )

    response = ListListingsResponse(**response)

    for listing_id, state in response.results.items():
        response.results[listing_id] = State(state)

    return response


def get(
    listing_ids: List[str],
    corpus_id: Optional[str] = None,
    api_key: Optional[str] = None,
) -> GetListingsResponse:
    """Retrieve data for specified listings.

    Args:
        listing_ids (List[str]): The IDs of the listings to retrieve. The
            elements of this list must be distinct (i.e., no duplicates); a
            `TonitaBadRequestError` will be raised otherwise.
        corpus_id (Optional[str]): The ID of the corpus this listing belongs
            to. If this argument is ``None``, then the value of
            ``tonita.corpus_id`` will be used.
        api_key (Optional[str]): An API key. If this argument is ``None``, then
            the value of ``tonita.api_key`` will be used.

    Returns:
        GetListingsResponse: See docstring for `GetListingsResponse`.

    Raises:
        TonitaBadRequestError: The request is malformed; see error message for
            specifics.
        TonitaInternalServerError: A server-side error occurred.
        TonitaUnauthorizedError: The API key is missing or invalid.
    """

    response = _request(
        method=HTTP_METHOD_POST,
        url_path=f"{LISTINGS_PATH_ROOT}/get",
        headers={
            CORPUS_ID_HTTP_HEADER_FIELD_NAME: _resolve_field_value(
                name=CORPUS_ID_NAME, value=corpus_id
            ),
            API_KEY_HTTP_HEADER_FIELD_NAME: _resolve_field_value(
                name=API_KEY_NAME, value=api_key
            ),
        },
        data={"listing_ids": listing_ids},
    )

    response = GetListingsResponse(**response)

    for listing_id, listing_result in response.results.items():
        # Cast each item of `response.results` from dict to dataclass.
        response.results[listing_id] = GetSingleListingResult(**listing_result)

        # Cast state value to `State` enum or `None`.
        state = None
        if response.results[listing_id].state is not None:
            state = State(response.results[listing_id].state)
        response.results[listing_id].state = state

    return response


def delete(
    listing_ids: List[str],
    corpus_id: Optional[str] = None,
    api_key: Optional[str] = None,
) -> DeleteListingsResponse:
    """Delete data for listings.

    Args:
        listing_ids (List[str]): The IDs of the listings to delete. The
            elements of this list must be distinct (i.e., no duplicates); a
            `TonitaBadRequestError` will be raised otherwise.
        corpus_id (Optional[str]): The ID of the corpus this listing belongs
            to. If this argument is ``None``, then the value of
            ``tonita.corpus_id`` will be used.
        api_key (Optional[str]): An API key. If this argument is ``None``, then
            the value of ``tonita.api_key`` will be used.

    Returns:
        DeleteListingsResponse: See docstring for `DeleteListingsResponse`.

    Raises:
        TonitaBadRequestError: The request is malformed; see error message for
            specifics.
        TonitaInternalServerError: A server-side error occurred.
        TonitaUnauthorizedError: The API key is missing or invalid.
    """

    response = _request(
        method=HTTP_METHOD_POST,
        url_path=f"{LISTINGS_PATH_ROOT}/delete",
        headers={
            CORPUS_ID_HTTP_HEADER_FIELD_NAME: _resolve_field_value(
                name=CORPUS_ID_NAME, value=corpus_id
            ),
            API_KEY_HTTP_HEADER_FIELD_NAME: _resolve_field_value(
                name=API_KEY_NAME, value=api_key
            ),
        },
        data={"listing_ids": listing_ids},
    )

    response = DeleteListingsResponse(**response)

    # Cast each item of `response.results` from dict to dataclass.
    for listing_id, listing_result in response.results.items():
        response.results[listing_id] = DeleteSingleListingResult(
            **listing_result
        )

    return response


def recover(
    listing_ids: List[str],
    corpus_id: Optional[str] = None,
    api_key: Optional[str] = None,
) -> RecoverListingsResponse:
    """Recover a batch of listings that were previously marked to be deleted.

    Args:
        listing_ids (List[str]): The IDs of the listings to recover. The
            elements of this list must be distinct (i.e., no duplicates); a
            `TonitaBadRequestError` will be raised otherwise.
        corpus_id (Optional[str]): The ID of the corpus this listing belongs
            to. If this argument is ``None``, then the value of
            ``tonita.corpus_id`` will be used.
        api_key (Optional[str]): An API key. If this argument is ``None``, then
            the value of ``tonita.api_key`` will be used.

    Returns:
        RecoverListingsResponse: See docstring for `RecoverListingsResponse`.

    Raises:
        TonitaBadRequestError: The request is malformed; see error message for
            specifics.
        TonitaInternalServerError: A server-side error occurred.
        TonitaUnauthorizedError: The API key is missing or invalid.
    """

    response = _request(
        method=HTTP_METHOD_POST,
        url_path=f"{LISTINGS_PATH_ROOT}/recover",
        headers={
            CORPUS_ID_HTTP_HEADER_FIELD_NAME: _resolve_field_value(
                name=CORPUS_ID_NAME, value=corpus_id
            ),
            API_KEY_HTTP_HEADER_FIELD_NAME: _resolve_field_value(
                name=API_KEY_NAME, value=api_key
            ),
        },
        data={"listing_ids": listing_ids},
    )

    response = RecoverListingsResponse(**response)

    # Cast each item of `response.results` from dict to dataclass.
    for listing_id, listing_result in response.results.items():
        response.results[listing_id] = RecoverSingleListingResult(
            **listing_result
        )

    return response
