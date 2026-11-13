"""Sublinear term frequency and smoothed inverse document frequency."""
from collections import Counter
from math import log
import numpy as np

from .tokenize import tokens
from .corpus import check_corpus


class TFIDF:
    def __init__(self, docs):
        self.docs = check_corpus(docs)
        self.vocabulary = sorted({token for doc in self.docs for token in tokens(doc.text)})
        self.term_index = {term: i for i, term in enumerate(self.vocabulary)}
        if not self.vocabulary:
            raise ValueError("Documents have no tokens")
        df = Counter(token for doc in self.docs for token in set(tokens(doc.text)))
        self.idf = np.array([log((len(self.docs) + 1) / (df[token] + 1)) + 1 for token in self.vocabulary])
        self.matrix = np.vstack([self.transform(doc.text) for doc in self.docs])

    def transform(self, text):
        result = np.zeros(len(self.vocabulary))
        for term, count in Counter(tokens(text)).items():
            if term in self.term_index:
                i = self.term_index[term]
                result[i] = (1 + log(count)) * self.idf[i]
        return result

    @staticmethod
    def cosine(matrix, query):
        query_norm = np.linalg.norm(query)
        document_norms = np.linalg.norm(matrix, axis=1)
        return matrix @ query / np.maximum(document_norms * query_norm, 1e-12)
