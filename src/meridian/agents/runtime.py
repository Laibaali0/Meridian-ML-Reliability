"""Read-only-by-default tool executor with schema and budget guards."""
from .audit import AuditTrail
from .budget import Budget
from .contracts import ContractError, validate
from .permissions import PermissionPolicy


class ToolFailure(Exception):
    pass


class Runtime:
    def __init__(self, registry, policy, budget=None):
        self.registry = registry
        self.policy = policy
        self.budget = budget or Budget()
        self.audit = AuditTrail()

    def call(self, name, arguments, units=1):
        if not self.budget.consume(units):
            self.audit.append(name, "blocked", "budget_exceeded")
            raise ToolFailure("budget_exceeded")
        try:
            tool = self.registry.resolve(name)
        except KeyError as exc:
            self.audit.append(name, "blocked", "unregistered")
            raise ToolFailure("unregistered") from exc
        deny = self.policy.check(tool)
        if deny:
            self.audit.append(name, "blocked", deny)
            raise ToolFailure(deny)
        try:
            validate(arguments, tool.required)
        except ContractError as exc:
            self.audit.append(name, "blocked", "invalid_arguments")
            raise ToolFailure("invalid_arguments") from exc
        try:
            value = tool.handler(**arguments)
        except Exception as exc:
            self.audit.append(name, "error", "execution_failure")
            raise ToolFailure("execution_failure") from exc
        self.audit.append(name, "ok")
        return value
