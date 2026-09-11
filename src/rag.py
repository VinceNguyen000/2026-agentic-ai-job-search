"""Local hybrid RAG over personal career evidence and job opportunities.

This module deliberately uses deterministic local hashed embeddings rather than
an external embedding API. BM25 supplies exact-term precision, while the dense
hash vector supplies a lightweight semantic-style similarity signal. Retrieved
career chunks are returned as evidence context for downstream synthesis.
"""

from collections import Counter
from dataclasses import dataclass
import hashlib
import json
import math
from pathlib import Path
import re
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

from src.models import Opportunity, Seeker
from src.retrieval import BM25Retriever
from src.utils import extract_keywords


@dataclass(frozen=True)
class CareerChunk:
    """A self-contained piece of personal career knowledge."""

    chunk_id: str
    category: str
    title: str
    text: str
    metadata: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chunk_id": self.chunk_id,
            "category": self.category,
            "title": self.title,
            "text": self.text,
            "metadata": self.metadata,
        }


@dataclass(frozen=True)
class EvidenceResult:
    """Hybrid retrieval result with sparse, dense, and combined scores."""

    chunk: CareerChunk
    bm25_score: float
    dense_score: float
    hybrid_score: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chunk": self.chunk.to_dict(),
            "bm25_score": round(self.bm25_score, 4),
            "dense_score": round(self.dense_score, 4),
            "hybrid_score": round(self.hybrid_score, 4),
        }


class LocalDenseEncoder:
    """Deterministic hashed dense-vector encoder with no network dependency."""

    def __init__(self, dimensions: int = 256):
        self.dimensions = dimensions

    def encode(self, text: str) -> List[float]:
        vector = [0.0] * self.dimensions
        tokens = extract_keywords(text)
        for token in tokens:
            digest = hashlib.blake2b(token.encode("utf-8"), digest_size=8).digest()
            index = int.from_bytes(digest[:4], "big") % self.dimensions
            sign = 1.0 if digest[4] % 2 else -1.0
            vector[index] += sign
        norm = math.sqrt(sum(value * value for value in vector))
        return [value / norm for value in vector] if norm else vector

    @staticmethod
    def cosine(left: Sequence[float], right: Sequence[float]) -> float:
        return sum(a * b for a, b in zip(left, right))


class PersonalKnowledgeBase:
    """Build a clean career knowledge base from local personal source files."""

    def __init__(self, chunks: Sequence[CareerChunk], encoder: Optional[Any] = None, dimensions: int = 256):
        self.chunks = list(chunks)
        self.encoder = encoder or LocalDenseEncoder(dimensions)
        self.documents = [f"{chunk.title} {chunk.text}" for chunk in self.chunks]
        self.bm25 = self._build_bm25()
        self.vectors = [self.encoder.encode(document) for document in self.documents]

    def _build_bm25(self) -> "ChunkBM25":
        return ChunkBM25(self.documents)

    @classmethod
    def from_directory(cls, directory: str, encoder: Optional[Any] = None) -> "PersonalKnowledgeBase":
        root = Path(directory)
        resume = (root / "resume_parsed.md").read_text(encoding="utf-8")
        projects = (root / "github_projects.md").read_text(encoding="utf-8")
        preferences = json.loads((root / "preferences.json").read_text(encoding="utf-8"))
        chunks = _markdown_chunks(resume, "resume") + _markdown_chunks(projects, "github")
        chunks.append(
            CareerChunk(
                chunk_id="preferences_profile",
                category="preferences",
                title="Career preferences and constraints",
                text=json.dumps(preferences, sort_keys=True),
                metadata={"source": "preferences.json", "hard_constraints": preferences.get("hard_constraints", {})},
            )
        )
        return cls(chunks, encoder=encoder)

    def retrieve(self, query: str, top_k: int = 5, bm25_weight: float = 0.55) -> List[EvidenceResult]:
        """Retrieve evidence using BM25 plus local dense cosine similarity."""
        if not self.chunks:
            return []
        query_vector = self.encoder.encode(query)
        sparse_scores = self.bm25.scores(query)
        max_sparse = max(sparse_scores, default=0.0)
        cosine = getattr(self.encoder, "cosine", LocalDenseEncoder.cosine)
        dense_scores = [max(0.0, cosine(query_vector, vector)) for vector in self.vectors]
        max_dense = max(dense_scores, default=0.0)
        results = []
        for index, chunk in enumerate(self.chunks):
            sparse = sparse_scores[index] / max_sparse if max_sparse else 0.0
            dense = dense_scores[index] / max_dense if max_dense else 0.0
            hybrid = bm25_weight * sparse + (1.0 - bm25_weight) * dense
            results.append(EvidenceResult(chunk, sparse, dense, hybrid))
        results.sort(key=lambda result: result.hybrid_score, reverse=True)
        return results[:top_k]

    def retrieve_for_job(self, seeker: Seeker, opportunity: Opportunity, top_k: int = 5) -> List[EvidenceResult]:
        """Retrieve personal evidence relevant to a specific opportunity."""
        query = " ".join(
            [
                opportunity.title,
                opportunity.description or "",
                " ".join(opportunity.responsibilities),
                " ".join(opportunity.required_skills),
                " ".join(opportunity.preferred_skills),
                " ".join(seeker.career_goals),
            ]
        )
        return self.retrieve(query, top_k=top_k)

    def build_context(self, query: str, top_k: int = 5) -> str:
        """Build citation-like context for an evidence-grounded response."""
        evidence = self.retrieve(query, top_k=top_k)
        return "\n\n".join(
            f"[{item.chunk.chunk_id}] {item.chunk.title}: {item.chunk.text}"
            for item in evidence
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chunk_count": len(self.chunks),
            "embedding_dimensions": self.encoder.dimensions,
            "embedding_type": "external_gemini" if self.encoder.__class__.__name__ == "GeminiEmbeddingEncoder" else "local_hashed_dense_vector",
            "retrieval": "BM25 plus dense cosine hybrid",
            "chunks": [chunk.to_dict() for chunk in self.chunks],
        }


