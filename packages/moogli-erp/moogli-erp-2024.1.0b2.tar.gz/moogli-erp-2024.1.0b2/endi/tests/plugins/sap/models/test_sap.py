import datetime
from decimal import Decimal


def test_adding_lines(company, customer, date_20190101):
    from endi.plugins.sap.models.sap import SAPAttestationLine

    l1 = SAPAttestationLine(
        company=company,
        customer=customer,
        category="cat",
        date=date_20190101,
        quantity=3,
        unit="m³",
        amount=Decimal("10.2"),
        product_id=4242,
    )

    l2 = SAPAttestationLine(
        company=company,
        customer=customer,
        category="cat",
        date=date_20190101,
        quantity=1,
        unit="m³",
        amount=Decimal("2.1"),
        product_id=4343,
    )

    lt = l1 + l2

    assert lt.company == company
    assert lt.customer == customer
    assert lt.category == "cat"
    assert lt.date == date_20190101
    assert lt.quantity == 4
    assert lt.unit == "m³"
    assert lt.amount == Decimal("12.3")
    assert lt.product_id is None


def test_attestation_get_cesu_sum(
    dbsession,
    customer,
    customer_2,
    date_20190101,
    mk_customer,
    mk_sapinvoice,
    mk_payment,
    mk_task_line,
):
    from endi.plugins.sap.models.sap import SAPAttestation

    invoice_1_2019 = mk_sapinvoice(customer=customer, date=datetime.date(2019, 5, 5))
    invoice_1_2020 = mk_sapinvoice(
        date=datetime.date(2020, 4, 30),
        customer=customer,
    )
    invoice_2_2019 = mk_sapinvoice(
        date=datetime.date(2019, 5, 5),
        customer=customer_2,
    )

    p1 = mk_payment(
        date=datetime.date(2019, 6, 6),
        amount=100000,
        task=invoice_1_2019,
        mode="Chèque CeSu",
    )
    mk_payment(date=datetime.date(2019, 6, 7), amount=4200000, task=invoice_1_2019)
    mk_payment(
        date=datetime.date(2020, 2, 1),
        amount=200000,
        task=invoice_1_2020,
        mode="Chèque CeSu",
    )
    mk_payment(
        date=datetime.date(2019, 7, 7),
        amount=500000,
        task=invoice_2_2019,
        mode="Chèque CeSu",
    )

    attestation = SAPAttestation(customer_id=customer.id, year=2019)
    cesu_amount = attestation.get_cesu_sum()
    # Only p1
    assert cesu_amount == 100000  # 1€

    p1.date = datetime.date(2020, 1, 1)
    dbsession.merge(p1)
    dbsession.flush()
    attestation = SAPAttestation(customer_id=customer.id, year=2019)
    cesu_amount = attestation.get_cesu_sum()
    # p1
    assert cesu_amount == 100000  # 1€

    attestation = SAPAttestation(customer_id=customer.id, year=2020)
    cesu_amount = attestation.get_cesu_sum()
    # Only p2
    assert cesu_amount == 200000  # 1€
