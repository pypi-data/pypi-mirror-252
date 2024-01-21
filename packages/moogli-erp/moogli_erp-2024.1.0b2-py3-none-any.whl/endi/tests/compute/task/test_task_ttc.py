from itertools import product
import pytest
import datetime

from endi.compute.task import (
    TaskTtcCompute,
)
from endi.models.task import TaskLine, TaskLineGroup, DiscountLine

from endi.compute import math_utils

LINES = [
    [
        {"cost": 10025000, "tva": 1960, "quantity": 2, "mode": "ttc"},
        {"cost": 7500000, "tva": 1960, "quantity": 3, "mode": "ttc"},
        {"cost": -5200000, "tva": 1960, "quantity": 1, "mode": "ttc"},
    ],
    [
        {"cost": 10025000, "tva": 1960, "quantity": 2, "mode": "ttc"},
        {"cost": 7500000, "tva": 1960, "quantity": 3, "mode": "ttc"},
        {"cost": -5200000, "tva": 1960, "quantity": 1, "mode": "ttc"},
    ],
]
DISCOUNTS = [
    {"amount": 2000000, "tva": 1960},
]
# float(total_ttc) / ((max(int(tva), 0) / 10000.0) + 1)
DISCOUNTS_HT = (1672240.0,)
POST_TTC_LINES = [{"amount": -5000000}]

# Values:
#         the money values are represented *100000
#
# Rounding rules:
#         TVA, total_ht and deposit are rounded (total_ttc is not)

# Lines total should be integers (here they are
# *100000) so it fits the limit case
#
# Line totals should be integers (here they are *100000)

TASK_LINES_UNIT_HT = [8382107.0, 6270903.0, -4347826.0]
TASK_LINES_TOTAL_HT = [16764206.0, 18812700.0, -4347824.0]
TASK_LINES_TOTAL_TTC = (20050000, 22500000, -5200000)
TASK_LINES_TOTAL_TVA = [3285794.0, 3687300.0, -852176.0]

LINES_TOTAL_TTC = sum(TASK_LINES_TOTAL_TTC) * 2
# HT = TTC / (1+ TVA) -> float(total_ttc) / ((max(int(tva), 0) / 10000.0) + 1)
LINES_TOTAL_HT = sum(TASK_LINES_TOTAL_HT) * 2
LINES_TOTAL_TVAS = sum(TASK_LINES_TOTAL_TVA) * 2

DISCOUNT_TOTAL_TTC = sum([d["amount"] for d in DISCOUNTS])
DISCOUNT_TOTAL_HT = sum(DISCOUNTS_HT)

# HT = TTC / (1+ TVA) -> float(total_ttc) / ((max(int(tva), 0) / 10000.0) + 1)
DISCOUNT_TVAS = (327760,)
DISCOUNT_TOTAL_TVAS = sum(DISCOUNT_TVAS)

HT_TOTAL = math_utils.floor_to_precision(LINES_TOTAL_HT - DISCOUNT_TOTAL_HT)
TVA = math_utils.floor_to_precision(LINES_TOTAL_TVAS - DISCOUNT_TOTAL_TVAS)

TTC_TOTAL = HT_TOTAL + TVA

TASK_TOTAL = TTC_TOTAL

POST_TTC_TOTAL = sum([p["amount"] for p in POST_TTC_LINES])
TASK_TOTAL_DUE = TASK_TOTAL + POST_TTC_TOTAL


@pytest.fixture
def task(mk_task, mk_task_line_group, mk_task_line, mk_discount_line, mk_post_ttc_line):
    """
    Reference rich task with well-known line/groups
    """
    t = mk_task(mode="ttc")
    t.line_groups.pop()
    for group in LINES:
        g = mk_task_line_group(task=t)
        for line in group:
            mk_task_line(group=g, **line)
    for line in DISCOUNTS:
        mk_discount_line(task=t, **line)
    for line in POST_TTC_LINES:
        mk_post_ttc_line(task=t, **line)
    return t


