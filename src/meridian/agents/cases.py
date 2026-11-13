"""Demonstration traces with successful calls and deliberately blocked actions."""
from .trace import load_cases


CASES = load_cases([
    {"name": "read a product", "steps": [
        {"tool": "catalog_lookup", "arguments": {"sku": "ITEM-01"},
         "expected": {"title": "Canvas Tote", "price_cents": 2200}}]},
    {"name": "sum prices", "steps": [
        {"tool": "add", "arguments": {"a": 2200, "b": 7900}, "expected": 10100}]},
    {"name": "deny unauthorized edits", "steps": [
        {"tool": "delete_product", "arguments": {"sku": "ITEM-01"},
         "expected_error": "writes_disabled"}]},
    {"name": "reject invalid input", "steps": [
        {"tool": "add", "arguments": {"a": True, "b": 2},
         "expected_error": "invalid_arguments"}]},
])
