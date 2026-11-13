"""Time-bound validity windows with explicit UTC-aware timestamps."""
from dataclasses import dataclass
from datetime import datetime, timezone


def parse_time(text):
    timestamp = datetime.fromisoformat(text.replace("Z", "+00:00"))
    if timestamp.tzinfo is None:
        raise ValueError("Timestamps must include a timezone")
    return timestamp.astimezone(timezone.utc)


@dataclass(frozen=True)
class TimeWindow:
    start: datetime
    end: datetime | None = None

    def __post_init__(self):
        if self.start.tzinfo is None or (self.end is not None and self.end.tzinfo is None):
            raise ValueError("Time windows need aware timestamps")
        if self.end is not None and self.end < self.start:
            raise ValueError("Validity window ends before it begins")

    def contains(self, when):
        if when.tzinfo is None:
            raise ValueError("Target date must be timezone aware")
        return when >= self.start and (self.end is None or when < self.end)
