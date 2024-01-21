import pytest

from endi.plugins.sap.models.services.attestation import SAPAttestationLineService

pytestmark = [pytest.mark.plugin_sap]


@pytest.fixture
def overpaid_invoice_w_discount(
    customer_1,
    dbsession,
    discount_line,
    mk_fully_paid_invoice,
):
    invoice = mk_fully_paid_invoice(customer=customer_1)
    invoice.discounts.append(discount_line)  # - 12€TTC
    # there is now an overpayment of 12€
    dbsession.merge(invoice)
    dbsession.flush()
    return invoice


@pytest.fixture
def underpaid_invoice_w_expenses(
    customer_1,
    dbsession,
    discount_line,
    mk_fully_paid_invoice,
    mk_task_line,
):
    invoice = mk_fully_paid_invoice(customer=customer_1)
    # 2 expenses of 12€TTC and 6€TTC
    l1 = mk_task_line(cost=500000, unity="km")
    l2 = mk_task_line(cost=1000000, unity="km")
    invoice.line_groups[0].lines = invoice.line_groups[0].lines + [l1, l2]
    dbsession.merge(invoice)
    dbsession.flush()
    return invoice


@pytest.fixture
def fully_paid_invoice_w_expenses(
    dbsession, date_20190101, mk_payment, underpaid_invoice_w_expenses
):
    invoice = underpaid_invoice_w_expenses
    invoice.payments = invoice.payments + [
        mk_payment(date=date_20190101, amount=1800000)
    ]
    dbsession.merge(invoice)
    dbsession.flush()
    return invoice


@pytest.fixture
def overpaid_invoice_w_negative_task_line(
    dbsession, customer_2, mk_fully_paid_invoice, mk_task_line, date_20190101
):
    invoice = mk_fully_paid_invoice(customer=customer_2)
    invoice.line_groups[0].lines.append(
        mk_task_line(cost=-500000, date=date_20190101)  # - 6€TTC
    )
    # there is now an overpayment of 6€
    dbsession.merge(invoice)
    dbsession.flush()
    return invoice


def test_get_regular_tasklines_no_enough_data():
    with pytest.raises(ValueError):
        list(SAPAttestationLineService().query(year=None))


def test_get_regular_tasklines_excluded(
    draft_invoice,
    unpaid_invoice,
):
    lines = SAPAttestationLineService().query(2019, set(), set())
    assert len(list(lines)) == 0


def test_get_unpaid_cancelled_invoice(
    dbsession, get_csrf_request_with_db, unpaid_invoice, user
):
    """
    Try to highlight the potential issue described in https://framagit.org/endi/endi/-/issues/3992
    """
    cinv = unpaid_invoice.gen_cancelinvoice(get_csrf_request_with_db(), user)
    cinv.status = "valid"
    cinv.financial_year = unpaid_invoice.financial_year
    dbsession.merge(cinv)
    dbsession.flush()

    lines = SAPAttestationLineService()._get_invoices(2019, set(), set())
    assert len(list(lines)) == 0


def test_get_alien_invoices_negative_taskline(
    overpaid_invoice_w_negative_task_line,
):
    query = SAPAttestationLineService()._get_invoices(2019, set(), set())
    assert query.count() == 1


def test_get_alien_invoices(partly_paid_invoice):
    query = SAPAttestationLineService()._get_invoices(
        year=2019, companies_ids=set(), customers_ids=set()
    )
    assert query.count() == 1


def test_get_alien_invoices_discount(overpaid_invoice_w_discount):
    query = SAPAttestationLineService()._get_invoices(2019, set(), set())
    assert query.count() == 1


def test_query(fully_paid_invoice):
    sap_lines = list(SAPAttestationLineService().query(year=2019))
    assert len(sap_lines) == 1
    assert sap_lines[0].amount == 12000000


def test_query_w_expenses(underpaid_invoice_w_expenses):
    sap_lines = list(SAPAttestationLineService().query(year=2019))
    assert len(sap_lines) == 3
    service_line, expense_line, epsilon_line = sap_lines
    assert sum(i.amount for i in sap_lines) == 12000000

    assert service_line.unit == "h"
    assert expense_line.unit == "frais"
    assert epsilon_line.unit == "h"


def test_query_w_expenses_fully_paid(fully_paid_invoice_w_expenses):
    sap_lines = list(SAPAttestationLineService().query(year=2019))
    assert len(sap_lines) == 2
    service_line, expense_line = sap_lines
    assert service_line.amount == 12000000
    assert expense_line.amount == 1800000


def test_query_partly_paid_invoice(partly_paid_invoice):
    sap_lines = list(SAPAttestationLineService().query(year=2019))
    assert len(sap_lines) == 2
    assert sap_lines[0].amount == 400000
    assert sap_lines[1].amount == 800000


