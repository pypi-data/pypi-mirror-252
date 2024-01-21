from endi.models.supply.internalsupplier_invoice import InternalSupplierInvoice


def test_internalsupplier_invoice_from_invoice(internalinvoice, supplier):
    internalinvoice.official_number = "4242"
    supplier_invoice = InternalSupplierInvoice.from_invoice(internalinvoice, supplier)

    assert supplier_invoice.remote_invoice_number == "4242"
    assert supplier_invoice.date == internalinvoice.date
    assert len(supplier_invoice.lines) == 1


def test_internalsupplier_invoice_resulted(
    dbsession,
    internalinvoice,
    mk_task_line_group,
    mk_task_line,
    supplier,
    mk_internalsupplier_payment,
):
    line = mk_task_line(cost=10000000, tva=2000, quantity=1)
    group = mk_task_line_group()
    group.lines = [line]
    internalinvoice.line_groups = [group]
    dbsession.merge(internalinvoice)
    dbsession.flush()

    supplier_invoice = InternalSupplierInvoice.from_invoice(internalinvoice, supplier)
    assert supplier_invoice.total == 12000
    payment = mk_internalsupplier_payment(
        supplier_invoice=supplier_invoice, amount=12000
    )
    supplier_invoice.record_payment(payment)
    assert supplier_invoice.paid_status == "resulted"
    assert supplier_invoice.supplier_paid_status == "resulted"
    assert supplier_invoice.worker_paid_status == "resulted"
