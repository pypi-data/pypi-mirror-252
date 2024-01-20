from dataclasses import dataclass

from tonita.datatypes.search import SearchRequest


@dataclass
class FeedbackItem:
    """Contains feedback data for a single search request-listing pair.

    Args:
        search_request (SearchRequest): Contains information about the search
            request to provide feedback on.
        corpus_id (str): The corpus ID for the search.
        listing_id (str): The ID of a listing from the search results produced
            by the search request.
        relevance (float): A value representing the ground-truth relevance
            of the listing for the search request. Must be between 0 and 1,
            inclusive.
    """

    search_request: SearchRequest
    corpus_id: str
    listing_id: str
    relevance: float

    def __post_init__(self):
        if self.relevance < 0 or self.relevance > 1:
            raise ValueError(
                "The value of `relevance` must be between 0 and 1, inclusive. "
                f"Received {self.relevance} instead."
            )


@dataclass
class SubmitFeedbackResponse:
    """Response to a feedback submission.

    Args:
        feedback_submission_id (str): An ID of the feedback submission.
    """

    feedback_submission_id: str
