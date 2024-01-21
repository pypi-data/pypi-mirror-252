import pytest
import datetime

from endi.models.task import TaskLine, TaskLineGroup, DiscountLine

from endi.compute import math_utils


TASK = {"project": 12, "expenses": 1500000, "expenses_ht": 1000000}
LINES = [
    [
        {"cost": 10025000, "tva": 1960, "quantity": 1.25, "mode": "ht"},
        {"cost": 7500000, "tva": 1960, "quantity": 3, "mode": "ht"},
        {"cost": -5200000, "tva": 1960, "quantity": 1, "mode": "ht"},
    ],
    [
        {"cost": 10025000, "tva": 1960, "quantity": 1.25, "mode": "ht"},
        {"cost": 7500000, "tva": 1960, "quantity": 3, "mode": "ht"},
        {"cost": -5200000, "tva": 1960, "quantity": 1, "mode": "ht"},
    ],
]
DISCOUNTS = [{"amount": 2000000, "tva": 1960}]
POST_TTC_LINES = [{"amount": -5000000}]

# Values:
#         the money values are represented *100000
#
# Rounding rules:
#         TVA, total_ttc and deposit are rounded (total_ht is not)

# Lines total should be integers (here they are
# *100000) so it fits the limit case
#
# Line totals should be integers (here they are *100000)
TASK_LINES_TOTAL_HT = (
    12531250.0,
    22500000,
    -5200000,
)  # 2, 3 )
TASK_LINES_TVAS = (
    2456125,
    4410000,
    -1019200,
)  # 0.392, 0.588)

LINES_TOTAL_HT = sum(TASK_LINES_TOTAL_HT) * 2
LINES_TOTAL_TVAS = sum(TASK_LINES_TVAS) * 2
EXPENSE_TVA = 196000

DISCOUNT_TOTAL_HT = sum([d["amount"] for d in DISCOUNTS])
DISCOUNT_TVAS = (392000,)
DISCOUNT_TOTAL_TVAS = sum(DISCOUNT_TVAS)

# Totals should be multiple of 1000 (ending to be floats with 2 numbers after
# the comma
HT_TOTAL = math_utils.floor_to_precision(
    LINES_TOTAL_HT - DISCOUNT_TOTAL_HT + TASK["expenses_ht"]
)
TVA = math_utils.floor_to_precision(
    LINES_TOTAL_TVAS - DISCOUNT_TOTAL_TVAS + EXPENSE_TVA
)

# TASK_TOTAL = lines + tva + expenses rounded
TASK_TOTAL = HT_TOTAL + TVA + TASK["expenses"]

POST_TTC_TOTAL = sum([p["amount"] for p in POST_TTC_LINES])
TASK_TOTAL_DUE = TASK_TOTAL + POST_TTC_TOTAL


def get_lines(datas):
    lines = []
    for line in datas:
        lines.append(TaskLine(**line))
    return lines


@pytest.fixture
def group_task_cents(mk_task, mk_task_line_group, mk_task_line):
    """
    Reference rich task with well-known line/groups
    """
    t = mk_task(mode="ht")
    t.line_groups.pop()
    g = mk_task_line_group(task=t)
    mk_task_line(group=g, cost=1, quantity=0.1, mode="ht")
    return t


@pytest.fixture
def task(mk_task, mk_task_line_group, mk_task_line, mk_discount_line, mk_post_ttc_line):
    """
    Reference rich task with well-known line/groups
    """
    t = mk_task(mode="ht")
    t.line_groups.pop()
    for group in LINES:
        g = mk_task_line_group(task=t)
        for line in group:
            mk_task_line(group=g, **line)
    for line in DISCOUNTS:
        mk_discount_line(task=t, **line)
    for line in POST_TTC_LINES:
        mk_post_ttc_line(task=t, **line)
    t.expenses_tva = 1960
    t.expenses = TASK["expenses"]
    t.expenses_ht = TASK["expenses_ht"]
    return t


@pytest.fixture
def invoice_bug363(
    def_tva, tva10, empty_task, customer, company, mk_product, mk_task_line_group
):
    prod = mk_product(tva=tva10, name="product 2", compte_cg="P0002")
    lines = []

    for cost, qtity in (
        (15000000, 1),
        (2000000, 86),
        (-173010000, 1),
        (10000000, 1),
        (-201845000, 1),
        (4500000, 33),
        (1800000, 74),
        (3500000, 28),
    ):
        lines.append(
            TaskLine(
                cost=cost, quantity=qtity, tva=tva10.value, product=prod, mode="ht"
            )
        )

    invoice = empty_task
    invoice.default_tva = def_tva.value
    invoice.expenses_tva = def_tva.value
    invoice.date = datetime.date(2016, 5, 4)
    invoice.customer = customer
    invoice.company = company
    invoice.official_number = "INV_002"
    mk_task_line_group(task=invoice, lines=lines)
    invoice.expenses_ht = 0
    invoice.expenses = 0
    return invoice


@pytest.fixture
def task_line_negative_tva(mk_task_line):
    return mk_task_line(tva=-1000, cost=1000, description="Test line bug2317")


