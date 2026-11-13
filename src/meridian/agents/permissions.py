"""Principle-of-least-privilege checks for named tool invocations."""


class PermissionPolicy:
    def __init__(self, allow=None, allow_writes=False):
        self.allow = set(allow or [])
        self.allow_writes = allow_writes

    def check(self, tool):
        if tool.name not in self.allow:
            return "not_allowlisted"
        if tool.writes and not self.allow_writes:
            return "writes_disabled"
        return None
