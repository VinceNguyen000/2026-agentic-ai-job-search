"""Optional Gemini embeddings and grounded synthesis adapters."""

import json
import os
from typing import Any, Dict, List, Optional, Sequence
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class GeminiAPIError(RuntimeError):
    """Raised when Gemini returns an unusable response."""


class GeminiClient:
    """Small dependency-free client for Gemini embedding and generation APIs."""

    def __init__(self, api_key: str, embedding_model: str = "text-embedding-004", llm_model: str = "gemini-2.0-flash"):
        self.api_key = api_key
        self.embedding_model = embedding_model
        self.llm_model = llm_model

    @classmethod
    def from_environment(cls) -> Optional["GeminiClient"]:
        if os.getenv("USE_EXTERNAL_AI", "0") != "1":
            return None
        api_key = os.getenv("GEMINI_API_KEY")
        return cls(api_key) if api_key else None

    def _post(self, url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        request = Request(
            f"{url}?key={self.api_key}",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=45) as response:
                return json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError) as exc:
            raise GeminiAPIError(f"Gemini request failed: {exc}") from exc

    def embed(self, texts: Sequence[str]) -> List[List[float]]:
        vectors = []
        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{self.embedding_model}:embedContent"
        for text in texts:
            payload = {"content": {"parts": [{"text": text}]}}
            response = self._post(endpoint, payload)
            values = response.get("embedding", {}).get("values")
            if not values:
                raise GeminiAPIError("Gemini embedding response did not contain values")
            vectors.append(values)
        return vectors

    def generate(self, prompt: str) -> str:
        endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{self.llm_model}:generateContent"
        response = self._post(endpoint, {"contents": [{"parts": [{"text": prompt}]}]})
        try:
            return response["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError, TypeError) as exc:
            raise GeminiAPIError("Gemini generation response did not contain text") from exc


class GeminiEmbeddingEncoder:
    """External 768-dimensional embedding encoder backed by Gemini."""

    def __init__(self, client: GeminiClient):
        self.client = client
        self.dimensions = 768

    def encode(self, text: str) -> List[float]:
        return self.client.embed([text])[0]

    @staticmethod
    def cosine(left: Sequence[float], right: Sequence[float]) -> float:
        return sum(a * b for a, b in zip(left, right))
