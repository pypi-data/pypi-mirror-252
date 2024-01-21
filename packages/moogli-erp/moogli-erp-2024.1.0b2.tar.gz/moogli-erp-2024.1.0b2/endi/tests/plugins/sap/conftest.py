import datetime
from pytest import fixture

from endi.tests.compute.conftest import invoice_multitva_payments


@fixture
def customer_1(mk_customer, company):
    return mk_customer(type="individual", name="John", company=company)


@fixture
def customer_2(mk_customer, company):
    return mk_customer(type="individual", name="Jack", company=company)


@fixture
def company_2(mk_company):
    return mk_company()


@fixture
def customer_company_2(mk_customer, company_2):
    return mk_customer(type="individual", name="Fried", company=company_2)


@fixture
def fully_paid_invoice(
    customer_1,
    dbsession,
    mk_fully_paid_invoice,
):
    # w customer.type = individual
    return mk_fully_paid_invoice(
        customer=customer_1,
    )


@fixture
def paid_invoice_accross_2019_2020(
    customer_1,
    date_20200101,
    dbsession,
    mk_fully_paid_invoice,
    mk_payment,
):
    invoice = mk_fully_paid_invoice(customer=customer_1)

    # 2 payments : 20% / 80%
    payment1 = invoice.payments[0]  # date_20190101
    payment2 = mk_payment(
        amount=int(0.8 * payment1.amount),
        bank_remittance_id="REM_ID",
        exported=1,
        date=date_20200101,
    )
    payment1.amount = int(payment1.amount * 0.2)
    invoice.payments.append(payment2)
    dbsession.merge(invoice)
    dbsession.merge(payment2)
    dbsession.merge(payment1)

    return invoice


@fixture
def fully_paid_invoice_2(
    customer_1,
    dbsession,
    mk_fully_paid_invoice,
):
    return mk_fully_paid_invoice(
        customer=customer_1,
        financial_year=2019,
        status="valid",
    )


@fixture
def partly_paid_invoice(
    customer_1,
    date_20190101,
    dbsession,
    bank_remittance,
    mk_invoice,
    mk_payment,
    mk_product,
    mk_task_line,
    mk_task_line_group,
):
    inv = mk_invoice(year=2019, status="valid", customer=customer_1)
    group = mk_task_line_group()
    inv.lines = [
        mk_task_line(
            date=date_20190101,
            group=group,
            product=mk_product(name="jardinage"),
            cost=1000000,
        ),
        mk_task_line(
            date=date_20190101,
            group=group,
            product=mk_product(name="bricolage"),
            cost=2000000,
        ),
    ]
    inv.line_groups = [group]

    inv.payments = [
        mk_payment(
            amount=500000, bank_remittance_id="REM_ID", exported=1, date=date_20190101
        ),
        mk_payment(
            amount=700000,
            bank_remittance_id="REM_ID",
            exported=1,
            date=date_20190101,
        ),
    ]
    inv = dbsession.merge(inv)
    inv.check_resulted()
    dbsession.flush()
    return inv


@fixture
def fully_paid_invoice_customer_2(
    customer_2,
    dbsession,
    mk_fully_paid_invoice,
):
    return mk_fully_paid_invoice(
        financial_year=2019,
        status="valid",
        customer=customer_2,
    )


@fixture
def fully_paid_invoice_company_2(
    mk_fully_paid_invoice,
    company_2,
    customer_company_2,
):
    return mk_fully_paid_invoice(
        financial_year=2019,
        status="valid",
        company=company_2,
        customer=customer_company_2,
    )


@fixture
def fully_paid_invoice_with_discount(customer_1, mk_fully_paid_invoice):
    return mk_fully_paid_invoice(
        financial_year=2019,
        status="valid",
        with_discount=True,
        customer=customer_1,
    )


@fixture
def mk_sapinvoice(
    dbsession,
    mk_invoice,
    mk_task_line_group,
    mk_task_line,
):
    def builder(date=datetime.date.today(), cost=100000, **kw):
        invoice = mk_invoice(**kw)
        tgroup = mk_task_line_group()
        tline = mk_task_line(date=date, cost=cost, group=tgroup)
        tgroup.lines = [tline]
        invoice.line_groups = [tgroup]
        invoice = dbsession.merge(invoice)
        dbsession.flush()
        return invoice

    return builder
