import pytest
import datetime
from endi.models.task.services import InternalPaymentService
from endi.compute.math_utils import integer_to_amount


class TestInternalPaymentService:
    @pytest.fixture
    def my_invoice(
        self,
        dbsession,
        mk_internalinvoice,
        task_line_group,
        mk_task_line,
    ):
        task_line_group.lines = [mk_task_line(cost=100000000)]
        invoice = mk_internalinvoice(status="valid", official_number="123456")
        invoice.line_groups = [task_line_group]
        dbsession.add(invoice)
        dbsession.flush()
        return invoice

    def test_sync_with_customer_paid_then_update(
        self,
        internal_customer,
        mk_internalpayment,
        my_invoice,
        dbsession,
        get_csrf_request_with_db,
        user,
    ):
        frns_invoice = my_invoice.sync_with_customer(
            get_csrf_request_with_db(context=my_invoice)
        )

        payment = mk_internalpayment(task=my_invoice, amount=60000000)
        my_invoice.check_resulted()

        request = get_csrf_request_with_db(context=payment, user=user)
        frns_payment = payment.sync_with_customer(request, action="add")

        assert integer_to_amount(frns_payment.amount, 2) == integer_to_amount(
            60000000, 5
        )

        assert frns_invoice.paid_status == "paid"

        payment.amount += 60000000
        dbsession.merge(payment)
        dbsession.flush()
        my_invoice.check_resulted()

        request = get_csrf_request_with_db(context=payment, user=user)
        frns_payment = payment.sync_with_customer(
            request, action="update", amount=60000000
        )
        assert frns_invoice.paid_status == "resulted"

    def test_sync_with_customer_on_delete_payment(
        self,
        internal_customer,
        mk_internalpayment,
        my_invoice,
        dbsession,
        get_csrf_request_with_db,
        user,
    ):
        frns_invoice = my_invoice.sync_with_customer(
            get_csrf_request_with_db(context=my_invoice)
        )
        payment = mk_internalpayment(task=my_invoice, amount=120000000)
        my_invoice.paid_status = "resulted"
        payment.sync_with_customer(
            get_csrf_request_with_db(context=payment, user=user), action="add"
        )
        dbsession.delete(payment)
        dbsession.flush()
        my_invoice.check_resulted()

        payment.sync_with_customer(
            get_csrf_request_with_db(context=payment, user=user),
            action="delete",
            amount=120000000,
        )
        assert frns_invoice.paid_status == "waiting"

    def test_sync_with_customer_resulted_with_cinvoice(
        self,
        internal_customer,
        mk_internalpayment,
        mk_internalcancelinvoice,
        mk_internalinvoice,
        task_line,
        task_line_group,
        mk_task_line,
        dbsession,
        get_csrf_request_with_db,
        user,
    ):
        task_line_group.lines = [mk_task_line(cost=100000000)]
        invoice = mk_internalinvoice(status="valid", official_number="123456")
        invoice.line_groups = [task_line_group]
        dbsession.add(invoice)
        dbsession.flush()
        frns_invoice = invoice.sync_with_customer(
            get_csrf_request_with_db(context=invoice, user=user)
        )

        cinvoice = mk_internalcancelinvoice(
            status="valid", official_number="123456", invoice=invoice
        )
        cinvoice.line_groups[0].lines = [mk_task_line(cost=-50000000)]
        dbsession.add(cinvoice)
        dbsession.flush()
        cinvoice.sync_with_customer(
            get_csrf_request_with_db(context=cinvoice, user=user)
        )

        payment = mk_internalpayment(task=invoice, amount=60000000)
        invoice.check_resulted()

        request = get_csrf_request_with_db(context=payment, user=user)
        frns_payment = payment.sync_with_customer(request, action="add")

        assert integer_to_amount(frns_payment.amount, 2) == integer_to_amount(
            60000000, 5
        )
        assert integer_to_amount(frns_invoice.total, 2) == integer_to_amount(
            invoice.total(), 5
        )

        assert frns_invoice.paid_status == "resulted"
