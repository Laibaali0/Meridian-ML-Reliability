"""Classification precision, recall and F1 from explicit predictions."""


def binary_metrics(truth, predictions):
    truth, predictions = list(truth), list(predictions)
    if not truth or len(truth) != len(predictions):
        raise ValueError("Labels and predictions must be aligned and nonempty")
    if not set(truth + predictions).issubset({0, 1}):
        raise ValueError("Binary classification requires 0/1 labels")
    tp = int(sum(t == p == 1 for t, p in zip(truth, predictions)))
    fp = int(sum(t == 0 and p == 1 for t, p in zip(truth, predictions)))
    fn = int(sum(t == 1 and p == 0 for t, p in zip(truth, predictions)))
    tn = len(truth) - tp - fp - fn
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn,
            "precision": precision, "recall": recall,
            "f1": 2 * precision * recall / (precision + recall) if precision + recall else 0.0}
