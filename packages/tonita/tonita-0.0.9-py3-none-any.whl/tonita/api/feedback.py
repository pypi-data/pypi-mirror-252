"""Functions for evaluation-related operations."""
import os
from dataclasses import asdict
from typing import List, Optional

import jsonlines

from tonita.api._helpers import (
    _get_module_var_value,
    _request,
    _resolve_field_value,
)
from tonita.constants import (
    API_KEY_HTTP_HEADER_FIELD_NAME,
    API_KEY_NAME,
    FEEDBACK_PATH_ROOT_NAME,
    HTTP_METHOD_POST,
)
from tonita.datatypes.feedback import FeedbackItem, SubmitFeedbackResponse

# Defaults to "feedback" unless set manually by the user in the environment.
FEEDBACK_PATH_ROOT = _get_module_var_value(FEEDBACK_PATH_ROOT_NAME)


def submit(
    feedback_items: Optional[List[FeedbackItem]] = None,
    jsonl_path: Optional[str] = None,
    api_key: Optional[str] = None,
) -> SubmitFeedbackResponse:
    """Submits a batch of feedback items.

    Args:
        feedback_items (Optional[List[FeedbackItem]]): The items containing the
            data to submit.

            Exactly one of ``feedback_items`` or ``jsonl_path`` must be
            provided.
        jsonl_path (Optional[str]): A path to a JSONL file where each line is
            a ``FeedbackItem`` in JSON format, where each field and value of
            the dataclass has a corresponding key and value in the JSON. For
            example, consider the following dataclass:

            .. code-block:: python

                FeedbackItem(
                    search_request=SearchRequest(
                        query="famous 90s romcom"
                    ),
                    corpus_id="movies",
                    listing_id="sa395823fn",
                    relevance=0.98
                )

            As a JSON, this becomes:

            .. code-block:: JSON

                {
                    "search_request": {
                        "query": "famous 90s romcom"
                    },
                    "corpus_id": "movies",
                    "listing_id": "sa395823fn",
                    "relevance": 0.98
                }

            Exactly one of ``feedback_items`` or ``jsonl_path`` must be
            provided.
        api_key (Optional[str]): An API key. If this argument is ``None``, then
            the value of ``tonita.api_key`` will be used.

    Returns:
        SubmitFeedbackResponse: See docstring for ``SubmitFeedbackResponse``.

    Raises:
        TonitaBadRequestError: The request is malformed; see error message for
            specifics.
        TonitaInternalServerError: A server-side error occurred.
        TonitaUnauthorizedError: The API key is missing or invalid.
    """

    # Check that exactly one of `feedback_items` and `jsonl_path` is provided.
    both_none = feedback_items is None and jsonl_path is None
    both_provided = feedback_items is not None and jsonl_path is not None
    if both_provided or both_none:
        raise ValueError(
            "Exactly one of `feedback_items` and `jsonl_path` must be "
            "provided."
        )

    # If a path to a JSONL file is provided, coerce to list of `FeedbackItem`s.
    if jsonl_path is not None:
        jsonl_path = os.path.abspath(os.path.expanduser(jsonl_path))

        feedback_items = []
        with jsonlines.open(jsonl_path) as reader:
            for line in reader:
                feedback_items.append(FeedbackItem(**line))

    # Cast `FeedbackItem`s to dictionaries to send via POST.
    feedback_item_jsons = []
    for feedback_item in feedback_items:
        feedback_item_jsons.append(asdict(feedback_item))

    response = _request(
        method=HTTP_METHOD_POST,
        url_path=f"{FEEDBACK_PATH_ROOT}/submit",
        headers={
            API_KEY_HTTP_HEADER_FIELD_NAME: _resolve_field_value(
                name=API_KEY_NAME, value=api_key
            )
        },
        data=feedback_item_jsons,
    )

    return SubmitFeedbackResponse(**response)
