"""Truncated SVD latent retrieval over a TF-IDF matrix, not pretrained embeddings."""
import numpy as np
from .tfidf import TFIDF


class LatentIndex:
    def __init__(self, docs, dimensions=12):
        if dimensions < 1:
            raise ValueError("dimensions must be positive")
        self.tfidf = TFIDF(docs)
        u, singular, vt = np.linalg.svd(self.tfidf.matrix, full_matrices=False)
        rank = min(dimensions, len(singular))
        self.components = vt[:rank]
        self.documents = u[:, :rank] * singular[:rank]

    def search(self, query, k=5):
        if k < 1:
            raise ValueError("k must be positive")
        projected_query = self.tfidf.transform(query) @ self.components.T
        scores = TFIDF.cosine(self.documents, projected_query)
        pairs = [(self.tfidf.docs[i].doc_id, float(score)) for i, score in enumerate(scores)]
        pairs.sort(key=lambda row: (-row[1], row[0]))
        return pairs[:k]
