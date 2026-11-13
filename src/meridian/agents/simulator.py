"""Safe toy catalog and arithmetic tools; no external network or writes."""
from .registry import Registry, Tool
from .permissions import PermissionPolicy
from .runtime import Runtime


CATALOG = {
    "ITEM-01": {"title": "Canvas Tote", "price_cents": 2200},
    "ITEM-02": {"title": "Running Shoe", "price_cents": 7900},
}


def runtime():
    def lookup(sku):
        if sku not in CATALOG:
            raise LookupError("Unknown SKU")
        return dict(CATALOG[sku])

    tools = Registry([
        Tool("catalog_lookup", {"sku": str}, lookup),
        Tool("add", {"a": int, "b": int}, lambda a, b: a + b),
        Tool("delete_product", {"sku": str}, lambda sku: {"deleted": sku}, writes=True),
    ])
    return Runtime(tools, PermissionPolicy({"catalog_lookup", "add", "delete_product"}, allow_writes=False))
