"""Typed evidence source with publication metadata and release constraints."""
from dataclasses import dataclass
from datetime import datetime
from .constraints import VersionConstraint
from .intervals import TimeWindow


@dataclass(frozen=True)
class Source:
    source_id: str
    title: str
    published: datetime
    validity: TimeWindow
    version_range: str
    url: str
    reliability: float = 1.0

    def __post_init__(self):
        if not self.source_id or not self.title or not 0 <= self.reliability <= 1:
            raise ValueError("Invalid source ID, title or reliability")
        if self.published.tzinfo is None:
            raise ValueError("Source publication time must be timezone aware")
        VersionConstraint(self.version_range)

    def applicable(self, target_date, target_version):
        return (self.published <= target_date and self.validity.contains(target_date)
                and VersionConstraint(self.version_range).allows(target_version))
