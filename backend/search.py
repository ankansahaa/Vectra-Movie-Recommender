import json
import pickle

import numpy as np
from sentence_transformers import SentenceTransformer

from backend.config import EMBEDDING_MODEL, SEARCH_INDEX_JSON, VECTORS_PATH


class VectraIndex:
    """In-memory semantic search index over the enriched movie catalogue."""

    def __init__(self) -> None:
        self.records: list[dict] = json.loads(SEARCH_INDEX_JSON.read_text(encoding="utf-8"))
        with open(VECTORS_PATH, "rb") as f:
            self.vectors: np.ndarray = pickle.load(f)
        self.model = SentenceTransformer(EMBEDDING_MODEL)
        self.id_to_index = {record["id"]: i for i, record in enumerate(self.records)}
        print(f"Vectra index ready — {len(self.records)} movies loaded.")

    def search(self, query: str, top_k: int = 24) -> list[tuple[dict, float]]:
        query_vector = self.model.encode([query], normalize_embeddings=True)
        similarities = (self.vectors @ query_vector[0]).flatten()
        top_indices = np.argsort(similarities)[::-1][:top_k]
        return [(self.records[i], float(similarities[i])) for i in top_indices]

    def get(self, movie_id: int) -> dict | None:
        idx = self.id_to_index.get(movie_id)
        return self.records[idx] if idx is not None else None

    def similar(self, movie_id: int, top_k: int = 12) -> list[tuple[dict, float]]:
        idx = self.id_to_index.get(movie_id)
        if idx is None:
            return []
        target_vector = self.vectors[idx]
        similarities = (self.vectors @ target_vector).flatten()
        top_indices = np.argsort(similarities)[::-1]
        results = []
        for i in top_indices:
            if i == idx:
                continue
            results.append((self.records[i], float(similarities[i])))
            if len(results) >= top_k:
                break
        return results

    def trending(self, top_k: int = 24) -> list[dict]:
        return sorted(self.records, key=lambda r: r.get("popularity") or 0, reverse=True)[:top_k]
