"""Evaluate simple comparator-style version requirements."""
import re
from .version import Version


class VersionConstraint:
    def __init__(self, expression):
        conditions = [chunk.strip() for chunk in expression.split(",") if chunk.strip()]
        if not conditions:
            raise ValueError("Provide at least one version constraint")
        self.rules = []
        for condition in conditions:
            match = re.fullmatch(r"(>=|<=|==|!=|>|<)\s*(v?\d+\.\d+(?:\.\d+)?(?:-[a-zA-Z0-9.-]+)?)", condition)
            if not match:
                raise ValueError(f"Unsupported version constraint: {condition}")
            self.rules.append((match[1], Version.parse(match[2])))

    def allows(self, version):
        v = Version.parse(version) if isinstance(version, str) else version
        for op, threshold in self.rules:
            if op == ">=" and v < threshold: return False
            if op == "<=" and threshold < v: return False
            if op == ">" and not threshold < v: return False
            if op == "<" and not v < threshold: return False
            if op == "==" and v != threshold: return False
            if op == "!=" and v == threshold: return False
        return True
