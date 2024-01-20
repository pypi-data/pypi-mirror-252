from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional

from tonita.datatypes.search import SearchRequest

# ******************************** Submit *************************************


@dataclass
class SubmitEvalRequest:
    """Request for a query evaluation.

    Args:
        search_requests (List[SearchRequest]): The search requests whose
            results to evaluate.
        email_addresses (Optional[List[str]]): An optional list of email
            addresses to which notifications should be sent about the status of
            the evaluation.
    """

    search_requests: List[SearchRequest]
    email_addresses: Optional[List[str]] = None

    def __post_init__(self):
        if self.email_addresses is None:
            self.email_addresses = []


@dataclass
class SubmitEvalResponse:
    """Response to a search evaluation submission.

    This dataclass contains the evaluation ID, which can be used to check the
    status of an evaluation and retrieve its results.

    Args:
        eval_id (str): The ID of this evaluation.
    """

    eval_id: str


# ******************************* Retrieve ************************************


class EvalStatus(Enum):
    """The status of an evaluation.

    Args:
        SUBMITTED: The evaluation was successfully submitted.
        IN_PROGRESS: The evaluation is currently being processed.
        COMPLETED: The evaluation has been completed.
        FAILED: The evaluation failed.
        INVALID: The evaluation is invalid (i.e., does not exist).
    """

    SUBMITTED = 1
    IN_PROGRESS = 2
    COMPLETED = 3
    FAILED = 4
    INVALID = 5


@dataclass
class Metrics:
    """Information retrieval metrics for an evaluated query.

    Args:
        precision_at_k (Dict[int, float]): Precision@k, where each key is an
            integer for `k` and each value is the precision value.
    """

    precision_at_k: Dict[int, float]


@dataclass
class ListingResult:
    """Result for a single listing within a query.

    Args:
        listing_id (str): The ID of the listing.
        rank (int): The rank of this listing in the search results given the
            query.
        score (float): The score of this listing in the search results given
            the query.
        rating (int): The evaluation rating of this listing given the query: 1
            if relevant and 0 if irrelevant.
    """

    listing_id: str
    rank: int
    score: float
    rating: int


@dataclass
class QueryResult:
    """The result for a single query.

    Args:
        search_request (SearchRequest): The search request associated with this
            query.
        metrics (Metrics): Evaluation metrics for this query.
        listing_results (List[ListingResult]): The results of the search for
            this particular query. Each element corresponds to a listing
            returned in the search results, and elements are sorted in
            decreasing order of its score.
    """

    search_request: SearchRequest
    metrics: Metrics
    listing_results: List[ListingResult]


@dataclass
class RetrieveEvalResponse:
    """Response for an evaluation retrieval.

    This dataclass will return the status of the evaluation and the evaluation
    results if they are available.

    Args:
        status (EvalStatus): The status of the evaluation.
        query_results (Optional[List[QueryResult]]): The evaluation results;
            one element for each query submitted. This will be ``None`` if the
            status is ``IN_PROGRESS`` or ``FAILED``, and will contain results
            only for a subset of queries submitted if ``NEAR_COMPLETED``.
    """

    status: EvalStatus
    query_results: Optional[List[QueryResult]] = None
