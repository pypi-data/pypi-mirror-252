import datetime


def test_number_collision_fix2975(
    mk_supplier_invoice,
    pyramid_request,
    csrf_request_with_db_and_user,
):
    from endi.models.config import Config

    Config.set("supplierinvoice_number_template", "{YY}-{MM}-{SEQMONTH}")

    supplier_invoice_1 = mk_supplier_invoice(
        status_date=datetime.date(2021, 9, 1), date=datetime.date(2021, 9, 1)
    )
    supplier_invoice_2 = mk_supplier_invoice(
        status_date=datetime.date(2021, 10, 1), date=datetime.date(2021, 9, 1)
    )

    assert supplier_invoice_1.official_number is None
    assert supplier_invoice_2.official_number is None

    supplier_invoice_1.set_validation_status("valid", csrf_request_with_db_and_user)
    assert supplier_invoice_1.official_number == "21-09-1"

    supplier_invoice_2.set_validation_status("valid", csrf_request_with_db_and_user)
    assert supplier_invoice_2.official_number == "21-09-2"
