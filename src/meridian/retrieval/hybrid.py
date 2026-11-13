"""One interface for lexical, SVD latent and fused retrieval."""
from .bm25 import BM25
from .latent import LatentIndex
from .fusion import rrf


class HybridSearch:
    def __init__(self, documents, dimensions=8):
        self.bm25 = BM25(documents)
        self.latent = LatentIndex(documents, dimensions=dimensions)

    def search(self, query, method="hybrid", k=5):
        if k <= 0:
            raise ValueError("k must be positive")
        lexical = self.bm25.search(query, k=len(self.bm25.docs))
        semantic = [doc for doc, score in self.latent.search(query, k=len(self.bm25.docs))]
        if method == "bm25":
            ranked = lexical
        elif method == "latent":
            ranked = semantic
        elif method == "hybrid":
            ranked = rrf([lexical, semantic])
        else:
            raise ValueError("Unknown retrieval method")
        return ranked[:k]
