import datetime
from endi.compute.math_utils import integer_to_amount
from endi.models.task.services import (
    EstimationInvoicingService,
    EstimationService,
)
import pytest


class TestEstimationInvoicingService:
    def test_get_common_invoice(
        self, get_csrf_request_with_db, estimation, user, mk_task_mention
    ):
        estimation.start_date = (datetime.date(2021, 2, 1),)
        estimation.first_visit = (datetime.date(2021, 1, 20),)
        estimation.end_date = ("Deux semaines après le début",)
        # #3809
        disabled_mention = mk_task_mention(active=False, label="Test", title="Titre")
        estimation.mentions.append(disabled_mention)
        common_invoice = EstimationInvoicingService._get_common_invoice(
            get_csrf_request_with_db(),
            estimation,
            user,
        )
        for key in (
            "company",
            "customer",
            "project",
            "business_type_id",
            "phase_id",
            "payment_conditions",
            "description",
            "address",
            "workplace",
            "start_date",
            "first_visit",
            "end_date",
            "insurance_id",
        ):
            assert getattr(common_invoice, key) == getattr(estimation, key)

        assert common_invoice.business_id is not None
        assert common_invoice.estimation == estimation
        assert common_invoice.status_user == user
        assert common_invoice.owner == user
        # Fix 3809
        for mention in estimation.mentions:
            if mention.active:
                assert mention in common_invoice.mentions
            else:
                assert mention not in common_invoice.mentions

    def test_get_common_invoice_ht_mode(
        self, get_csrf_request_with_db, estimation, user
    ):
        common_invoice = EstimationInvoicingService._get_common_invoice(
            get_csrf_request_with_db(),
            estimation,
            user,
        )
        assert common_invoice.mode == estimation.mode
        assert common_invoice.mode == "ht"

    def test_get_common_invoice_ttc_mode(
        self, get_csrf_request_with_db, estimation, user
    ):
        estimation.mode = "ttc"
        common_invoice = EstimationInvoicingService._get_common_invoice(
            get_csrf_request_with_db(),
            estimation,
            user,
        )
        assert common_invoice.mode == estimation.mode
        assert common_invoice.mode == "ttc"

    def test_get_task_line(self):
        task_line = EstimationInvoicingService._get_task_line(
            100000, "Description", tva=700
        )
        assert task_line.description == "Description"
        assert task_line.cost == 100000
        assert task_line.tva == 700

    def test_get_deposit_task_line(self):
        task_line = EstimationInvoicingService._get_deposit_task_line(100000, 700)
        assert task_line.description == "Facture d'acompte"
        assert task_line.cost == 100000
        assert task_line.tva == 700

    def test_get_deposit_task_lines(self, full_estimation, tva):
        task_lines = EstimationInvoicingService._get_deposit_task_lines(full_estimation)
        assert len(task_lines) == 2
        assert task_lines[0].cost + task_lines[1].cost == 2 * 1000000
        assert task_lines[0].tva == tva.value
        assert task_lines[1].tva == 700

    def test_gen_deposit_invoice(
        self, get_csrf_request_with_db, full_estimation, user, plugin_active
    ):
        deposit_invoice = EstimationInvoicingService.gen_deposit_invoice(
            get_csrf_request_with_db(),
            full_estimation,
            user,
        )
        assert (
            deposit_invoice.all_lines[0].cost + deposit_invoice.all_lines[1].cost
            == 0.1 * full_estimation.total_ht()
        )

        import datetime

        today = datetime.date.today()
        # Ref : https://framagit.org/endi/endi/issues/1812
        if not plugin_active("sap"):
            assert deposit_invoice.display_units == 0
        assert deposit_invoice.date == today
        assert deposit_invoice.ttc == 2270000  # 10% des 22700000

    def test_get_intermediate_invoiceable_amounts(self, full_estimation, tva):
        amounts = EstimationInvoicingService._get_intermediate_invoiceable_amounts(
            full_estimation
        )
        assert 700 in list(amounts[0].keys())
        assert tva.value in list(amounts[0].keys())

    def test_gen_intermediate_invoice(
        self,
        get_csrf_request_with_db,
        full_estimation,
        payment_line,
        plugin_active,
        user,
    ):
        invoice = EstimationInvoicingService.gen_intermediate_invoice(
            get_csrf_request_with_db(), full_estimation, payment_line, user
        )

        # Ref : https://framagit.org/endi/endi/issues/1812
        if not plugin_active("sap"):
            assert invoice.display_units == 0
        assert invoice.total_ttc() == payment_line.amount
        assert invoice.ttc == payment_line.amount

    def test__get_all_intermediate_invoiceable_task_lines(
        self, full_estimation, estimation
    ):
        lines = EstimationInvoicingService._get_all_intermediate_invoiceable_task_lines(
            full_estimation
        )
        assert len(lines) == 4  # 2 pour l'acompte + 2 pour le premier paiement

    def test_gen_sold_invoice(self, get_csrf_request_with_db, full_estimation, user):
        invoice = EstimationInvoicingService.gen_sold_invoice(
            get_csrf_request_with_db(), full_estimation, user
        )
        # Ref : https://framagit.org/endi/endi/issues/1812
        assert invoice.display_units == 1

        lines = invoice.all_lines
        for index in range(2):
            assert lines[index].cost == full_estimation.all_lines[index].cost
            assert lines[index].tva == full_estimation.all_lines[index].tva

        assert len(lines) == 6
        assert len(invoice.discounts) == 1
        assert invoice.ttc == 5430000  # 222700000 * 90 /100 - 15000000

    def test_all_invoices(
        self, get_csrf_request_with_db, full_estimation, payment_line, user
    ):
        deposit_invoice = EstimationInvoicingService.gen_deposit_invoice(
            get_csrf_request_with_db(), full_estimation, user
        )
        intermediate_invoice = EstimationInvoicingService.gen_intermediate_invoice(
            get_csrf_request_with_db(), full_estimation, payment_line, user
        )
        sold_invoice = EstimationInvoicingService.gen_sold_invoice(
            get_csrf_request_with_db(), full_estimation, user
        )
        assert (
            deposit_invoice.total_ht()
            + intermediate_invoice.total_ht()
            + sold_invoice.total_ht()
            == full_estimation.total_ht()
        )

    def test_all_invoices_ttc(
        self, get_csrf_request_with_db, full_estimation_ttc, payment_line, user
    ):
        deposit_invoice = EstimationInvoicingService.gen_deposit_invoice(
            get_csrf_request_with_db(), full_estimation_ttc, user
        )
        intermediate_invoice = EstimationInvoicingService.gen_intermediate_invoice(
            get_csrf_request_with_db(), full_estimation_ttc, payment_line, user
        )
        sold_invoice = EstimationInvoicingService.gen_sold_invoice(
            get_csrf_request_with_db(), full_estimation_ttc, user
        )

        assert deposit_invoice.total() == 3000000  # 10%
        assert intermediate_invoice.total() == 15000000  # fixé
        assert sold_invoice.total() == 12000000  # fixé

        assert (
            deposit_invoice.total()
            + intermediate_invoice.total()
            + sold_invoice.total()
            == full_estimation_ttc.total()
        )

    def test_gen_invoice_ref450(self, get_csrf_request_with_db, full_estimation, user):
        sold_invoice = EstimationInvoicingService.gen_sold_invoice(
            get_csrf_request_with_db(), full_estimation, user
        )

        for line in sold_invoice.all_lines:
            assert line.product_id is not None

    @pytest.fixture
    def estimation_with_price_study(
        self,
        get_csrf_request_with_db,
        estimation,
        price_study,
        mk_price_study_product,
        mk_price_study_work_item,
        tva20,
    ):
        mk_price_study_product(
            supplier_ht=10000000, quantity=12.5, mode="supplier_ht", tva=tva20
        )
        mk_price_study_product(ht=10000000, quantity=1, mode="ht", tva=tva20)
        mk_price_study_work_item(
            supplier_ht=10000000,
            work_unit_quantity=4,
            total_quantity=8,
            mode="supplier_ht",
        )
        price_study.sync_amounts(sync_down=True)
        price_study.sync_with_task(get_csrf_request_with_db())
        estimation.deposit = 20
        estimation.update_payment_lines(get_csrf_request_with_db(), 3)
        return estimation

    def test_gen_sold_invoice_with_price_study(
        self, get_csrf_request_with_db, estimation_with_price_study, user
    ):
        estimation = estimation_with_price_study
        sold_invoice = EstimationInvoicingService.gen_sold_invoice(
            get_csrf_request_with_db(), estimation_with_price_study, user
        )
        assert sold_invoice.has_price_study()

        assert len(sold_invoice.price_study.chapters) == 2

        # On a un chapitre avec les factures déjà réglée (acompte + 2)
        assert len(sold_invoice.price_study.chapters[1].products) == 3
        assert (
            sold_invoice.price_study.chapters[1].products[0].description
            == "Facture d'acompte"
        )
        # Total = total du devis - acompte - 2 factures intermédiaires
        assert sold_invoice.ttc == estimation.sold()
        assert sold_invoice.price_study.force_ht is True

    def test_gen_sold_invoice_with_price_study_ref3484(
        self, get_csrf_request_with_db, estimation_with_price_study, user
    ):
        estimation_with_price_study.deposit = 0
        estimation_with_price_study.update_payment_lines(get_csrf_request_with_db(), 1)
        sold_invoice = EstimationInvoicingService.gen_sold_invoice(
            get_csrf_request_with_db(), estimation_with_price_study, user
        )
        assert sold_invoice.has_price_study()

        # Pas de chapitre vide !!
        assert len(sold_invoice.price_study.chapters) == 1

        assert len(sold_invoice.line_groups) == 1


