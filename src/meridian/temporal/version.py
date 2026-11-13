"""Comparable semantic release versions with optional prerelease identifiers."""
from dataclasses import dataclass
import re

_PATTERN = re.compile(r"^v?(\d+)\.(\d+)(?:\.(\d+))?(?:-([0-9A-Za-z.-]+))?(?:\+[0-9A-Za-z.-]+)?$")


@dataclass(frozen=True)
class Version:
    major: int
    minor: int
    patch: int = 0
    prerelease: str = ""

    @classmethod
    def parse(cls, text):
        match = _PATTERN.fullmatch(text.strip())
        if not match:
            raise ValueError(f"Invalid version: {text}")
        return cls(int(match[1]), int(match[2]), int(match[3] or 0), match[4] or "")

    def _parts(self):
        return (self.major, self.minor, self.patch)

    def __lt__(self, other):
        if not isinstance(other, Version):
            return NotImplemented
        if self._parts() != other._parts():
            return self._parts() < other._parts()
        if not self.prerelease:
            return False
        if not other.prerelease:
            return True
        # Simplified prerelease sorting; numeric identifiers are not fully SemVer-compliant.
        return self.prerelease < other.prerelease

    def __str__(self):
        base = f"{self.major}.{self.minor}.{self.patch}"
        return base + (f"-{self.prerelease}" if self.prerelease else "")
