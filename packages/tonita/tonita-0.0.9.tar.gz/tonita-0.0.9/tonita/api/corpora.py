"""Functions for corpus-related operations."""

import re
from typing import Optional

from tonita.api._helpers import (
    _get_module_var_value,
    _request,
    _resolve_field_value,
)
from tonita.constants import (
    API_KEY_HTTP_HEADER_FIELD_NAME,
    API_KEY_NAME,
    CORPORA_PATH_ROOT_NAME,
    CORPUS_ID_NAME,
    HTTP_METHOD_POST,
)
from tonita.datatypes.corpora import (
    AddCorpusResponse,
    DeleteCorpusResponse,
    GetCorpusResponse,
    ListCorporaResponse,
    RecoverCorpusResponse,
    State,
)

# Defaults to "corpora" unless set manually by the user in the environment.
CORPORA_PATH_ROOT = _get_module_var_value(CORPORA_PATH_ROOT_NAME)


def add(corpus_id: str, api_key: Optional[str] = None) -> AddCorpusResponse:
    """Add a corpus.

    Args:
        corpus_id (str): The ID of the corpus to add. This ID can only contain
            alphanumeric characters and underscores.
        api_key (Optional[str]): An API key. If this argument is ``None``, then
            the value of ``tonita.api_key`` will be used.

    Returns:
        AddCorpusResponse: See docstring for `AddCorpusResponse`.

    Raises:
        TonitaBadRequestError: The request is malformed; see error message for
            specifics.
        TonitaInternalServerError: A server-side error occurred.
        TonitaUnauthorizedError: The API key is missing or invalid.
        ValueError: If the corpus ID contains characters that are not
            alphanumeric or underscores.
    """

    valid_corpus_id_regex = re.compile("^[a-zA-Z0-9_]+$")
    if not valid_corpus_id_regex.match(corpus_id):
        raise ValueError(
            "Corpus ID can only contain alphanumeric characters and "
            "underscores."
        )

    response = _request(
        method=HTTP_METHOD_POST,
        url_path=f"{CORPORA_PATH_ROOT}/add",
        headers={
            API_KEY_HTTP_HEADER_FIELD_NAME: _resolve_field_value(
                name=API_KEY_NAME, value=api_key
            )
        },
        data={CORPUS_ID_NAME: corpus_id},
    )

    return AddCorpusResponse(**response)


def list(api_key: Optional[str] = None) -> ListCorporaResponse:
    """List all available corpora.

    Args:
        api_key (Optional[str]): An API key. If this argument is ``None``, then
            the value of ``tonita.api_key`` will be used.

    Returns:
        ListCorporaResponse: See docstring for `ListCorporaResponse`.

    Raises:
        TonitaInternalServerError: A server-side error occurred.
        TonitaUnauthorizedError: The API key is missing or invalid.
    """

    response = _request(
        method=HTTP_METHOD_POST,
        url_path=f"{CORPORA_PATH_ROOT}/list",
        headers={
            API_KEY_HTTP_HEADER_FIELD_NAME: _resolve_field_value(
                name=API_KEY_NAME, value=api_key
            )
        },
        data="{}",
    )

    response = ListCorporaResponse(**response)

    for corpus_id, state in response.results.items():
        response.results[corpus_id] = State(state)

    return response


def get(corpus_id: str, api_key: Optional[str] = None) -> GetCorpusResponse:
    """Get information about a corpus.

    Args:
        corpus_id (str): The ID of the corpus to get information for.
        api_key (Optional[str]): An API key. If this argument is ``None``, then
            the value of ``tonita.api_key`` will be used.

    Returns:
        GetCorpusResponse: See docstring for `GetCorpusResponse`.

    Raises:
        TonitaBadRequestError: The request is malformed; see error message for
            specifics.
        TonitaInternalServerError: A server-side error occurred.
        TonitaUnauthorizedError: The API key is missing or invalid.
    """

    response = _request(
        method=HTTP_METHOD_POST,
        url_path=f"{CORPORA_PATH_ROOT}/get",
        headers={
            API_KEY_HTTP_HEADER_FIELD_NAME: _resolve_field_value(
                name=API_KEY_NAME, value=api_key
            )
        },
        data={CORPUS_ID_NAME: corpus_id},
    )

    response = GetCorpusResponse(**response)

    if response.state is not None:
        response.state = State(response.state)

    return response


def delete(
    corpus_id: str, api_key: Optional[str] = None
) -> DeleteCorpusResponse:
    """Delete a corpus.

    Args:
        corpus_id (str): The ID of the corpus to delete.
        api_key (Optional[str]): An API key. If this argument is ``None``, then
            the value of ``tonita.api_key`` will be used.

    Returns:
        DeleteCorpusResponse: See docstring for `DeleteCorpusResponse`.

    Raises:
        TonitaBadRequestError: The request is malformed; see error message for
            specifics.
        TonitaInternalServerError: A server-side error occurred.
        TonitaUnauthorizedError: The API key is missing or invalid.
    """

    response = _request(
        method=HTTP_METHOD_POST,
        url_path=f"{CORPORA_PATH_ROOT}/delete",
        headers={
            API_KEY_HTTP_HEADER_FIELD_NAME: _resolve_field_value(
                name=API_KEY_NAME, value=api_key
            )
        },
        data={CORPUS_ID_NAME: corpus_id},
    )

    return DeleteCorpusResponse(**response)


def recover(
    corpus_id: str, api_key: Optional[str] = None
) -> RecoverCorpusResponse:
    """Recover a corpus that was previously marked to be deleted.

    Args:
        corpus_id (str): The ID of the corpus to recover.
        api_key (Optional[str]): An API key. If this argument is ``None``, then
            the value of ``tonita.api_key`` will be used.

    Returns:
        RecoverCorpusResponse: See docstring for `RecoverCorpusResponse`.

    Raises:
        TonitaBadRequestError: The request is malformed; see error message for
            specifics.
        TonitaInternalServerError: A server-side error occurred.
        TonitaUnauthorizedError: The API key is missing or invalid.
    """

    response = _request(
        method=HTTP_METHOD_POST,
        url_path=f"{CORPORA_PATH_ROOT}/recover",
        headers={
            API_KEY_HTTP_HEADER_FIELD_NAME: _resolve_field_value(
                name=API_KEY_NAME, value=api_key
            )
        },
        data={CORPUS_ID_NAME: corpus_id},
    )

    return RecoverCorpusResponse(**response)