@pytest.fixture
def invoice_bug363(def_tva, tva10, empty_task_ttc, customer, company, mk_product):
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
                cost=cost,
                quantity=qtity,
                tva=tva10.value,
                product=prod,
                mode="ttc",
            )
        )

    invoice = empty_task_ttc
    invoice.default_tva = def_tva.value
    invoice.expenses_tva = def_tva.value
    invoice.date = datetime.date(2016, 0o5, 0o4)
    invoice.company = company
    invoice.official_number = "INV_002"
    invoice.line_groups = [TaskLineGroup(lines=lines)]
    return invoice


@pytest.fixture
def invoice_bug3682(
    dbsession,
    invoice,
    mk_task_line,
    mk_task_line_group,
    mk_discount_line,
    tva10,
    mk_product,
):
    prod = mk_product(tva=tva10, compte_cg="P0002")
    lines = [mk_task_line(cost=10000000, tva=1000, product=prod)]
    group = mk_task_line_group()
    group.lines = lines
    invoice.line_groups = [group]
    invoice.discounts = [mk_discount_line(amount=1000000, tva=1000)]
    dbsession.merge(invoice)
    dbsession.flush()
    return invoice


@pytest.fixture
def invoice_bug3420(
    dbsession,
    invoice,
    mk_task_line,
    mk_task_line_group,
    tva20,
    mk_product,
):
    invoice.mode = "ttc"
    prod = mk_product(tva=tva20, compte_cg="P0002")
    group = mk_task_line_group()
    for cost, quantity in (
        (1200000, 1),
        (1250000, 1),
        (250000, 1),
        (6000000, 2),
    ):
        group.lines.append(
            mk_task_line(
                cost=cost, quantity=quantity, tva=2000, product=prod, mode="ttc"
            )
        )

    invoice.line_groups = [group]
    dbsession.merge(invoice)
    dbsession.flush()
    return invoice


@pytest.fixture
def estimation_bug3658(dbsession, estimation, tva55, mk_task_line, mk_task_line_group):
    estimation.mode = "ttc"
    lines = []
    for cost, quantity in (
        (210000, 3.0),
        (105000, 9.0),
        (123000, 3.0),
        (500000, 12.0),
        (200000, 8.76),
        (315000, 1.475),
        (245000, 10.0),
        (245000, 12.0),
        (90000, 11.0),
        (315000, 2.0),
    ):
        lines.append(
            mk_task_line(tva=tva55.value, cost=cost, quantity=quantity, mode="ttc")
        )
    group = mk_task_line_group()
    group.lines = lines
    estimation.line_groups = [group]
    dbsession.merge(estimation)
    return estimation


@pytest.fixture
def task_line_negative_tva(mk_task_line):
    return mk_task_line(
        tva=-1000, cost=1000, mode="ttc", description="Test line bug2317"
    )


