"""Point-in-time-safe feature lookup for a fixed set of user keys."""
from collections import defaultdict
from bisect import bisect_right


def point_in_time_join(events, feature_history):
    """events: (entity, event_time); features: (entity, observed_time, value)."""
    history = defaultdict(list)
    for entity, timestamp, value in feature_history:
        history[entity].append((timestamp, value))
    for values in history.values():
        values.sort(key=lambda row: row[0])
    results = []
    for entity, event_time in events:
        records = history.get(entity, [])
        timestamps = [timestamp for timestamp, _ in records]
        index = bisect_right(timestamps, event_time)-1
        results.append(records[index][1] if index >= 0 else None)
    return results
