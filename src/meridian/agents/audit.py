"""Append-only in-memory audit records for safe, testable tool evaluation."""
from dataclasses import dataclass


@dataclass(frozen=True)
class AuditEntry:
    index: int
    tool: str
    status: str
    reason: str = ""


class AuditTrail:
    def __init__(self):
        self.entries = []

    def append(self, tool, status, reason=""):
        self.entries.append(AuditEntry(len(self.entries) + 1, tool, status, reason))

    def counts(self):
        return {status: sum(entry.status == status for entry in self.entries)
                for status in sorted({entry.status for entry in self.entries})}
