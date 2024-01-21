import colander
import pytest


@pytest.fixture
def supplier_wo_registration(mk_supplier):
    return mk_supplier(registration="")


def test_valid_SupplierInvoiceDispatchSchema(
    date_20190101,
    get_csrf_request_with_db,
    supplier,
    company,
    expense_type,
):
    from endi.forms.supply.supplier_invoice import SupplierInvoiceDispatchSchema

    request = get_csrf_request_with_db()
    schema = SupplierInvoiceDispatchSchema().bind(request=request)
    data = schema.deserialize(
        {
            "date": date_20190101.isoformat(),
            "total_ht": "0",
            "total_tva": "0",
            "lines": [],
            "supplier_id": supplier.id,
            "invoice_file": {"filename": "125_1_test.pdf"},
        }
    )
    assert data == {
        "date": date_20190101,
        "invoice_file": {"filename": "125_1_test.pdf"},
        "lines": [],
        "supplier_id": supplier.id,
        "total_ht": 0,
        "total_tva": 0,
    }

    schema = SupplierInvoiceDispatchSchema().bind(request=request)
    data = schema.deserialize(
        {
            "date": date_20190101.isoformat(),
            "total_ht": "10",
            "total_tva": "2",
            "lines": [
                {
                    "ht": "7.5",
                    "tva": "1.5",
                    "description": "A",
                    "company_id": company.id,
                    "type_id": expense_type.id,
                },
                {
                    "ht": "2.5",
                    "tva": "0.5",
                    "description": "B",
                    "company_id": company.id,
                    "type_id": expense_type.id,
                },
            ],
            "supplier_id": supplier.id,
            "invoice_file": {"filename": "125_1_test.pdf"},
        }
    )
    assert data == {
        "date": date_20190101,
        "invoice_file": {"filename": "125_1_test.pdf"},
        "lines": [
            {
                "company_id": company.id,
                "description": "A",
                "ht": 750,
                "tva": 150,
                "type_id": expense_type.id,
            },
            {
                "company_id": company.id,
                "description": "B",
                "ht": 250,
                "tva": 50,
                "type_id": expense_type.id,
            },
        ],
        "supplier_id": supplier.id,
        "total_ht": 1000,
        "total_tva": 200,
    }


def test_invalid_SupplierInvoiceDispatchSchema(
    date_20190101,
    get_csrf_request_with_db,
    supplier,
    supplier_wo_registration,
    company,
    expense_type,
):
    from endi.forms.supply.supplier_invoice import (
        SupplierInvoiceDispatchSchema,
    )

    pyramid_request = get_csrf_request_with_db()
    schema = SupplierInvoiceDispatchSchema().bind(request=pyramid_request)

    # Wrong sum
    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                "date": date_20190101.isoformat(),
                "total_ht": "0",
                "total_tva": "2",
                "lines": [
                    {
                        "ht": "7.5",
                        "tva": "1.5",
                        "description": "A",
                        "company_id": company.id,
                        "type_id": expense_type.id,
                    },
                    {
                        "ht": "2.5",
                        "tva": "0.5",
                        "description": "B",
                        "company_id": company.id,
                        "type_id": expense_type.id,
                    },
                ],
                "supplier_id": supplier.id,
                "invoice_file": {"filename": "125_1_test.pdf"},
            }
        )

    # Wrong supplier (no Supplier.registration)
    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                "date": date_20190101,
                "total_ht": "0",
                "total_tva": "0",
                "lines": [],
                "supplier_id": supplier_wo_registration.id,
                "invoice_file": {"filename": "125_1_test.pdf"},
            }
        )


def test_get_supplier_invoice_edit_schema():
    from endi.forms.supply.supplier_invoice import (
        get_supplier_invoice_edit_schema,
    )

    schema = get_supplier_invoice_edit_schema()

    for field in (
        "date",
        "supplier_id",
        "cae_percentage",
        "payer_id",
        "supplier_orders",
        "remote_invoice_number",
    ):
        assert field in schema

    schema = get_supplier_invoice_edit_schema(internal=True)

    for field in (
        "date",
        "supplier_id",
        "cae_percentage",
        "payer_id",
        "supplier_orders",
        "remote_invoice_number",
    ):
        assert field not in schema
