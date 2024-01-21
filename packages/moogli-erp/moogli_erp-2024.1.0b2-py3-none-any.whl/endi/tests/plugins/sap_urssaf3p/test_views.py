def test_invoice_request_controller(invoice, csrf_request_with_db_and_user):
    from endi.plugins.sap_urssaf3p.views.payment_request import InvoiceRequestController

    request = csrf_request_with_db_and_user

    c = InvoiceRequestController(request)
    c.set_request_status(invoice, request.identity, status="waiting")
    assert invoice.urssaf_payment_request.request_status == "waiting"


def test_invoice_request_controller_updated_at(invoice, csrf_request_with_db_and_user):
    from endi.plugins.sap_urssaf3p.views.payment_request import InvoiceRequestController

    request = csrf_request_with_db_and_user

    c = InvoiceRequestController(request)
    c.set_request_status(invoice, request.identity, status="waiting")
    dt1 = invoice.urssaf_payment_request.updated_at

    c.set_request_status(invoice, request.identity, status="other")
    dt2 = invoice.urssaf_payment_request.updated_at

    assert dt1 != dt2, "set_request_status should update Node.updated_at"
