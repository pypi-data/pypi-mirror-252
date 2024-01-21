def test_supplier_invoice_parts(half_cae_supplier_invoice):
    assert half_cae_supplier_invoice.cae_total == 552
    assert half_cae_supplier_invoice.worker_total == 551


def test_supplier_invoice_line_parts(half_cae_supplier_invoice):
    line1, line2 = half_cae_supplier_invoice.lines

    assert line1.cae_total == 550
    assert line1.worker_total == 549

    assert line2.cae_total == 2
    assert line2.worker_total == 2


def test_supplier_invoice_parts_payments(
    half_cae_supplier_invoice,
    mk_supplier_payment,
    mk_user_payment,
):
    assert half_cae_supplier_invoice.paid() == 0
    assert half_cae_supplier_invoice.cae_paid() == 0
    assert half_cae_supplier_invoice.worker_paid() == 0

    assert half_cae_supplier_invoice.topay() == 1103
    assert half_cae_supplier_invoice.cae_topay() == 552
    assert half_cae_supplier_invoice.worker_topay() == 551

    mk_supplier_payment(
        supplier_invoice=half_cae_supplier_invoice,
        amount=200,
    )
    mk_user_payment(
        supplier_invoice=half_cae_supplier_invoice,
        amount=100,
    )

    assert half_cae_supplier_invoice.paid() == 300
    assert half_cae_supplier_invoice.cae_paid() == 200
    assert half_cae_supplier_invoice.worker_paid() == 100

    assert half_cae_supplier_invoice.topay() == 803
    assert half_cae_supplier_invoice.cae_topay() == 352
    assert half_cae_supplier_invoice.worker_topay() == 451
