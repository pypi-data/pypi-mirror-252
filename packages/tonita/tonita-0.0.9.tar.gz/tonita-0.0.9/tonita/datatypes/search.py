from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class SearchRequest:
    """Contains search request data.

    This dataclass will typically only be used for submitting evaluations and
    feedback.

    Args:
        query (Optional[str]): See `tonita.search` parameter docstrings.
        listing_id (Optional[str]): See `tonita.search` parameter docstrings.
        categories (Optional[List[str]]): See `tonita.search` parameter
            docstrings.
        facet_restrictions (Optional[List[Dict[str, Any]]]):  See
            `tonita.search` parameter docstrings.
    """

    query: Optional[str] = None
    listing_id: Optional[str] = None
    categories: Optional[List[str]] = None
    facet_restrictions: Optional[List[Dict[str, Any]]] = None

    def __post_init__(self):
        error_msg = (
            "The request must contain exactly one of `query` or `listing_id`. "
            f"Got query='{self.query}' and listing_id='{self.listing_id}'."
        )

        both_none = self.query is None and self.listing_id is None
        both_provided = self.query is not None and self.listing_id is not None
        if both_none or both_provided:
            raise ValueError(error_msg)


@dataclass
class Snippet:
    """Explains why a listing was considered relevant to a query.

    Args:
        display_string (str):
            We simply return a single string that describes the basis for why a
            response item was returned. The caller may choose to use this, e.g.
            for displaying as a highlighted snippet under the title of the
            result.
    """

    display_string: str


@dataclass
class SearchResponseItem:
    """A single search result.

    Args:
        listing_id (str): The ID of a listing considered relevant to the query.
        score (float): A higher score denotes a better match to the query.
        categories (List[str]): The set of categories this listing belongs to.
        snippets (List[Snippet]): Explains why this listing was considered a
            relevant match for the query.
    """

    listing_id: str
    score: float
    categories: List[str]
    snippets: List[Snippet]


@dataclass
class SearchResponse:
    """Response to a search request.

    Args:
        items (List[SearchResponseItem]): A list of search results.
        search_response_id (str): An ID for this search response.
    """

    items: List[SearchResponseItem]
    search_response_id: str
