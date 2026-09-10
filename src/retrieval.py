"""Lexical and hybrid retrieval for job opportunities.

The BM25 implementation is intentionally dependency-light so the project can run
locally. It provides a retrieval stage before the explainable weighted matcher.
"""

from collections import Counter
import math
from typing import Dict, Iterable, List, Sequence, Tuple

from src.models import Opportunity, Seeker
from src.utils import extract_keywords


class BM25Retriever:
    """Small in-memory BM25 index for opportunity documents."""

    def __init__(self, opportunities: Sequence[Opportunity], k1: float = 1.5, b: float = 0.75):
        self.opportunities = list(opportunities)
        self.k1 = k1
        self.b = b
        self.documents = [self._document_tokens(opportunity) for opportunity in self.opportunities]
        self.document_lengths = [len(document) for document in self.documents]
        self.average_document_length = sum(self.document_lengths) / len(self.document_lengths) if self.documents else 0.0
        self.document_frequency = Counter()
        for document in self.documents:
            self.document_frequency.update(set(document))

    @staticmethod
    def _document_text(opportunity: Opportunity) -> str:
        return " ".join(
            [
                opportunity.title,
                opportunity.company,
                opportunity.description or "",
                " ".join(opportunity.responsibilities),
                " ".join(opportunity.required_skills),
                " ".join(opportunity.preferred_skills),
            ]
        )

    @classmethod
    def _document_tokens(cls, opportunity: Opportunity) -> List[str]:
        return extract_keywords(cls._document_text(opportunity))

    def score(self, query: str, document_index: int) -> float:
        """Calculate a BM25 score for one indexed document."""
        if not self.documents or self.average_document_length == 0:
            return 0.0
        query_terms = extract_keywords(query)
        document = self.documents[document_index]
        term_counts = Counter(document)
        score = 0.0
        total_documents = len(self.documents)
        for term in query_terms:
            frequency = term_counts.get(term, 0)
            if not frequency:
                continue
            document_frequency = self.document_frequency.get(term, 0)
            inverse_document_frequency = math.log(1 + (total_documents - document_frequency + 0.5) / (document_frequency + 0.5))
            length_norm = 1 - self.b + self.b * len(document) / self.average_document_length
            score += inverse_document_frequency * (frequency * (self.k1 + 1)) / (frequency + self.k1 * length_norm)
        return score

    def retrieve(self, query: str, top_k: int = 10) -> List[Tuple[Opportunity, float]]:
        """Return opportunities ordered by descending BM25 score."""
        scored = [(opportunity, self.score(query, index)) for index, opportunity in enumerate(self.opportunities)]
        scored.sort(key=lambda item: item[1], reverse=True)
        return scored[:top_k]


class HybridRetriever:
    """Combine BM25 retrieval with the explainable weighted matcher."""

    def __init__(self, opportunities: Sequence[Opportunity]):
        self.opportunities = list(opportunities)
        self.bm25 = BM25Retriever(self.opportunities)

    @staticmethod
    def _query_for_seeker(seeker: Seeker) -> str:
        return " ".join(seeker.skills + seeker.career_goals + seeker.industry_interests)

    def retrieve(self, seeker: Seeker, top_k: int = 10) -> List[Dict[str, object]]:
        """Retrieve lexical candidates and expose normalized retrieval scores."""
        results = self.bm25.retrieve(self._query_for_seeker(seeker), top_k=top_k)
        maximum = max((score for _, score in results), default=0.0)
        return [
            {
                "opportunity": opportunity,
                "retrieval_score": round(score / maximum * 100, 2) if maximum else 0.0,
                "bm25_score": round(score, 4),
            }
            for opportunity, score in results
        ]

    def rerank(self, seeker: Seeker, matcher: object, top_k: int = 5) -> List[Dict[str, object]]:
        """Use BM25 for candidate retrieval and the weighted matcher for reranking."""
        candidates = self.retrieve(seeker, top_k=max(top_k, 10))
        reranked = []
        for candidate in candidates:
            opportunity = candidate["opportunity"]
            match = matcher.calculate_match(seeker, opportunity)
            reranked.append({**candidate, "match_result": match})
        reranked.sort(
            key=lambda item: (item["match_result"].overall_match_percentage, item["retrieval_score"]),
            reverse=True,
        )
        return reranked[:top_k]
