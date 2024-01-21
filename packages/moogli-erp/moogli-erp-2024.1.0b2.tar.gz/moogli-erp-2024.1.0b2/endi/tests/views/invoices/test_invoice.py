import datetime

from endi.models.task.invoice import Invoice
from endi.views.invoices.invoice import (
    InvoiceDuplicateView,
)


TODAY = datetime.date.today()


class TestInvoiceDuplicate:
    def duplicate_one(
        self,
        config,
        request,
        customer,
        project,
        full_invoice,
    ):
        config.add_route("/invoices/{id}", "/")
        params = {
            "customer_id": customer.id,
            "project_id": project.id,
            "business_type_id": full_invoice.business_type_id,
        }
        request.context = full_invoice
        view = InvoiceDuplicateView(request)
        view.submit_success(params)

    def get_one(self):
        return Invoice.query().order_by(Invoice.id.desc()).first()

    def test_duplicate_common(
        self,
        config,
        get_csrf_request_with_db_and_user,
        mk_customer,
        mk_project,
        full_invoice,
    ):
        new_customer = mk_customer(name="newcustomer")
        new_project = mk_project(name="newproject", customers=[new_customer])
        request = get_csrf_request_with_db_and_user()
        self.duplicate_one(config, request, new_customer, new_project, full_invoice)
        invoice = self.get_one()
        assert invoice.type_ == "invoice"
        assert invoice.customer_id == new_customer.id
        assert invoice.project_id == new_project.id

    def test_duplicate_internal(
        self,
        config,
        get_csrf_request_with_db_and_user,
        mk_customer,
        mk_project,
        full_invoice,
        mk_tva,
        mk_product,
    ):
        new_tva = mk_tva(value=0, name="O%")
        new_product = mk_product(tva=new_tva, name="interne", internal=True)

        new_customer = mk_customer(name="newcustomer", type="internal")
        new_project = mk_project(name="newproject", customers=[new_customer])
        request = get_csrf_request_with_db_and_user()

        self.duplicate_one(config, request, new_customer, new_project, full_invoice)
        invoice = self.get_one()
        assert invoice.type_ == "internalinvoice"
        assert invoice.customer_id == new_customer.id
        assert invoice.project_id == new_project.id
        for line in invoice.all_lines:
            assert line.tva == new_tva.value
            assert line.product_id == new_product.id