class ChunkBM25:
    """BM25 implementation for personal evidence chunks."""

    def __init__(self, documents: Sequence[str], k1: float = 1.5, b: float = 0.75):
        self.documents = [extract_keywords(document) for document in documents]
        self.k1 = k1
        self.b = b
        self.average_length = sum(map(len, self.documents)) / len(self.documents) if self.documents else 0.0
        self.document_frequency = Counter()
        for document in self.documents:
            self.document_frequency.update(set(document))

    def scores(self, query: str) -> List[float]:
        terms = extract_keywords(query)
        total_documents = len(self.documents)
        scores = []
        for document in self.documents:
            frequencies = Counter(document)
            score = 0.0
            for term in terms:
                frequency = frequencies.get(term, 0)
                document_frequency = self.document_frequency.get(term, 0)
                if not frequency or not document_frequency or not self.average_length:
                    continue
                inverse_frequency = math.log(1 + (total_documents - document_frequency + 0.5) / (document_frequency + 0.5))
                length_norm = 1 - self.b + self.b * len(document) / self.average_length
                score += inverse_frequency * (frequency * (self.k1 + 1)) / (frequency + self.k1 * length_norm)
            scores.append(score)
        return scores


def _markdown_chunks(text: str, source: str) -> List[CareerChunk]:
    """Split Markdown into heading-based, self-contained evidence chunks."""
    sections = re.split(r"\n(?=##?\s+)", text)
    chunks = []
    for index, section in enumerate(sections):
        lines = [line.strip() for line in section.splitlines() if line.strip()]
        if not lines:
            continue
        title = re.sub(r"^#+\s*", "", lines[0]).strip("- ") or f"{source} section {index + 1}"
        body = " ".join(lines[1:]) if len(lines) > 1 else lines[0]
        chunks.append(
            CareerChunk(
                chunk_id=f"{source}_{index + 1:02d}",
                category=source,
                title=title,
                text=body,
                metadata={"source": f"{source}.md", "section_index": index + 1},
            )
        )
    return chunks


def hard_gate_opportunity(seeker: Seeker, opportunity: Opportunity, minimum_salary: Optional[float] = None) -> Tuple[bool, List[str]]:
    """Apply prerequisite checks before soft scoring."""
    reasons = []
    salary_floor = minimum_salary if minimum_salary is not None else seeker.salary_expectation_min
    if salary_floor is not None and opportunity.salary_max is not None and opportunity.salary_max < salary_floor:
        reasons.append("salary maximum is below seeker minimum")
    if seeker.work_mode_preference and opportunity.work_mode not in seeker.work_mode_preference:
        reasons.append("work mode is incompatible")
    if reasons:
        return False, reasons
    return True, []
