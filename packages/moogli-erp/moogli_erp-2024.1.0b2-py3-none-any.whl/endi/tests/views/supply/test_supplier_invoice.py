import pytest
import io

from endi.models.supply import SupplierInvoice


@pytest.fixture
def file_payload():
    return {
        "fp": io.BytesIO(),
        "filename": "truc.pdf",
        "size": 0,
        "mimetype": "application/octet-stream",
    }


@pytest.fixture
def routes(mk_config, config):
    routes = [
        "/companies/{id}/supplier_invoices",
        "/supplier_invoices/{id}",
    ]
    for route in routes:
        config.add_route(route, route)


def test_supplier_invoice_add_view_wo_order(
    csrf_request_with_db_and_user,
    company,
    routes,
):
    from endi.views.supply.invoices.views import SupplierInvoiceAddView

    csrf_request_with_db_and_user.context = company
    view = SupplierInvoiceAddView(csrf_request_with_db_and_user)
    result = view.submit_success({"supplier_orders_ids": []})
    assert result.code == 302
    assert SupplierInvoice.query().count() == 0  # goes to step 2


def test_supplier_invoice_add_step2_view_order(
    csrf_request_with_db_and_user,
    supplier,
    routes,
):
    csrf_request_with_db_and_user.context = supplier.company
    from endi.views.supply.invoices.views import SupplierInvoiceAddStep2View

    view = SupplierInvoiceAddStep2View(csrf_request_with_db_and_user)
    result = view.submit_success({"supplier_id": supplier.id})
    assert result.code == 302
    assert SupplierInvoice.query().count() == 1
    assert SupplierInvoice.query().first().supplier == supplier


def test_supplier_invoice_add_view_w_order(
    csrf_request_with_db_and_user,
    supplier_order,
    routes,
):
    from endi.views.supply.invoices.views import SupplierInvoiceAddView

    csrf_request_with_db_and_user.context = supplier_order.company
    view = SupplierInvoiceAddView(csrf_request_with_db_and_user)
    result = view.submit_success({"supplier_orders_ids": [supplier_order.id]})
    assert result.code == 302
    assert SupplierInvoice.query().count() == 1
    invoice = SupplierInvoice.query().first()

    assert invoice.supplier == supplier_order.supplier
    assert supplier_order.supplier_invoice == invoice


def test_supplier_invoice_dispatch_view_display_form(
    csrf_request_with_db_and_user,
):
    from endi.views.supply.invoices.views import SupplierInvoiceDispatchView

    view = SupplierInvoiceDispatchView(csrf_request_with_db_and_user)
    # Just check form display does not crash
    result = view.__call__()
    assert isinstance(result, dict)


def test_supplier_invoice_dispatch_submit_success_wo_lines(
    csrf_request_with_db_and_user,
    supplier,
    today,
    file_payload,
):
    from endi.views.supply.invoices.views import SupplierInvoiceDispatchView

    empty_appstruct = {
        "date": today,
        "invoice_file": file_payload,
        "lines": [],
        "supplier_id": supplier.id,
        "total_ht": 0,
        "total_tva": 0,
    }

    view = SupplierInvoiceDispatchView(csrf_request_with_db_and_user)
    result = view.submit_success(empty_appstruct)
    assert result.code == 302


def test_supplier_invoice_dispatch_submit_success_w_lines(
    csrf_request_with_db_and_user,
    supplier,
    expense_type,
    company1,
    company2,
    company3,
    mk_supplier,
    date_20190101,
    file_payload,
):
    from endi.models.third_party.supplier import Supplier
    from endi.models.supply import SupplierInvoice
    from endi.views.supply.invoices.views import SupplierInvoiceDispatchView

    Supplier.query().delete()
    # Company 1 holds the supplier which will be selected for dispatch
    company1_supplier = mk_supplier(
        company=company1,
        registration="1234",
        company_name="sup",
    )
    # Company 2 has a matching (by registration) supplier
    mk_supplier(company=company2, registration="1234", company_name="bloup")
    # Company 3 has no matching (by registration) supplier
    mk_supplier(company=company2, registration="abcd")

    assert Supplier.query().count() == 3
    assert SupplierInvoice.query().count() == 0

    filled_appstruct = {
        "date": date_20190101,
        "invoice_file": file_payload,
        "remote_invoice_number": "",
        "lines": [
            {
                "company_id": company2.id,
                "description": "ia",
                "ht": 100,
                "tva": 99,
                "type_id": expense_type.id,
            },
            {
                "company_id": company3.id,
                "description": "ia",
                "ht": 50,
                "tva": 40,
                "type_id": expense_type.id,
            },
            {
                "company_id": company3.id,
                "description": "o",
                "ht": 5,
                "tva": 2,
                "type_id": expense_type.id,
            },
        ],
        "supplier_id": company1_supplier.id,
        "total_ht": 0,
        "total_tva": 0,
        "remote_invoice_number": "abcd",
    }

    view = SupplierInvoiceDispatchView(csrf_request_with_db_and_user)
    result = view.submit_success(filled_appstruct)

    assert result.code == 302

    # Check Suppliers creation
    assert Supplier.query().count() == 4
    same_suppliers_companies = Supplier.query("company_id").filter_by(
        registration="1234",
    )
    new_company3_supplier = (
        Supplier.query().filter_by(company_id=company3.id, registration="1234").first()
    )

    assert new_company3_supplier.company_name == "sup"

    assert set(same_suppliers_companies) == set(
        [
            (company1.id,),
            (company2.id,),
            (company3.id,),
        ]
    )

    # Check SupplierInvoices creation
    assert SupplierInvoice.query().count() == 2

    inv1, inv2 = SupplierInvoice.query().order_by(
        SupplierInvoice.company_id,
        SupplierInvoice.id,
    )

    assert inv1.company_id == company2.id
    assert inv2.company_id == company3.id

    assert inv1.total_ht == 100
    assert inv1.total_tva == 99
    assert inv1.name == None
    assert inv1.remote_invoice_number == "abcd"

    assert inv2.total_ht == 55
    assert inv2.total_tva == 42
    assert inv2.date == date_20190101
    assert inv2.name == None
    assert inv2.remote_invoice_number == "abcd"

    assert len(inv2.lines) == 2

    # Check one line
    assert inv2.lines[0].type_id == expense_type.id
    assert inv2.lines[0].description == "ia"
    assert inv2.lines[0].ht == 50
    assert inv2.lines[0].tva == 40
