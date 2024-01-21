import pytest

from endi.compute import math_utils
from endi.models.task import (
    TaskLine,
    TaskLineGroup,
)


def compute_payment_ttc(payment):
    total = 0
    for tva, ht in list(payment.items()):
        line = TaskLine(tva=tva, cost=ht)
        total += line.total()
    return total


class TestInvoiceCompute:
    def getOne(self, invoice_ht_mode, payments):
        invoice = invoice_ht_mode
        invoice.payments = payments
        lines = [TaskLine(cost=6000000, quantity=1, tva=0, mode="ht")]
        invoice.line_groups = [TaskLineGroup(lines=lines)]
        return invoice

    def test_paid(self, invoice_ht_mode, payment_one, payment_two):
        invoice = self.getOne(invoice_ht_mode, [payment_one, payment_two])
        assert invoice.paid() == 2500000

    def test_topay(self, invoice_ht_mode, payment_one, payment_two):
        invoice = self.getOne(invoice_ht_mode, [payment_one, payment_two])
        assert invoice.topay() == 3500000

    def test_topay_with_cancelinvoice(
        self,
        cancelinvoice_1,
        cancelinvoice_2,
        invoice_ht_mode,
        payment_one,
        payment_two,
    ):
        invoice = self.getOne(invoice_ht_mode, [payment_one, payment_two])
        cinv1 = cancelinvoice_1
        lines = [TaskLine(cost=-500000, quantity=1, tva=0)]
        cinv1.line_groups = [TaskLineGroup(lines=lines)]
        cinv2 = cancelinvoice_2
        lines = [TaskLine(cost=-600000, quantity=1, tva=0)]
        cinv2.line_groups = [TaskLineGroup(lines=lines)]
        invoice.cancelinvoices = [cinv1, cinv2]
        assert invoice.cancelinvoice_amount() == 1100000
        assert invoice.topay() == 2400000

    def test_topay_with_epsilon(self, invoice_ht_mode, mk_payment):
        # total - 0.1centimes
        paid = 6000000 - 100
        payment = mk_payment(amount=paid, task_id=invoice_ht_mode.id)
        invoice = self.getOne(invoice_ht_mode, [payment])
        assert invoice.topay() == 0

    def test__get_payment_excess(self, mk_invoice):
        # Ref https://framagit.org/endi/endi/-/issues/2170
        invoice = mk_invoice()

        with pytest.raises(Exception):
            invoice._get_payment_excess(120510000.0, 120000000.0)
        with pytest.raises(Exception):
            invoice._get_payment_excess(-120510000.0, -120000000.0)

    def test__is_last_payment(self, mk_invoice):
        invoice = mk_invoice()
        computer = invoice._get_invoice_computer()
        assert computer._is_last_payment(120500000, 120000000)
        assert computer._is_last_payment(120000000, 120000000)
        assert not computer._is_last_payment(119000000, 120000000)
        assert computer._is_last_payment(-120500000, -120000000)
        assert computer._is_last_payment(-120000000, -120000000)
        assert not computer._is_last_payment(-119000000, -120000000)

    def test__get_single_tva_payment(self, mk_invoice, tva20):
        invoice = mk_invoice()
        computer = invoice._get_invoice_computer()

        assert computer._get_single_tva_payment(
            11111111, {"2000": 11111111}.items()
        ) == [{"tva_id": tva20.id, "amount": 11111000}]

    def test__get_payments_by_tva(self, mk_invoice, tva20, tva55):
        invoice = mk_invoice()
        computer = invoice._get_invoice_computer()

        # 10 %
        payments = computer._get_payments_by_tva(
            10949240.0, 109492400, 0, {2000: 3992400.0, 550: 105500000.0}.items()
        )
        assert sum([p["amount"] for p in payments]) == 10949000.0

    def test_compute_payments_single_tva(
        self, dbsession, mk_invoice, mk_task_line, mk_task_line_group, tva20
    ):
        # Ref https://framagit.org/endi/endi/-/issues/2170
        invoice = mk_invoice()
        group = mk_task_line_group()
        mk_task_line(cost=100000000, tva=2000, group=group),
        mk_task_line(cost=3327000, tva=2000, group=group),
        invoice.line_groups = [group]
        dbsession.merge(invoice)
        dbsession.flush()
        payments = invoice.compute_payments(123992000)
        assert payments == [{"tva_id": tva20.id, "amount": 123992000}]

        payments = invoice.compute_payments(123992400)
        assert payments == [{"tva_id": tva20.id, "amount": 123992000}]

        with pytest.raises(Exception):
            payments = invoice.compute_payments(124692400)

    def test_compute_payments_multi_tva(self, invoice_multitva_payments, mk_payment):
        invoice = invoice_multitva_payments
        assert invoice.topay() == 87405000

        assert len(invoice.topay_by_tvas()) == 3
        assert list(invoice.topay_by_tvas().values())[0] == 5760000
        payments = invoice.compute_payments(10520000)
        assert len(payments) == 3

        assert payments[0]["amount"] == 693000
        assert payments[1]["amount"] == 5197000
        assert payments[2]["amount"] == 4630000

        for p in payments:
            invoice.payments.append(
                mk_payment(mode="Chèque", amount=p["amount"], tva_id=p["tva_id"]),
            )

        # After the 3 payments are recorded
        assert invoice.topay() == 76885000  # 87405000 - 10520000
        assert len(invoice.topay_by_tvas()) == 3

    def test_compute_payments_2491(
        self, mk_invoice, mk_task_line, mk_task_line_group, tva20, tva55
    ):
        invoice = mk_invoice()
        group = mk_task_line_group()
        mk_task_line(cost=100000000, tva=550, group=group),
        mk_task_line(cost=3327000, tva=2000, group=group),
        invoice.line_groups = [group]
        payments = invoice.compute_payments(109492000)
        assert sum([p["amount"] for p in payments]) == 109492000

    def test_compute_payments_negative_single_tva(
        self, dbsession, mk_invoice, mk_task_line, mk_task_line_group, tva20
    ):
        # Ref https://framagit.org/endi/endi/-/issues/2170
        invoice = mk_invoice()
        group = mk_task_line_group()
        mk_task_line(cost=-100000000, tva=2000, group=group),
        mk_task_line(cost=-3327000, tva=2000, group=group),
        invoice.line_groups = [group]
        dbsession.merge(invoice)
        dbsession.flush()
        payments = invoice.compute_payments(-123992000)
        assert payments == [{"tva_id": tva20.id, "amount": -123992000}]

        payments = invoice.compute_payments(-123992400)
        assert payments == [{"tva_id": tva20.id, "amount": -123992000}]

    def test_compute_payments_negative_multi_tva(
        self, dbsession, mk_invoice, mk_task_line, mk_task_line_group, tva20, tva55
    ):
        # Ref https://framagit.org/endi/endi/-/issues/2170
        invoice = mk_invoice()
        group = mk_task_line_group()
        mk_task_line(cost=-100000000, tva=550, group=group),
        mk_task_line(cost=-3327000, tva=2000, group=group),
        invoice.line_groups = [group]
        dbsession.merge(invoice)
        dbsession.flush()
        payments = invoice.compute_payments(-109492000)
        assert sum([p["amount"] for p in payments]) == -109492000
        payments = invoice.compute_payments(-109492400)
        assert sum([p["amount"] for p in payments]) == -109492000


