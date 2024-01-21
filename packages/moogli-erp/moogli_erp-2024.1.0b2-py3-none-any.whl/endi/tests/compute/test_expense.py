import pytest

from unittest.mock import MagicMock
from endi.compute.expense import (
    ExpenseCompute,
    ExpenseLineCompute,
    ExpenseKmLineCompute,
)
from endi.compute.sage.expense import SageExpenseMain


@pytest.fixture
def simple_type():
    return MagicMock(type="expense")


@pytest.fixture
def teltype():
    return MagicMock(percentage=50.415, type="expensetel")


@pytest.fixture
def kmtype():
    return MagicMock(amount=0.38888, label="", code="")


class DummyAmount:
    def __init__(self, amount):
        self.amount = amount

    def get_amount(self):
        return self.amount


def test_expense_compute():
    sheet = ExpenseCompute()
    sheet.lines = (MagicMock(total=10), MagicMock(total=20))
    sheet.kmlines = (MagicMock(total=10), MagicMock(total=60))
    assert sheet.total == 100
    sheet.payments = (
        DummyAmount(amount=15),
        DummyAmount(amount=15),
    )
    assert sheet.topay() == 70
    assert sheet.paid() == 30


def test_expense_line_compute(teltype):
    compute = ExpenseLineCompute()
    compute.expense_type = teltype
    assert compute._compute_value(99.53) == 50


def test_expense_kmline_compute(kmtype):
    compute = ExpenseKmLineCompute()
    compute.expense_type = kmtype
    compute.km = 100
    compute.ht = 100 * kmtype.amount
    assert compute.total == 39


def test_expense_line(simple_type):
    compute = ExpenseLineCompute()
    compute.expense_type = simple_type
    assert compute._compute_value(99.53) == 100


def test_real_world_error(mk_expense_type):
    # test based on a real world problem that raised the error
    kmtype = mk_expense_type(amount=0.38)
    kmlines = []
    for km in [
        3000,
        2800,
        280,
        200,
        540,
        2800,
        3600,
        3000,
        3000,
        4400,
        2000,
        3000,
        4600,
    ]:
        compute = ExpenseKmLineCompute()
        compute.km = km
        compute.expense_type = kmtype
        compute.ht = km * kmtype.amount
        kmlines.append(compute)

    teltype = mk_expense_type(percentage=50)
    telline = ExpenseLineCompute()
    telline.ht = 2666
    telline.tva = 533
    telline.expense_type = teltype

    km_lines_total = sum(l.total for l in kmlines)
    km_lines_rounded_total = int(sum(l.total_ht for l in kmlines))
    km_lines_linerounded_total = sum(int(l.total_ht) for l in kmlines)

    telline_total = telline.total
    telline_rounded_total = int(telline.total_tva) + int(telline.total_ht)

    last_rounded_total = int(km_lines_total + telline_total)
    byproduct_rounded_total = km_lines_rounded_total + telline_rounded_total
    byline_rounded_total = km_lines_linerounded_total + telline_rounded_total

    # Option 1
    assert last_rounded_total == byline_rounded_total
    # Option 2
    assert last_rounded_total == byproduct_rounded_total


def test_expense_label_with_non_ascii_date(pyramid_request):
    pyramid_request.config = {
        "bookentry_expense_label_template": "{expense_date:%B}",
    }

    expense_main = SageExpenseMain(context=None, request=pyramid_request)
    expense_main.set_expense(MagicMock(year=2018, month=12))

    assert expense_main.libelle == "décembre"


def test_expense_label_supplier(pyramid_request, supplier):
    pyramid_request.config = {
        "bookentry_expense_label_template": "{supplier_label} / {expense_description} / {invoice_number}",
    }

    expense_main = SageExpenseMain(context=None, request=pyramid_request)
    expense_main.set_expense(MagicMock())

    assert expense_main.libelle == " /  / "

    empty_line = MagicMock(supplier=None, description="", invoice_number="")
    assert expense_main.get_line_libelle(empty_line) == " /  / "

    full_line = MagicMock(
        supplier=supplier,
        description="Fu",
        invoice_number="1234",
    )
    assert expense_main.get_line_libelle(full_line) == "Fournisseur Test / Fu / 1234"
