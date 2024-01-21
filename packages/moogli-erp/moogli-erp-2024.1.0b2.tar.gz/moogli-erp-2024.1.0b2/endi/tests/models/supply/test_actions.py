def test_supplier_invoice_validation_sets_official_number(
    mk_supplier_invoice,
    pyramid_request,
    csrf_request_with_db_and_user,
    content,
):
    supplier_invoice_1 = mk_supplier_invoice()
    supplier_invoice_2 = mk_supplier_invoice()

    assert supplier_invoice_1.official_number is None
    assert supplier_invoice_2.official_number is None

    supplier_invoice_1.set_validation_status("valid", csrf_request_with_db_and_user)
    assert supplier_invoice_1.official_number == "1"

    supplier_invoice_2.set_validation_status("valid", csrf_request_with_db_and_user)
    assert supplier_invoice_2.official_number == "2"


def test_externalsupplier_invoice_validation_doesnt_set_resulted(
    mk_supplier_invoice,
    mk_supplier_invoice_line,
    pyramid_request,
    csrf_request_with_db_and_user,
    content,
):
    # negative supplier_invoice but external
    supplier_invoice = mk_supplier_invoice()
    mk_supplier_invoice_line(supplier_invoice=supplier_invoice, ht=-50000, tva=-10000)

    supplier_invoice.set_validation_status("valid", csrf_request_with_db_and_user)
    assert supplier_invoice.worker_paid_status == "waiting"
    assert supplier_invoice.paid_status == "waiting"
    assert supplier_invoice.supplier_paid_status == "waiting"


def test_internalsupplier_invoice_validation_sets_resulted_when_negative(
    mk_internalsupplier_invoice,
    mk_supplier_invoice_line,
    pyramid_request,
    csrf_request_with_db_and_user,
    content,
):
    # negative internalsupplier_invoice
    supplier_invoice = mk_internalsupplier_invoice()
    mk_supplier_invoice_line(supplier_invoice=supplier_invoice, ht=-50000, tva=-10000)

    supplier_invoice.set_validation_status("valid", csrf_request_with_db_and_user)
    assert supplier_invoice.worker_paid_status == "resulted"
    assert supplier_invoice.paid_status == "resulted"
    assert supplier_invoice.supplier_paid_status == "resulted"


def test_internalsupplier_invoice_validation_sets_not_resulted_when_positive(
    mk_internalsupplier_invoice,
    mk_supplier_invoice_line,
    pyramid_request,
    csrf_request_with_db_and_user,
    content,
):
    # positive internalsupplier_invoice
    supplier_invoice = mk_internalsupplier_invoice()
    mk_supplier_invoice_line(supplier_invoice=supplier_invoice, ht=50000, tva=10000)

    supplier_invoice.set_validation_status("valid", csrf_request_with_db_and_user)
    assert supplier_invoice.worker_paid_status == "waiting"
    assert supplier_invoice.paid_status == "waiting"
    assert supplier_invoice.supplier_paid_status == "waiting"
