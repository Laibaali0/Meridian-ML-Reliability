"""Okapi BM25 with length normalization and deterministic ID ordering."""
from collections import Counter
from math import log

from .corpus import check_corpus
from .tokenize import tokens


class BM25:
    def __init__(self, docs, k1=1.2, b=0.75):
        self.docs = check_corpus(docs)
        if k1 <= 0 or not 0 <= b <= 1:
            raise ValueError("k1 must be positive and b within [0,1]")
        self.k1, self.b = k1, b
        self.counts = [Counter(tokens(doc.text)) for doc in self.docs]
        self.lengths = [sum(row.values()) for row in self.counts]
        self.mean_length = sum(self.lengths) / len(self.docs) or 1
        document_frequency = Counter(term for row in self.counts for term in row)
        n = len(self.docs)
        self.idf = {term: log(1 + (n - freq + .5) / (freq + .5)) for term, freq in document_frequency.items()}

    def score(self, query):
        scores = {}
        for index, doc in enumerate(self.docs):
            total = 0.0
            for term in set(tokens(query)):
                frequency = self.counts[index].get(term, 0)
                if frequency:
                    denom = frequency + self.k1 * (1 - self.b + self.b * self.lengths[index] / self.mean_length)
                    total += self.idf[term] * frequency * (self.k1 + 1) / denom
            scores[doc.doc_id] = total
        return scores

    def search(self, query, k=5):
        if k < 1:
            raise ValueError("k must be positive")
        scores = self.score(query)
        return sorted(scores, key=lambda key: (-scores[key], key))[:k]
