import pytest
import datetime


def test_payment_add(full_invoice, get_csrf_request_with_db, login, bank, tva):
    request = get_csrf_request_with_db(user=login.user)
    from endi_payment.public import PaymentService

    service = PaymentService(None, request)

    params = {"amount": 2000000, "mode": "cheque", "bank_id": bank.id, "tva": tva}
    service.add(full_invoice, params)

    assert len(full_invoice.payments) == 1
    assert full_invoice.payments[0].amount == 2000000


def test_payment_update(payment, get_csrf_request_with_db, login, tva):
    request = get_csrf_request_with_db(user=login.user)
    from endi_payment.public import PaymentService

    service = PaymentService(None, request)

    params = {"amount": 2000000, "mode": "cheque", "tva": tva}
    service.update(payment, params)

    assert payment.mode == "cheque"
    assert payment.amount == 2000000


def test_payment_delete(payment, full_invoice, get_csrf_request_with_db, login, tva):
    invoice_id = full_invoice.id
    from endi.models.task.payment import Payment

    payment_id = payment.id
    payment.tva = tva
    request = get_csrf_request_with_db(user=login.user)
    from endi_payment.public import PaymentService

    service = PaymentService(None, request)
    service.delete(payment)

    from endi.models.task import Invoice

    invoice = Invoice.get(invoice_id)

    assert len(invoice.payments) == 0
    assert Payment.get(payment_id) == None