class TestEstimationCompute:
    @pytest.fixture
    def current_estimation(
        self,
        dbsession,
        empty_ht_estimation,
        payment_line_1,
        payment_line_2,
        payment_line_3,
    ):
        estimation = empty_ht_estimation
        estimation.expenses_ht = 20000
        estimation.deposit = 20
        estimation.manualDeliverables = 0
        lines = [
            TaskLine(cost=5000000, quantity=1, tva=1960, mode="ht"),
            TaskLine(cost=5000000, quantity=1, tva=1960, mode="ht"),
            TaskLine(cost=1000000, quantity=1, tva=500, mode="ht"),
        ]
        estimation.line_groups = [TaskLineGroup(lines=lines)]
        estimation.discounts = []
        estimation.payment_lines = [payment_line_1, payment_line_2, payment_line_3]
        dbsession.merge(estimation)
        return estimation

    @pytest.fixture
    def current_estimation_ttc(
        self,
        dbsession,
        empty_ht_estimation,
        mk_payment_line,
    ):
        estimation = empty_ht_estimation
        estimation.mode = "ttc"
        estimation.deposit = 20
        estimation.manualDeliverables = 0
        lines = [
            TaskLine(cost=10000000, quantity=1, tva=2000, mode="ttc"),
        ]
        estimation.line_groups = [TaskLineGroup(lines=lines)]
        estimation.discounts = []
        estimation.payment_lines = [
            mk_payment_line(),
            mk_payment_line(),
            mk_payment_line(),
        ]
        dbsession.merge(estimation)
        return estimation

    def test_add_ht_by_tva(self, current_estimation):
        lines = [
            TaskLine(cost=5000000, quantity=1, tva=1960, mode="ht"),
            TaskLine(cost=1000000, quantity=1, tva=500, mode="ht"),
        ]

        dico = {}
        current_estimation.add_ht_by_tva(dico, lines)
        assert list(dico.keys()) == [1960, 500]

    # Deposit
    def test_deposit_amounts(self, current_estimation):
        amounts = current_estimation.deposit_amounts_native()
        assert list(amounts.keys()) == [1960, 500, 2000]
        assert amounts[1960] == 2000000
        assert amounts[500] == 200000
        # expenses_ht
        assert amounts[2000] == 4000

    def test_deposit_amount_ttc(self, current_estimation):
        # 2392000 = 2000000 * 119.6 / 100 + 200000 * 105/100 + 4000 * 1.2
        # arrondi à 0.01 (donc 1000)
        assert current_estimation.deposit_amount_ttc() == 2607000

    # Payment lines (with equal repartition)
    def test_get_nb_payment_lines(self, current_estimation):
        assert current_estimation.get_nb_payment_lines() == 3

    def test_paymentline_amounts(self, current_estimation):
        amounts = current_estimation.paymentline_amounts_native()
        assert list(amounts.keys()) == [1960, 500, 2000]
        assert int(amounts[1960]) == 2666666
        assert int(amounts[500]) == 266666

    def test_paymentline_amount_ttc(self, current_estimation):
        # 3475.712 = 2672 * 119.6/100 + 266 * 105/100.0
        assert current_estimation.paymentline_amount_ttc() == 3475000

    # Ref #3667 : https://framagit.org/endi/endi/-/issues/3667
    def test_paymentline_amount_ttc_ttc_mode(self, current_estimation_ttc):
        # acompte : 2000000
        # Reste : 8000000
        assert current_estimation_ttc.paymentline_amount_ttc() == 2667000

        deposit = current_estimation_ttc.deposit_amount_ttc()
        amount = 2 * current_estimation_ttc.paymentline_amount_ttc()
        sold = current_estimation_ttc.sold()
        assert deposit + amount + sold == current_estimation_ttc.total()

    def test_sold(self, current_estimation):
        sold = current_estimation.sold()
        deposit = current_estimation.deposit_amount_ttc()
        paymentline = current_estimation.paymentline_amount_ttc()
        nblines = current_estimation.get_nb_payment_lines() - 1
        assert sold + deposit + paymentline * nblines == current_estimation.total()

    # Payment lines (with non manual repartition)
    def test_manual_payment_line_amounts(self, current_estimation):
        current_estimation.manualDeliverables = 1
        payments = current_estimation.manual_payment_line_amounts()
        assert list(payments[0].keys()) == [1960]
        assert list(payments[1].keys()) == [1960, 500]
        assert list(payments[2].keys()) == [500, 2000]
        deposit = current_estimation.deposit_amount_ttc()
        amount1 = compute_payment_ttc(payments[0])
        amount2 = compute_payment_ttc(payments[1])
        assert math_utils.floor(amount1) == 4000000
        assert math_utils.floor(amount2) == 6000000
        total = current_estimation.sold() + deposit + amount1 + amount2
        assert math_utils.floor_to_precision(total) == current_estimation.total()

    @pytest.fixture
    def estimation_3677(
        self,
        dbsession,
        empty_ht_estimation,
        mk_payment_line,
        mk_task_line,
        mk_task_line_group,
        tva10,
    ):
        lines = [
            mk_task_line(cost=103313000, tva=tva10.value, mode="ht"),
            mk_task_line(cost=177008000, quantity=2.38, tva=tva10.value, mode="ht"),
            mk_task_line(cost=7963000, quantity=122.31, tva=tva10.value, mode="ht"),
        ]
        empty_ht_estimation.line_groups = [mk_task_line_group(lines=lines)]
        empty_ht_estimation.payment_lines = [
            mk_payment_line(amount=824201000),
            mk_payment_line(amount=0),
        ]
        empty_ht_estimation.deposit = 50
        empty_ht_estimation.manualDeliverables = 1
        dbsession.merge(empty_ht_estimation)
        dbsession.flush()
        return empty_ht_estimation

    def test_manual_payment_line_amounts_bug_3677(self, estimation_3677):
        deposit = estimation_3677.deposit_amount_ttc()
        payments = estimation_3677.manual_payment_line_amounts()
        total = compute_payment_ttc(payments[0]) + deposit
        assert math_utils.floor_to_precision(total) == estimation_3677.total()