class TestTaskCompute:
    def test_lines_total_ht(self, task):
        assert task.groups_total_ht() == LINES_TOTAL_HT

    def test_discounts_total_ht(self, task):
        assert task.discount_total_ht() == DISCOUNT_TOTAL_HT

    def test_total_ht(self, task):
        assert task.total_ht() == HT_TOTAL

    def test_get_tvas(self, task):
        tvas = task.get_tvas()
        assert tvas[1960] == TVA

    def test_get_tvas_multiple(self, empty_task):
        task = empty_task
        lines = [
            TaskLine(cost=35000000, quantity=1, tva=1960, mode="ht"),
            TaskLine(cost=40000000, quantity=1, tva=550, mode="ht"),
        ]
        task.line_groups = [TaskLineGroup(lines=lines)]

        task.discounts = [
            DiscountLine(
                amount=1200000,
                tva=550,
            ),
            DiscountLine(
                amount=15000000,
                tva=1960,
            ),
        ]
        tvas = task.get_tvas()
        assert list(tvas.keys()) == [1960, 550]
        assert tvas[1960] == 3920000
        assert tvas[550] == 2134000

    def test_get_tvas_multiple_rounding(self, empty_task):
        task = empty_task
        lines = [
            TaskLine(cost=10004000, quantity=1, tva=1000, mode="ht"),
            TaskLine(cost=5002000, quantity=1, tva=2000, mode="ht"),
        ]
        task.line_groups = [TaskLineGroup(lines=lines)]
        # Ref https://framagit.org/endi/endi/issues/305
        tvas = task.get_tvas()
        assert tvas[1000] == 1000000
        assert task.tva_amount() == 2000000

    def test_tva_amount(self, task):
        # cf #501
        line = TaskLine(cost=5010000, quantity=1, tva=1960, mode="ht")
        assert line.tva_amount() == 981960
        assert task.tva_amount() == TVA

    def test_total_ttc(self, empty_task):
        task = empty_task
        lines = [TaskLine(cost=1030000, quantity=1.25, tva=1960, mode="ht")]
        task.line_groups = [TaskLineGroup(lines=lines)]
        # cf ticket #501
        # line total : 12.875
        # tva : 2.5235 -> 2.52
        # => total : 15.40 (au lieu de 15.395)
        assert task.total_ttc() == 1540000

    def test_total(self, task):
        assert task.total() == TASK_TOTAL

    def test_post_ttc_total(self, task):
        assert task.post_ttc_total() == POST_TTC_TOTAL

    def test_total_due(self, task):
        assert task.total_due() == TASK_TOTAL_DUE

    def test_no_tva(self, empty_task):
        task = empty_task
        line = TaskLine(cost=3500000, tva=-100)
        task.line_groups = [TaskLineGroup(lines=[line])]
        assert task.no_tva()

        line = TaskLine(cost=3500000, tva=0)
        task.line_groups = [TaskLineGroup(lines=[line])]
        assert not task.no_tva()

        line = TaskLine(cost=3500000, tva=100)
        task.line_groups = [TaskLineGroup(lines=[line])]
        assert not task.no_tva()

    def test_get_tvas_by_product(self, invoice_bug363):
        assert (
            invoice_bug363.get_tvas_by_product()[
                (
                    "P0002",
                    "TVA10",
                )
            ]
            == 20185000
        )

    def test_get_tva_ht_parts(self, empty_task):
        task = empty_task
        task.expenses_tva = 2000
        lines = [
            TaskLine(cost=-120000000, quantity=1, tva=2000, mode="ht"),
            TaskLine(cost=-120000000, quantity=0.5, tva=2000, mode="ht"),
        ]
        task.line_groups = [TaskLineGroup(lines=lines)]
        task.expenses_ht = -36000000
        assert task.tva_ht_parts()[2000] == -216000000.0

    def test_get_tva_ttc_parts(
        self, mk_invoice, mk_task_line, mk_task_line_group, tva20, tva55
    ):
        invoice = mk_invoice()
        group = mk_task_line_group()
        mk_task_line(cost=100000000, tva=550, group=group),
        mk_task_line(cost=3327000, tva=2000, group=group),
        invoice.line_groups = [group]
        parts = invoice.tva_ttc_parts()
        assert parts[550] == 105500000
        assert parts[2000] == 3992000


class TestLineCompute:
    def test_line_compute(self, task):
        for index, line_obj in enumerate(get_lines(LINES[0])):
            assert line_obj.total_ht() == TASK_LINES_TOTAL_HT[index]
            assert (
                line_obj.total() == TASK_LINES_TOTAL_HT[index] + TASK_LINES_TVAS[index]
            )

    def test_discount_compute(self, task):
        for index, line_obj in enumerate(task.discounts):
            assert line_obj.total_ht() == DISCOUNTS[index]["amount"]
            assert line_obj.total() == DISCOUNTS[index]["amount"] + DISCOUNT_TVAS[index]

    def test_negative_tva(self, task_line_negative_tva):
        assert task_line_negative_tva.tva_amount() == 0


class TestGroupCompute:
    def test_cents(self, group_task_cents):
        assert group_task_cents.line_groups[0].total_ht() == 0.1
