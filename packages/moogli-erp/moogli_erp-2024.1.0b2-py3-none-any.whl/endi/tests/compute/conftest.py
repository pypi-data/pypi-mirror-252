import pytest

from endi.models.task import (
    TaskLine,
    TaskLineGroup,
)

from datetime import date


@pytest.fixture
def mk_task(fixture_factory, user, company, project, customer, default_business_type):
    from endi.models.task.task import Task

    return fixture_factory(
        Task,
        user=user,
        company=company,
        project=project,
        customer_id=customer.id,
        customer=customer,
        business_type=default_business_type,
    )


@pytest.fixture
def invoice_multitva_payments(
    def_tva, tva10, tva20, tva55, invoice_ht_mode, customer, company, mk_product
):
    # Invoice contains
    # 2xA 24€HT = 48€HT
    # 5xB 78.5€HT = 392.5€HT
    # 8xC 45.58€HT = 364.64€HT
    # Total 805.14€HT 874.0452€TTC -> 874.05€TTC

    prodA = mk_product(tva=tva20, name="A")
    prodB = mk_product(tva=tva10, name="B")
    prodC = mk_product(tva=tva55, name="C")

    lines = []
    lines.append(
        TaskLine(
            cost=2400000,
            quantity=2,
            tva=tva20.value,
            product=prodA,
            mode="ht",
            date=date(2021, 3, 1),
            unity="h",
        )
    )
    lines.append(
        TaskLine(
            cost=7850000,
            quantity=5,
            tva=tva10.value,
            product=prodB,
            mode="ht",
            date=date(2021, 3, 1),
            unity="h",
        )
    )
    lines.append(
        TaskLine(
            cost=4558000,
            quantity=8,
            tva=tva55.value,
            product=prodC,
            mode="ht",
            date=date(2021, 3, 1),
            unity="h",
        )
    )

    invoice = invoice_ht_mode
    invoice.default_tva = def_tva.value
    invoice.expenses_tva = def_tva.value
    invoice.date = date(2021, 3, 1)
    invoice.customer = customer
    invoice.company = company
    invoice.official_number = "INV_005"
    invoice.line_groups = [TaskLineGroup(lines=lines)]
    invoice.expenses_ht = 0
    invoice.expenses = 0
    invoice.status = "valid"
    return invoice


@pytest.fixture
def payment_line_1(mk_payment_line):
    return mk_payment_line(amount=4000000)


@pytest.fixture
def payment_line_2(mk_payment_line):
    return mk_payment_line(amount=6000000)


@pytest.fixture
def payment_line_3(mk_payment_line):
    return mk_payment_line(amount=50000)


@pytest.fixture
def empty_task(mk_task):
    return mk_task(mode="ht")


@pytest.fixture
def empty_task_ttc(mk_task):
    return mk_task(mode="ttc")


@pytest.fixture
def empty_ht_estimation(mk_estimation):
    return mk_estimation(mode="ht")


@pytest.fixture
def cancelinvoice_1(
    mk_cancelinvoice,
):
    return mk_cancelinvoice(status="valid")


@pytest.fixture
def cancelinvoice_2(
    mk_cancelinvoice,
):
    return mk_cancelinvoice(status="valid")


@pytest.fixture
def payment_one(mk_payment):
    return mk_payment(amount=1500000)


@pytest.fixture
def payment_two(mk_payment):
    return mk_payment(amount=1000000)
