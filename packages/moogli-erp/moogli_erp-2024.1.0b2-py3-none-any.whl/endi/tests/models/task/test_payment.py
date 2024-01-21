import datetime
from pytest import fixture


@fixture
def invoice2(mk_invoice):
    return mk_invoice()


@fixture
def invoice3(mk_invoice, company2):
    return mk_invoice(company=company2)


@fixture
def payment1(mk_payment):
    return mk_payment(
        date=datetime.date(2019, 10, 1),
        amount=1000000,
        bank_remittance_id="REM_ID",
        check_number="0123456789",
        exported=1,
    )


@fixture
def payment2(mk_payment, invoice2):
    return mk_payment(
        date=datetime.date(2019, 10, 1),
        amount=2000000,
        bank_remittance_id="REM_ID",
        check_number="0123456789",
        exported=1,
        task=invoice2,
    )


@fixture
def payment3(mk_payment):
    return mk_payment(
        date=datetime.date(2019, 10, 1),
        amount=3000000,
        bank_remittance_id="REM_ID",
        check_number="9876543210",
        exported=1,
    )


@fixture
def payment4(mk_payment, invoice3):
    return mk_payment(
        date=datetime.date(2019, 10, 1),
        amount=4000000,
        bank_remittance_id="REM_ID",
        check_number="9876543210",
        exported=1,
        task=invoice3,
    )


def test_remittance_get_total_amount(bank_remittance, payment1, payment2, payment3):
    bank_remittance.payments = [payment1, payment2, payment3]
    assert bank_remittance.get_total_amount() == 6000000


def test_remittance_get_grouped_payments(
    bank_remittance, payment1, payment2, payment3, global_seq_1, global_seq_2
):
    bank_remittance.payments = [payment1, payment2, payment3]
    grouped_payments = bank_remittance.get_grouped_payments()
    expected_values = [
        {
            "amount": payment1.amount + payment2.amount,
            "bank_label": payment1.customer_bank.label,
            "check_number": payment1.check_number,
            "code_compta": payment1.invoice.company.code_compta,
            "date": payment1.date,
            "invoice_ref": "{0} + {1}".format(global_seq_1.index, global_seq_2.index),
            "issuer": payment1.issuer,
        },
        {
            "amount": payment3.amount,
            "bank_label": payment3.customer_bank.label,
            "check_number": payment3.check_number,
            "code_compta": payment3.invoice.company.code_compta,
            "date": payment3.date,
            "invoice_ref": "{}".format(global_seq_1.index),
            "issuer": payment3.issuer,
        },
    ]
    assert grouped_payments == expected_values
