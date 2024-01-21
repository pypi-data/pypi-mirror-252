from endi.forms.supply.supplier_order import get_supplier_order_edit_schema


def test_get_supplier_order_edit_schema():
    schema = get_supplier_order_edit_schema()
    for field in ("supplier_id", "cae_percentage", "name"):
        assert field in schema

    schema = get_supplier_order_edit_schema(internal=True)
    for field in ("supplier_id", "cae_percentage"):
        assert field not in schema
    for field in ("name",):
        assert field in schema
