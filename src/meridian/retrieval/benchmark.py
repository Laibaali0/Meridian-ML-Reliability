"""Reproducible fixture comparisons; not public-benchmark claims."""
from .corpus import Document
from .hybrid import HybridSearch
from .metrics import ndcg, recall_at_k, reciprocal_rank


def benchmark():
    docs = [
        Document("latency", "Quantized transformer inference on GPU memory"),
        Document("catalog", "Product catalog search relevance ranking"),
        Document("recommend", "Contextual bandit product recommendations"),
        Document("mlops", "Model deployment and monitoring pipelines"),
        Document("safety", "AI agent tool safety and evaluation"),
        Document("vector", "Fast vector search index and nearest neighbors"),
    ]
    judgments = {
        "GPU quantization": {"latency": 3, "mlops": 1},
        "product ranking": {"catalog": 3, "recommend": 2},
        "AI tool safety": {"safety": 3},
    }
    engine = HybridSearch(docs)
    results = {}
    for method in ("bm25", "latent", "hybrid"):
        query_metrics = []
        for query, truth in judgments.items():
            ids = engine.search(query, method=method, k=5)
            query_metrics.append((recall_at_k(ids, truth, 5), reciprocal_rank(ids, truth), ndcg(ids, truth, 5)))
        results[method] = dict(zip(("recall", "mrr", "ndcg"),
                                   [sum(row[i] for row in query_metrics)/len(query_metrics) for i in range(3)]))
    return {"toy_queries": len(judgments), "methods": results, "data": "hand-authored fixture"}
