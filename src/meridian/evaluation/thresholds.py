"""Declarative acceptance criteria with explicit comparison operators."""


def check(metrics, requirements):
    failures = {}
    for name, rule in requirements.items():
        if name not in metrics:
            failures[name] = "missing"
            continue
        operator, boundary = rule
        value = metrics[name]
        valid = {
            ">=": lambda: value >= boundary,
            "<=": lambda: value <= boundary,
            ">": lambda: value > boundary,
            "<": lambda: value < boundary,
        }
        if operator not in valid:
            raise ValueError(f"Unsupported operator: {operator}")
        if not valid[operator]():
            failures[name] = f"{value} does not satisfy {operator} {boundary}"
    return {"passed": not failures, "failures": failures}
