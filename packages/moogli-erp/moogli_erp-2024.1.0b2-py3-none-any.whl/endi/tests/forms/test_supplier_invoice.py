import colander
import pytest


def test_same_percentage_supplier_order_validator(mk_supplier_order, schema_node):
    from endi.forms.supply.supplier_invoice import (
        same_percentage_supplier_order_validator,
    )

    order_0 = mk_supplier_order(cae_percentage=0)
    order_0bis = mk_supplier_order(cae_percentage=0)
    order_100 = mk_supplier_order(cae_percentage=100)

    # assert no exception
    same_percentage_supplier_order_validator(schema_node, [order_0.id, order_0bis.id])

    with pytest.raises(colander.Invalid):
        same_percentage_supplier_order_validator(
            schema_node,
            [order_0.id, order_100.id],
        )


def test_supplier_consistency_validator_schema(
    mk_supplier,
    supplier_invoice,
    supplier,
    supplier_order,
    schema_node,
):
    from endi.forms.supply.supplier_invoice import (
        supplier_consistency_validator,
    )

    # assert no exception
    assert (
        supplier_consistency_validator(
            {
                "supplier_id": supplier_invoice.supplier.id,
                "supplier_orders": [],
            },
            supplier_invoice,
        )
        is True
    )

    # assert no exception
    assert (
        supplier_consistency_validator(
            {
                "supplier_id": None,
                "supplier_orders": [supplier_order.id],
            },
            supplier_invoice,
        )
        is True
    )

    supplier2 = mk_supplier()
    assert (
        supplier_consistency_validator(
            {
                "supplier_id": supplier2.id,
                "supplier_orders": [supplier_order.supplier.id],
            },
            supplier_invoice,
        )
        is not True
    )