class TestTaskCompute:
    def test_total_ttc(self, task):
        assert task.total_ttc() == TTC_TOTAL

    def test_lines_total_ht(self, task):
        assert task.groups_total_ht() == LINES_TOTAL_HT

    def test_discounts_total_ht(self, task):
        assert task.discount_total_ht() == DISCOUNT_TOTAL_HT

    def test_total_ht(self, task):
        assert task.total_ht() == HT_TOTAL

    def test_get_tvas(self, task):
        tvas = task.get_tvas()
        assert tvas[1960] == TVA

    def test_get_tvas_multiple(self, empty_task_ttc):
        task = empty_task_ttc
        lines = [
            TaskLine(cost=35000000, quantity=1, tva=1960, mode="ttc"),
            TaskLine(cost=40000000, quantity=1, tva=550, mode="ttc"),
        ]
        task.line_groups = [TaskLineGroup(lines=lines)]
        task.discounts = [
            DiscountLine(amount=1200000, tva=550),
            DiscountLine(amount=15000000, tva=1960),
        ]
        tvas = task.get_tvas()
        assert list(tvas.keys()) == [1960, 550]
        assert tvas[1960] == 3278000
        assert tvas[550] == 2023000

    def test_tva_amount(self, task, empty_task_ttc):
        line = TaskLine(cost=5010000, quantity=1, tva=1960, mode="ttc")
        assert math_utils.floor_to_precision(line.tva_amount(), precision=5) == 821039
        # 821038.8000000003
        assert task.tva_amount() == TVA

    def test_total_ttc_bis(self, empty_task_ttc):
        task = empty_task_ttc
        lines = [TaskLine(cost=1030000, quantity=1.25, tva=1960, mode="ttc")]
        task.line_groups = [TaskLineGroup(lines=lines)]
        assert task.total_ttc() == 1287500.0

    def test_total_ttc(self, invoice_bug3420):
        assert invoice_bug3420.total_ttc() == 14700000

    def test_total(self, task):
        assert task.total() == TASK_TOTAL

    def test_post_ttc_total(self, task):
        assert task.post_ttc_total() == POST_TTC_TOTAL

    def test_total_due(self, task):
        assert task.total_due() == TASK_TOTAL_DUE

    def test_no_tva(self, empty_task_ttc):
        task = empty_task_ttc
        line = TaskLine(cost=3500000, tva=-100, mode="ttc")
        task.line_groups = [TaskLineGroup(lines=[line])]
        assert task.no_tva()

        line = TaskLine(cost=3500000, tva=0, mode="ttc")
        task.line_groups = [TaskLineGroup(lines=[line])]
        assert not task.no_tva()

        line = TaskLine(cost=3500000, tva=100, mode="ttc")
        task.line_groups = [TaskLineGroup(lines=[line])]
        assert not task.no_tva()

    def test_get_tvas_by_product(self, invoice_bug363, invoice_bug3682):
        assert TaskTtcCompute(invoice_bug363).tva_amount() == 18350000
        assert (
            TaskTtcCompute(invoice_bug363).get_tvas_by_product()[("P0002", "TVA10")]
            == 18350000
        )
        assert (
            TaskTtcCompute(invoice_bug3682).get_tvas_by_product()[("P0002", "TVA10")]
            == 1000000
        )

    def test_get_tva_ht_parts(self, empty_task_ttc):
        task = empty_task_ttc
        lines = [
            TaskLine(cost=-120000000, quantity=1, tva=2000, mode="ttc"),
            TaskLine(cost=-120000000, quantity=0.5, tva=2000, mode="ttc"),
        ]
        task.line_groups = [TaskLineGroup(lines=lines)]
        assert task.tva_ht_parts()[2000] == -150000000.0

    def test_negative_tva(self, task_line_negative_tva):
        assert task_line_negative_tva.tva_amount() == 0

    def test_tva(self, estimation_bug3658):
        assert (
            estimation_bug3658.total() - estimation_bug3658.total_ht()
            == estimation_bug3658.tva_amount()
        )


class TestGroupCompute:
    def test_group_compute(self, task):
        for group_obj in task.line_groups:
            assert group_obj.get_tvas() == {1960: sum(TASK_LINES_TOTAL_TVA)}
            assert group_obj.tva_amount() == sum(TASK_LINES_TOTAL_TVA)
            assert group_obj.total_ht() == sum(TASK_LINES_TOTAL_HT)
            assert group_obj.total_ttc() == sum(TASK_LINES_TOTAL_TTC)


class TestLineCompute:
    def test_line_compute(self, task):
        for index, line_obj in enumerate(task.line_groups[0].lines):
            assert line_obj.total_ht() == TASK_LINES_TOTAL_HT[index]
            assert line_obj.tva_amount() == TASK_LINES_TOTAL_TVA[index]
            assert line_obj.total() == TASK_LINES_TOTAL_TTC[index]

    def test_discount_compute(self, task):
        for index, line_obj in enumerate(task.discounts):
            assert line_obj.total_ht() == DISCOUNTS_HT[index]
            assert line_obj.tva_amount() == DISCOUNT_TVAS[index]
            assert line_obj.total() == DISCOUNTS[index]["amount"]

    def test_line_compute_bug_3865(self, mk_task_line):
        line_obj = mk_task_line(tva=2000, cost=600000000, mode="ttc")
        assert line_obj.total_ht() == 500000000
