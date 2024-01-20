"""Function for search."""

from typing import Any, Dict, List, Optional

import requests

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
    SEARCH_PATH_ROOT_NAME,
)
from tonita.datatypes.search import SearchResponse, SearchResponseItem, Snippet
from tonita.errors import TonitaBadRequestError

# Defaults to "search" unless set manually by the user in the environment.
SEARCH_PATH_ROOT = _get_module_var_value(SEARCH_PATH_ROOT_NAME)
DEFAULT_MAX_RESULTS = 10
MAX_RESULTS_LIMIT = 100


def _validate_search_inputs(
    query: Optional[str] = None,
    listing_id: Optional[str] = None,
    max_results: int = DEFAULT_MAX_RESULTS,
    categories: Optional[List[str]] = None,
    facet_restrictions: Optional[List[Dict[str, Any]]] = None,
    retrieval_only: bool = False,
    corpus_id: Optional[str] = None,
    api_key: Optional[str] = None,
    session: Optional[requests.Session] = None,
):
    """
    Validates all inputs to the `search()` method:
    - Ensures that there are no invalid inputs, sets default values if needed.
    - Ensures all inputs and their contents are of the correct type.
    - Ensures that there are no invalid combinations of inputs.
    If there is any error, returns a TonitaBadRequestError.
    """

    # Set all default values for params which cannot be None.
    if max_results is None:
        max_results = DEFAULT_MAX_RESULTS

    if retrieval_only is None:
        retrieval_only = False

    if query is not None and not isinstance(query, str):
        error_msg = (
            f"Expected attribute 'query' to have type "
            f"'<class 'str'>'. Received the value '{query}' of "
            f"type '{type(query)}'."
        )
        raise TonitaBadRequestError(error_msg)

    if listing_id is not None and not isinstance(listing_id, str):
        error_msg = (
            f"Expected attribute 'listing_id' to have type "
            f"'<class 'str'>'. Received the value '{listing_id}' of "
            f"type '{type(listing_id)}'."
        )
        raise TonitaBadRequestError(error_msg)

    if not isinstance(max_results, int):
        error_msg = (
            f"Expected attribute 'max_results' to have type "
            f"'<class 'int'>'. Received the value '{max_results}' of "
            f"type '{type(max_results)}'."
        )
        raise TonitaBadRequestError(error_msg)

    if categories is not None:
        if not isinstance(categories, list):
            error_msg = (
                f"Expected attribute 'categories' to have type "
                f"'<class 'list'>'. Received the value '{categories}' of "
                f"type '{type(categories)}'."
            )
            raise TonitaBadRequestError(error_msg)

        elif isinstance(categories, list):
            for cat in categories:
                if not isinstance(cat, str):
                    error_msg = (
                        f"Expected attribute 'categories' to have "
                        f"elements of type '<class 'str'>'. Received '{cat}' "
                        f"of type '{type(cat)}'."
                    )
                    raise TonitaBadRequestError(error_msg)

    if facet_restrictions is not None:
        if not isinstance(facet_restrictions, list):
            error_msg = (
                f"Expected attribute 'facet_restrictions' to have type "
                f"'<class 'list'>'. Received the value '{facet_restrictions}' "
                f"of type '{type(facet_restrictions)}'."
            )
            raise TonitaBadRequestError(error_msg)

        elif isinstance(facet_restrictions, list):
            for facet_rest in facet_restrictions:
                if type(facet_rest) is not dict:
                    error_msg = (
                        f"Expected attribute 'facet_restrictions' to "
                        f"have elements of type '<class 'dict'>'. Received "
                        f"'{facet_rest}' of type '{type(facet_rest)}'."
                    )
                    raise TonitaBadRequestError(error_msg)

    if not isinstance(retrieval_only, bool):
        error_msg = (
            f"Expected attribute 'retrieval_only' to have type "
            f"'<class 'bool'>'. Received the value '{retrieval_only}' of "
            f"type '{type(retrieval_only)}'."
        )
        raise TonitaBadRequestError(error_msg)

    if corpus_id is not None and not isinstance(corpus_id, str):
        error_msg = (
            f"Expected attribute 'corpus_id' to have type "
            f"'<class 'str'>'. Received the value '{corpus_id}' of "
            f"type '{type(corpus_id)}'."
        )
        raise TonitaBadRequestError(error_msg)

    if api_key is not None and not isinstance(api_key, str):
        error_msg = (
            f"Expected attribute 'api_key' to have type "
            f"'<class 'str'>'. Received the value '{api_key}' of "
            f"type '{type(api_key)}'."
        )
        raise TonitaBadRequestError(error_msg)

    if session is not None and not isinstance(session, requests.Session):
        error_msg = (
            f"Expected attribute 'session' to have type "
            f"'<class 'requests.Session'>'. Received the value '{session}' of "
            f"type '{type(session)}'."
        )
        raise TonitaBadRequestError(error_msg)

    # Check that exactly one of `query` and `listing_id` is provided.
    error_msg = (
        "The request must contain exactly one of `query` or "
        f"`listing_id`. Got query='{query}' and listing_id='{listing_id}'."
    )

    if query is None and listing_id is None:
        raise TonitaBadRequestError(error_msg)

    elif query is not None and listing_id is not None:
        raise TonitaBadRequestError(error_msg)

    # Check if `max_results` has a valid value.
    if max_results <= 0:
        raise TonitaBadRequestError(
            "The value of 'max_results' must be a positive integer. "
            f"Got {max_results}."
        )

    if max_results > MAX_RESULTS_LIMIT:
        raise TonitaBadRequestError(
            f"The value of 'max_results' can be at most {MAX_RESULTS_LIMIT}. "
            f"Got {max_results}."
        )


