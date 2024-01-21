from endi.models.supply import (
    SupplierInvoiceLine,
    SupplierOrderLine,
)
from endi.forms.supply import get_add_edit_line_schema


def test_get_add_edit_line_schema():

    schema = get_add_edit_line_schema(SupplierInvoiceLine)
    for field in (
        "ht",
        "tva",
        "type_id",
        "description",
        "customer_id",
        "business_id",
        "project_id",
    ):
        assert field in schema

    schema = get_add_edit_line_schema(SupplierInvoiceLine, internal=True)
    for field in ("type_id", "description", "customer_id", "business_id", "project_id"):
        assert field in schema
    for field in ("tva", "ht"):
        assert field not in schema

    schema = get_add_edit_line_schema(SupplierOrderLine)
    for field in ("ht", "tva", "type_id", "description"):
        assert field in schema

    schema = get_add_edit_line_schema(SupplierOrderLine, internal=True)
    for field in ("type_id", "description"):
        assert field in schema

    for field in ("tva", "ht"):
        assert field not in schema
