import colander
import pytest
import datetime
from endi.forms.tasks.invoice import (
    get_add_edit_invoice_schema,
    get_add_edit_cancelinvoice_schema,
    get_pdf_export_schema,
    SetProductsSchema,
)


def test_cancelinvoice_invoice_id():
    schema = get_add_edit_cancelinvoice_schema(includes=("invoice_id",))
    schema = schema.bind()

    value = {"invoice_id": 5}
    assert schema.deserialize(value) == value

    value = {}
    with pytest.raises(colander.Invalid):
        schema.deserialize(value)


def test_cancelinvoice(request_with_config, config, cancelinvoice, tva, unity):
    schema = get_add_edit_cancelinvoice_schema()
    request_with_config.context = cancelinvoice
    schema = schema.bind(request=request_with_config)

    value = {
        "name": "Avoir 1",
        "date": datetime.date.today().isoformat(),
        "address": "adress",
        "description": "description",
        "payment_conditions": "Test",
        "invoice_id": 5,
        "financial_year": 2017,
        "line_groups": [
            {
                "task_id": 5,
                "title": "title",
                "description": "description",
                "order": 5,
                "lines": [
                    {
                        "date": colander.null,
                        "cost": 15,
                        "tva": 20,
                        "description": "description",
                        "unity": "h",
                        "quantity": 5,
                        "order": 2,
                    }
                ],
            }
        ],
    }
    expected_value = {
        "name": "Avoir 1",
        "date": datetime.date.today(),
        "address": "adress",
        "description": "description",
        "payment_conditions": "Test",
        "invoice_id": 5,
        "financial_year": 2017,
        "line_groups": [
            {
                "task_id": 5,
                "title": "title",
                "description": "description",
                "order": 5,
                "display_details": True,
                "lines": [
                    {
                        "date": colander.null,
                        "cost": 1500000,
                        "tva": 2000,
                        "description": "description",
                        "mode": "ht",
                        "unity": "h",
                        "quantity": 5.0,
                        "order": 2,
                    }
                ],
            }
        ],
    }
    # Check those values are valid
    result = schema.deserialize(value)
    for key, value in list(expected_value.items()):
        assert result[key] == value


def test_invoice(config, invoice, request_with_config, tva, unity):
    schema = get_add_edit_invoice_schema()
    request_with_config.context = invoice
    config.testing_securitypolicy(userid="test", identity="admin", permissive=True)
    schema = schema.bind(request=request_with_config)

    value = {
        "name": "Facture 1",
        "date": datetime.date.today().isoformat(),
        "address": "adress",
        "description": "description",
        "payment_conditions": "Test",
        "estimation_id": 5,
        "financial_year": 2017,
        "line_groups": [
            {
                "task_id": 5,
                "title": "title",
                "description": "description",
                "order": 5,
                "lines": [
                    {
                        "cost": 15,
                        "tva": 20,
                        "description": "description",
                        "unity": "h",
                        "quantity": 5,
                        "order": 2,
                    }
                ],
            }
        ],
    }
    expected_value = {
        "name": "Facture 1",
        "date": datetime.date.today(),
        "address": "adress",
        "description": "description",
        "payment_conditions": "Test",
        "estimation_id": 5,
        "financial_year": 2017,
        "line_groups": [
            {
                "task_id": 5,
                "title": "title",
                "description": "description",
                "order": 5,
                "display_details": True,
                "lines": [
                    {
                        "cost": 1500000,
                        "date": colander.null,
                        "tva": 2000,
                        "description": "description",
                        "mode": "ht",
                        "unity": "h",
                        "quantity": 5.0,
                        "order": 2,
                    }
                ],
            }
        ],
    }
    # Check those values are valid
    result = schema.deserialize(value)
    for key, value in list(expected_value.items()):
        assert result[key] == value


def test_pdf_export_schema(dbsession, invoice):
    invoice.status = "valid"
    invoice.official_number = "F2021-203"
    invoice.financial_year = 2021
    dbsession.merge(invoice)
    dbsession.flush()
    # assert not raise
    schema = get_pdf_export_schema()
    schema.deserialize(
        {"official_number": {"start": "F2021-203"}, "financial_year": 2021}
    )
    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {"official_number": {"start": "F2021-20454"}, "financial_year": 2021}
        )


def test_set_product_schema(
    dbsession, mk_internalinvoice, get_csrf_request_with_db, invoice
):
    # Assure que le schéma se construit correctement
    # Ref https://framagit.org/endi/endi/-/issues/2664
    schema = SetProductsSchema()
    req = get_csrf_request_with_db()
    req.context = mk_internalinvoice()
    bound_schema = schema.bind(request=req)

    schema = SetProductsSchema()
    req = get_csrf_request_with_db()
    req.context = invoice
    bound_schema = schema.bind(request=req)