def search(
    query: Optional[str] = None,
    listing_id: Optional[str] = None,
    max_results: int = DEFAULT_MAX_RESULTS,
    categories: Optional[List[str]] = None,
    facet_restrictions: Optional[List[Dict[str, Any]]] = None,
    retrieval_only: bool = False,
    corpus_id: Optional[str] = None,
    api_key: Optional[str] = None,
    session: Optional[requests.Session] = None,
) -> SearchResponse:
    """Return search results given a query.

    Args:
        query (Optional[str]): The query for which relevant listings are
            retrieved. This query is a text string that specifies what the user
            is looking for, and is typically a keyword-search query or a
            natural-language query. If ``query`` is provided, ``listing_id``
            must be ``None``.
        listing_id (Optional[str]): If ``listing_id`` is provided, a search
            will return listings that are similar to the given listing. If
            ``listing_id`` is provided, ``query`` must be None.
        max_results (int): The maximum number of results to return.
        categories (Optional[List[str]]): If given, search is restricted to
            listings within these categories.
        facet_restrictions (Optional[List[Dict[str, Any]]]): If facet
            restrictions are provided, listings that satisfy more of the given
            restrictions will generally be ranked higher (and have higher
            scores) than listings that satisfy fewer of them.
            Each restriction is expressed as a dict with the following keys:

            1. "name": Required.
                The name of the facet. For example, "price".

            2. "type": Required.
                The type of the facet across listings that the restriction is
                based on. This will determine how the facet value is handled
                (i.e., what operations are valid for it). For example, each
                listing may have a "price" facet that is numeric, or a "genre"
                facet that is a string.

                Valid values for this field are "STRING", "NUMERIC", and
                "BOOLEAN".
            3. "operation": Required.
                The operation for the restriction. For example, if the value of
                some numeric facet must be greater than or equal to 9, the
                operation would be "GREATER_THAN_EQUAL".

                Valid values are "EQUAL", "LESS_THAN", "LESS_THAN_EQUAL",
                "GREATER_THAN", "GREATER_THAN_EQUAL", and "ONE_OF".

            4. "value": Required.
                The value used for the restriction. Note that this is not
                necessarily the same as the facet value. For example, a
                restriction that movies must be one of three genres would have
                "value" be `["comedy", "drama", "thriller"]`, but the facet
                value for a movie that satisfies the restriction might just be
                "drama". On the other hand, a restriction that the facet for
                "director" be "Jane Doe" would set the "value" field of the
                restriction to "Jane Doe".

            5. "weight": Optional.
                An importance weight for the facet. This weight does not need
                to be normalized across facet restrictions. Weights must be
                provided either for all of the restrictions or for none of
                them. If no weights are provided, equal weights across
                restrictions will be assumed. Facets with zero or negative
                weight will be ignored. Consider the following example set of
                facet restrictions for books:

                .. code-block:: JSON

                    [
                        {
                            "name": "pages",
                            "type": "NUMERIC",
                            "operation": "LESS_THAN_EQUAL",
                            "value": 500,
                            "weight": 3.14159,
                        },
                        {
                            "name": "language",
                            "type": "STRING",
                            "operation": "ONE_OF",
                            "value": ["english", "portuguese", "korean"],
                            "weight": 2.71828,
                        },
                    ]

                Here, we have two restrictions: one that the number of pages of
                the book be less than 500, and one that the language of the
                book must be either English, Portuguese, or Korean. The
                importance weights denote that the restriction on the number of
                pages is slightly more important than the restriction on
                language.
        retrieval_only (bool): Search progresses in two stages:

            1. A retrieval stage, where listings are retrieved along with raw
                scores;

            2. A rescoring stage, where we refine the scores of the listings
                that were retrieved.

            The retrieval stage is very fast, whereas the rescoring stage can
            take more time. Note, however, that the ranking of the listings
            will typically change after scores are refined.
            If this flag is set to ``True``, only the retrieval phase will be
            performed and those results returned. If ``False``, both phases
            will be performed.

            **NOTE:** At this time, the `retrieval_only` flag is applicable
            only for searches with a query, and its default value is `False`.
            For searches where a listing ID is specified, only raw scores will
            ever be returned. Therefore, the ``retrieval_only`` flag does not
            apply; richer rescoring options coming soon.
        corpus_id (Optional[str]): The ID of the corpus to search within. If
            this argument is ``None``, then the value of ``tonita.corpus_id``
            will be used.
        api_key (Optional[str]): An API key. If this argument is `None`, then
            the value of ``tonita.api_key`` will be used.
        session (Optional[requests.Session]): A `requests.Session` object to
            use for the request. If the user does not provide a session, a new
            one will be created.

    Returns:
        SearchResponse: See docstring for `SearchResponse`.

    Raises:
        TonitaBadRequestError: The request is malformed; see error message for
            specifics.
        TonitaInternalServerError: A server-side error occurred.
        TonitaUnauthorizedError: The API key is missing or invalid.
    """

    _validate_search_inputs(
        query=query,
        listing_id=listing_id,
        max_results=max_results,
        categories=categories,
        facet_restrictions=facet_restrictions,
        retrieval_only=retrieval_only,
        corpus_id=corpus_id,
        api_key=api_key,
        session=session,
    )

    response = _request(
        method=HTTP_METHOD_POST,
        url_path=SEARCH_PATH_ROOT,
        headers={
            CORPUS_ID_HTTP_HEADER_FIELD_NAME: _resolve_field_value(
                name=CORPUS_ID_NAME, value=corpus_id
            ),
            API_KEY_HTTP_HEADER_FIELD_NAME: _resolve_field_value(
                name=API_KEY_NAME, value=api_key
            ),
        },
        data=dict(
            query=query,
            listing_id=listing_id,
            max_results=max_results,
            categories=categories,
            facet_restrictions=facet_restrictions,
            retrieval_only=retrieval_only,
        ),
        session=session,
    )

    search_response_items = []
    for item in response["items"]:
        # Pack snippets.
        snippets = []
        for snippet in item["snippets"]:
            snippets.append(Snippet(display_string=snippet["display_string"]))

        search_response_items.append(
            SearchResponseItem(
                listing_id=item["listing_id"],
                score=item["score"],
                categories=item["categories"],
                snippets=snippets,
            )
        )

    return SearchResponse(
        items=search_response_items,
        search_response_id=response["search_response_id"],
    )
