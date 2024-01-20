"""Functions for evaluation-related operations."""
from dataclasses import asdict
from typing import List, Optional

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
    EVAL_PATH_ROOT_NAME,
    HTTP_METHOD_POST,
)
from tonita.datatypes.eval import (
    EvalStatus,
    ListingResult,
    Metrics,
    QueryResult,
    RetrieveEvalResponse,
    SubmitEvalRequest,
    SubmitEvalResponse,
)
from tonita.datatypes.search import SearchRequest

# Defaults to "eval" unless set manually by the user in the environment.
EVAL_PATH_ROOT = _get_module_var_value(EVAL_PATH_ROOT_NAME)


def submit(
    search_requests: List[SearchRequest],
    notification_email_addresses: List[str],
    corpus_id: Optional[str] = None,
    api_key: Optional[str] = None,
) -> SubmitEvalResponse:
    """Submits a request for evaluation of a batch of search requests.

    Args:
        search_requests (List[SearchRequest]): A list of `SearchRequest`s to
            evaluate. See docstring for `SearchRequest`.
        notification_email_addresses (List[str]): A list of email addresses to
            which notifications about the progress of this evaluation should be
            sent.
        corpus_id (Optional[str]): The ID of the corpus to search within for
            this batch of search requests. If this argument is ``None``, then
            the value of ``tonita.corpus_id`` will be used.
        api_key (Optional[str]): An API key. If this argument is ``None``, then
            the value of ``tonita.api_key`` will be used.

    Returns:
        SubmitEvalResponse: See docstring for `SubmitEvalResponse`.

    Raises:
        TonitaBadRequestError: The request is malformed; see error message for
            specifics.
        TonitaInternalServerError: A server-side error occurred.
        TonitaUnauthorizedError: The API key is missing or invalid.
    """

    request = SubmitEvalRequest(
        email_addresses=notification_email_addresses,
        search_requests=search_requests,
    )

    response = _request(
        method=HTTP_METHOD_POST,
        url_path=f"{EVAL_PATH_ROOT}/submit",
        headers={
            CORPUS_ID_HTTP_HEADER_FIELD_NAME: _resolve_field_value(
                name=CORPUS_ID_NAME, value=corpus_id
            ),
            API_KEY_HTTP_HEADER_FIELD_NAME: _resolve_field_value(
                name=API_KEY_NAME, value=api_key
            ),
        },
        data=asdict(request),
    )

    return SubmitEvalResponse(**response)


def retrieve(
    eval_id: str,
    corpus_id: Optional[str] = None,
    api_key: Optional[str] = None,
) -> RetrieveEvalResponse:
    """Retrieves the status of an evaluation, as well as results if available.

    Args:
        eval_id (str): The ID of an evaluation whose status to check or results
            to retrieve.
        corpus_id (Optional[str]): The ID of the corpus that was used when
            submitting the evaluation. If this argument is ``None``, then the
            value of ``tonita.corpus_id`` will be used.
        api_key (Optional[str]): An API key corresponding to the submitted
            evaluation. If this argument is ``None``, then the value of
            ``tonita.api_key`` will be used.

    Returns:
        RetrieveEvalResponse: See docstring for `RetrieveEvalResponse`.

    Raises:
        TonitaBadRequestError: The request is malformed; see error message for
            specifics.
        TonitaInternalServerError: A server-side error occurred.
        TonitaUnauthorizedError: The API key is missing or invalid.
    """

    response = _request(
        method=HTTP_METHOD_POST,
        url_path=f"{EVAL_PATH_ROOT}/retrieve",
        headers={
            CORPUS_ID_HTTP_HEADER_FIELD_NAME: _resolve_field_value(
                name=CORPUS_ID_NAME, value=corpus_id
            ),
            API_KEY_HTTP_HEADER_FIELD_NAME: _resolve_field_value(
                name=API_KEY_NAME, value=api_key
            ),
        },
        data={"evaluation_id": eval_id},
    )

    if response["query_results"] is None:
        return RetrieveEvalResponse(
            status=EvalStatus(response["status"]),
        )

    query_results = []
    for query_result_json in response["query_results"]:
        listing_results = []
        for listing_result_json in query_result_json["listing_results"]:
            listing_results.append(ListingResult(**listing_result_json))

        listing_results = sorted(listing_results, key=lambda x: x.rank)

        search_request = query_result_json["search_request"]
        precision_at_k = query_result_json["metrics"]["precision_at_k"]

        query_results.append(
            QueryResult(
                search_request=SearchRequest(
                    query=search_request["query"],
                    listing_id=search_request["listing_id"],
                    categories=search_request["categories"],
                    facet_restrictions=search_request["facet_restrictions"],
                ),
                metrics=Metrics(precision_at_k=precision_at_k),
                listing_results=listing_results,
            )
        )

    return RetrieveEvalResponse(
        status=EvalStatus(response["status"]),
        query_results=query_results,
    )