class TestInternalEstimationProcessService:
    def test_sync_with_customer(
        self,
        internal_customer,
        mk_internalestimation,
        mk_expense_type,
        task_line,
        task_line_group,
        dbsession,
        get_csrf_request_with_db,
    ):
        task_line_group.lines = [task_line]
        estimation = mk_internalestimation(status="valid")
        estimation.line_groups = [task_line_group]
        dbsession.add(estimation)
        dbsession.flush()

        request = get_csrf_request_with_db(context=estimation)
        order = estimation.sync_with_customer(request)

        assert estimation.supplier_order_id == order.id
        assert integer_to_amount(order.total, 2) == integer_to_amount(
            estimation.total(), 5
        )
        assert order.supplier.source_company_id == estimation.company_id

        typ = mk_expense_type(internal=True, label="Type interne")
        order = estimation.sync_with_customer(request)
        assert order.lines[0].type_id == typ.id


class TestEstimationService:
    def test_duplicate(
        self, get_csrf_request_with_db, full_estimation, user, customer, project, phase
    ):
        result = EstimationService.duplicate(
            get_csrf_request_with_db(),
            full_estimation,
            user,
            project=project,
            customer=customer,
            phase=phase,
        )
        assert result.internal_number.startswith(
            "Company {0:%Y-%m}".format(datetime.date.today())
        )
        assert len(full_estimation.default_line_group.lines) == len(
            result.default_line_group.lines
        )
        assert len(full_estimation.payment_lines) == len(result.payment_lines)
        assert len(full_estimation.discounts) == len(result.discounts)

    def test__clean_payment_lines(self, full_estimation, dbsession):
        # full_estimation a deux payment_line
        res = EstimationService._clean_payment_lines(full_estimation, dbsession, 2)
        assert len(res) == 2
        res = EstimationService._clean_payment_lines(full_estimation, dbsession, 8)
        assert len(res) == 2
        res = EstimationService._clean_payment_lines(full_estimation, dbsession, 1)
        assert len(res) == 1

    def test__complete_payment_lines(self, full_estimation, dbsession):
        res = EstimationService._complete_payment_lines(full_estimation, dbsession, 2)
        assert len(res) == 2
        res = EstimationService._complete_payment_lines(full_estimation, dbsession, 8)
        assert len(res) == 8
        res = EstimationService._complete_payment_lines(full_estimation, dbsession, 1)
        assert len(res) == 1
        full_estimation.payment_lines = []
        res = EstimationService._complete_payment_lines(full_estimation, dbsession, 8)
        assert len(res) == 8

    def test__update_payment_lines(self, full_estimation, dbsession):
        total = full_estimation.total()
        deposit = full_estimation.deposit_amount_ttc()
        topay = total - deposit
        result = EstimationService._update_computed_payment_lines(
            full_estimation, dbsession, 8, topay
        )
        assert len(result) == 8
        assert sum([line.amount for line in result]) == topay

    def test__update_sold(self, full_estimation, dbsession):
        full_estimation.deposit = 50
        total = full_estimation.total()
        deposit = full_estimation.deposit_amount_ttc()
        topay = total - deposit
        result = EstimationService._update_computed_payment_lines(
            full_estimation, dbsession, 8, topay
        )
        assert len(result) == 8
        assert sum([line.amount for line in result]) == topay
        assert topay * 2 == total
