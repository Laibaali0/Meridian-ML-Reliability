"""Simple approximate inverted-file (IVF) index with K-means coarse centroids."""
import numpy as np


class IVFIndex:
    def __init__(self, vectors, ids, lists=4, seed=42, iterations=10):
        self.vectors = np.asarray(vectors, dtype=float)
        self.ids = list(ids)
        if self.vectors.ndim != 2 or len(self.ids) != len(self.vectors) or len(self.ids) == 0:
            raise ValueError("Expected aligned dense vectors and IDs")
        if len(set(self.ids)) != len(self.ids) or not 1 <= lists <= len(self.ids):
            raise ValueError("Invalid IDs or centroid count")
        if not np.isfinite(self.vectors).all():
            raise ValueError("All vectors must be finite")
        rng = np.random.default_rng(seed)
        centroids = self.vectors[rng.choice(len(self.vectors), size=lists, replace=False)].copy()
        for _ in range(iterations):
            assignment = np.argmin(np.square(self.vectors[:, None, :] - centroids[None, :, :]).sum(axis=2), axis=1)
            for cluster in range(lists):
                members = self.vectors[assignment == cluster]
                if len(members):
                    centroids[cluster] = members.mean(axis=0)
        self.centroids = centroids
        self.assignment = np.argmin(np.square(self.vectors[:, None, :] - centroids[None, :, :]).sum(axis=2), axis=1)

    def search(self, vector, k=5, probes=1):
        query = np.asarray(vector, dtype=float)
        if query.shape != (self.vectors.shape[1],) or k < 1 or probes < 1:
            raise ValueError("Invalid query, k, or probes")
        closest = np.argsort(np.square(self.centroids - query).sum(axis=1))[:probes]
        subset = np.flatnonzero(np.isin(self.assignment, closest))
        distances = np.square(self.vectors[subset] - query).sum(axis=1)
        ranking = sorted(zip(subset, distances), key=lambda row: (row[1], self.ids[row[0]]))
        return [(self.ids[i], float(distance)) for i, distance in ranking[:k]]