def test_query_overpaid_invoice_w_discount(overpaid_invoice_w_discount):
    sap_lines = list(SAPAttestationLineService().query(year=2019))
    assert len(sap_lines) == 1
    assert sap_lines[0].amount == 10800000


def test_query_overpaid_invoice_w_negative_task_line(
    overpaid_invoice_w_negative_task_line,
):
    sap_lines = list(SAPAttestationLineService().query(year=2019))
    assert len(sap_lines) == 2
    assert sap_lines[0].amount == 12000000
    assert sap_lines[1].amount == -600000


def test_query_complex(
    fully_paid_invoice,  # 120€
    overpaid_invoice_w_discount,  # 108€
    overpaid_invoice_w_negative_task_line,  # 120 - 6
    partly_paid_invoice,  # 4€ + 8€
):
    lines = list(SAPAttestationLineService().query(year=2019))
    lines_amounts = [line.amount for line in lines]
    lines_amounts.sort()

    assert lines_amounts == [
        -600000,
        400000,
        800000,
        10800000,
        12000000,
        12000000,
    ]


def test_query_invoice_multi_year(
    paid_invoice_accross_2019_2020,
):
    lines_2019 = list(SAPAttestationLineService().query(year=2019))
    lines_2020 = list(SAPAttestationLineService().query(year=2020))

    assert len(lines_2019) == 1
    assert len(lines_2020) == 1

    assert lines_2019[0].amount == 2400000
    assert lines_2020[0].amount == 9600000


def test_query_payment_on_different_year(
    date_20210101,
    dbsession,
    fully_paid_invoice,
):
    # Invoice should appear in the attestations of the payment's year
    fully_paid_invoice.payments[0].date = date_20210101
    dbsession.merge(fully_paid_invoice.payments[0])
    dbsession.flush()

    # 2019
    sap_lines = list(SAPAttestationLineService().query(year=2019))
    assert len(sap_lines) == 0

    # 2020
    sap_lines = list(SAPAttestationLineService().query(year=2020))
    assert len(sap_lines) == 0

    # 2021
    sap_lines = list(SAPAttestationLineService().query(year=2021))
    assert len(sap_lines) == 1
    assert sap_lines[0].amount == 12000000


@pytest.fixture
def fully_paid_invoice_multitva_payments(
    bank_remittance,
    customer_2,
    date_20210101,
    dbsession,
    invoice_multitva_payments,
    mk_payment,
):
    payment = mk_payment(
        amount=87405000 - 100000,  # 100% - 1€
        bank_remittance_id="REM_ID",
        exported=1,
        date=date_20210101,
    )
    invoice_multitva_payments.payments = [payment]
    invoice_multitva_payments.customer = customer_2
    dbsession.merge(invoice_multitva_payments)
    dbsession.flush()
    return invoice_multitva_payments


def test_query_ignored(fully_paid_invoice_multitva_payments):
    line_service = SAPAttestationLineService()
    lines = list(line_service.query(year=2021))
    assert len(lines) == 0
    rejects = line_service.get_rejects()
    assert len(rejects) == 1
    assert rejects[0].invoice == fully_paid_invoice_multitva_payments
    assert "TVA" in rejects[0].msg


@pytest.fixture
def invoice_bug_3205(
    dbsession,
    date_20190101,
    mk_task_line,
    mk_invoice,
    mk_payment,
    mk_task_line_group,
):
    lines_data = [
        (4166670, 1),
        (4166670, 1),
        (4166670, 1),
        (4166670, 1),
        (4166670, 1),
        (4166670, 1),
        (4166670, 1),
        (1458330, -1),
    ]
    inv = mk_invoice(year=2019)
    group = mk_task_line_group()
    inv.lines = [
        mk_task_line(
            unity="h", cost=cost, quantity=quantity, date=date_20190101, group=group
        )
        for cost, quantity in lines_data
    ]
    inv.line_groups = [group]
    inv.payments = [mk_payment(amount=33250000, date=date_20190101, exported=1)]

    inv = dbsession.merge(inv)
    dbsession.flush()
    return inv


def test_negative_tasklines_sums_count_bug_3205(invoice_bug_3205):
    # Just check that it does not AssertionError because of negative delta
    lines = list(
        SAPAttestationLineService()._invoice_to_sap_lines(invoice_bug_3205, 2019)
    )
    # We count the negative lines « naively » so hours could be removed by
    # negative tasklines
    agregate = sum(lines)
    assert agregate.amount == 33250000  # the negative taskline dicreased amount
    assert agregate.quantity == 7  # the negative taskline did not remove hours
