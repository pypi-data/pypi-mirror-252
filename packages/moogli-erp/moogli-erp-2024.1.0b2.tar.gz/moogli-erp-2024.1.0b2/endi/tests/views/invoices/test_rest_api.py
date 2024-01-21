import pytest
from endi.models.task import Invoice
from endi.views.project.routes import PROJECT_ITEM_INVOICE_ROUTE
from endi.tests.tools import Dummy
from endi.views.invoices.rest_api import InvoiceAddRestView
from endi.views.invoices.routes import (
    API_INVOICE_ADD_ROUTE,
    INVOICE_ITEM_ROUTE,
    CINV_ITEM_ROUTE,
)


class TestInvoiceAddRestView:
    @pytest.fixture
    def view_result(
        self,
        get_csrf_request_with_db,
        company,
        project,
        customer,
        phase,
        default_business_type,
    ):
        def callview(params={}):
            props = {}
            props.update(
                {
                    "name": "Facture",
                    "business_type_id": str(default_business_type.id),
                    "project_id": str(project.id),
                    "phase_id": str(phase.id),
                    "customer_id": str(customer.id),
                }
            )
            props.update(params)
            project.__name__ = "project"
            request = get_csrf_request_with_db(
                post=props,
                current_route_path=API_INVOICE_ADD_ROUTE,
                context=company,
            )

            view = InvoiceAddRestView(company, request)
            view.post()
            return Invoice.query().all()[-1]

        return callview

    def test_add_invoice(
        self,
        view_result,
        project,
        phase,
        company,
        customer,
        default_business_type,
    ):
        invoice = view_result()
        assert invoice.name == "Facture"
        assert invoice.company == company
        assert invoice.phase == phase
        assert invoice.customer == customer
        assert invoice.project == project
        assert invoice.business_type == default_business_type

    def test_add_invoice_attach_customer_to_project(
        self,
        view_result,
        project,
        phase,
        company,
        customer,
        mk_customer,
        default_business_type,
    ):
        # Ref #3609
        customer_without_project = mk_customer()
        invoice = view_result({"customer_id": customer_without_project.id})
        assert invoice.name == "Facture"
        assert invoice.company == company
        assert invoice.phase == phase
        assert invoice.customer == customer_without_project
        assert invoice.project == project
        assert invoice.business_type == default_business_type

        assert customer_without_project.projects == [project]

    def test_add_internalinvoice(
        self,
        view_result,
        project,
        phase,
        company,
        mk_customer,
        default_business_type,
    ):
        int_customer = mk_customer(type="internal", name="test")
        project.customers.append(int_customer)
        invoice = view_result({"customer_id": int_customer.id})

        assert invoice.type_ == "internalinvoice"
        assert invoice.name == "Facture"
        assert invoice.company == company
        assert invoice.phase == phase
        assert invoice.customer == int_customer
        assert invoice.project == project
        assert invoice.business_type == default_business_type


def test_invoice_valid_view(config, get_csrf_request_with_db, full_invoice, user):
    config.add_route(INVOICE_ITEM_ROUTE, INVOICE_ITEM_ROUTE)
    config.testing_securitypolicy(userid="test", identity="admin", permissive=True)
    from endi.views.invoices.rest_api import InvoiceStatusRestView

    request = get_csrf_request_with_db(
        post={"submit": "valid", "comment": "Test comment"},
        context=full_invoice,
        user=user,
    )
    request.is_xhr = True

    view = InvoiceStatusRestView(request)
    result = view.__call__()
    assert result == {"redirect": INVOICE_ITEM_ROUTE.format(id=full_invoice.id)}
    assert full_invoice.status == "valid"
    assert full_invoice.statuses[-1].comment == "Test comment"
    assert full_invoice.statuses[-1].status == "valid"


def test_invoice_datechange_callback(
    dbsession, config, get_csrf_request_with_db, full_invoice, user
):
    import datetime
    from endi.views.invoices.rest_api import InvoiceRestView

    config.add_route(PROJECT_ITEM_INVOICE_ROUTE, PROJECT_ITEM_INVOICE_ROUTE)

    full_invoice.financial_year = 2015
    full_invoice.date = datetime.date(2015, 1, 1)
    dbsession.merge(full_invoice)

    request = get_csrf_request_with_db(
        post={"date": "2016-01-01"}, context=full_invoice, user=user
    )

    view = InvoiceRestView(request)
    view.put()

    assert full_invoice.financial_year == 2016


def test_cancelinvoice_valid_view(
    config, get_csrf_request_with_db, full_cancelinvoice, full_invoice, user
):
    config.add_route(CINV_ITEM_ROUTE, CINV_ITEM_ROUTE)
    config.testing_securitypolicy(userid="test", identity="admin", permissive=True)
    from endi.views.invoices.rest_api import CancelInvoiceStatusRestView

    request = get_csrf_request_with_db(
        post={"submit": "valid", "comment": "Test comment"},
        context=full_cancelinvoice,
        user=user,
    )
    request.is_xhr = True
    view = CancelInvoiceStatusRestView(request)
    result = view.__call__()
    assert result == {"redirect": CINV_ITEM_ROUTE.format(id=full_cancelinvoice.id)}
    assert full_cancelinvoice.status == "valid"
    assert full_cancelinvoice.statuses[-1].comment == "Test comment"
    assert full_cancelinvoice.statuses[-1].status == "valid"
    assert full_invoice.paid_status == "resulted"
