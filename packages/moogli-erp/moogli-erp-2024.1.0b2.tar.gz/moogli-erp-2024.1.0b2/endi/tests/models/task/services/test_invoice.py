import datetime
from endi.models.task.services import InvoiceService
from endi.compute.math_utils import integer_to_amount


class TestInvoiceService:
    def test_duplicate(
        self, get_csrf_request_with_db, full_invoice, user, customer, project, phase
    ):
        result = InvoiceService.duplicate(
            get_csrf_request_with_db(),
            full_invoice,
            user,
            project=project,
            customer=customer,
            phase=phase,
        )
        assert len(full_invoice.default_line_group.lines) == len(
            result.default_line_group.lines
        )
        assert len(full_invoice.discounts) == len(result.discounts)
        assert result.mentions == full_invoice.mentions

    def test_duplicate_financial_year(
        self, get_csrf_request_with_db, full_invoice, user, customer, project, phase
    ):
        full_invoice.financial_year = 2010
        result = InvoiceService.duplicate(
            get_csrf_request_with_db(),
            full_invoice,
            user,
            project=project,
            customer=customer,
            phase=phase,
        )
        assert result.financial_year == datetime.date.today().year


class TestInternalInvoiceProcessService:
    def test_sync_with_customer(
        self,
        internal_customer,
        mk_internalinvoice,
        mk_expense_type,
        task_line,
        task_line_group,
        dbsession,
        get_csrf_request_with_db,
    ):
        task_line_group.lines = [task_line]
        invoice = mk_internalinvoice(status="valid")
        invoice.official_number = "123456"
        invoice.line_groups = [task_line_group]
        dbsession.add(invoice)
        dbsession.flush()

        request = get_csrf_request_with_db(context=invoice)
        supplier_invoice = invoice.sync_with_customer(request)

        assert invoice.supplier_invoice_id == supplier_invoice.id
        assert integer_to_amount(supplier_invoice.total, 2) == integer_to_amount(
            invoice.total(), 5
        )
        assert supplier_invoice.supplier.source_company_id == invoice.company_id

        typ = mk_expense_type(internal=True, label="Type interne")
        supplier_invoice = invoice.sync_with_customer(request)
        assert supplier_invoice.lines[0].type_id == typ.id


class TestInternalCancelInvoiceProcessService:
    def test_sync_with_customer(
        self,
        internal_customer,
        mk_internalcancelinvoice,
        mk_expense_type,
        task_line,
        task_line_group,
        dbsession,
        get_csrf_request_with_db,
        user,
    ):
        task_line.cost = -1 * task_line.cost
        task_line_group.lines = [task_line]
        invoice = mk_internalcancelinvoice(status="valid")
        invoice.official_number = "123456"
        invoice.line_groups = [task_line_group]
        dbsession.add(invoice)
        dbsession.flush()

        request = get_csrf_request_with_db(context=invoice, user=user)
        supplier_invoice = invoice.sync_with_customer(request)

        assert invoice.supplier_invoice_id == supplier_invoice.id
        assert integer_to_amount(supplier_invoice.total, 2) == integer_to_amount(
            invoice.total(), 5
        )
        assert supplier_invoice.supplier.source_company_id == invoice.company_id

        typ = mk_expense_type(internal=True, label="Type interne")
        supplier_invoice = invoice.sync_with_customer(request)
        assert supplier_invoice.lines[0].type_id == typ.id
        assert supplier_invoice.status == "valid"
        assert supplier_invoice.paid_status == "resulted"
