import pytest

from endi.compute.price_study import (
    ProductSupplierHtComputer,
    ProductHtComputer,
    WorkItemHtComputer,
    WorkItemSupplierHtComputer,
)
from endi.models.config import Config


class TestProductHtMode:
    @pytest.fixture
    def computer(self, mk_price_study_product, tva20):
        p = mk_price_study_product(
            supplier_ht=5000000,
            ht=1000000,
            mode="ht",
            tva=tva20,
        )
        return ProductHtComputer(p, Config)

    def test_unit_ht(self, computer):
        assert computer.unit_ht() == 1000000


class TestWorkItemHtMode:
    @pytest.fixture
    def computer(self, mk_price_study_work_item, tva20):
        p = mk_price_study_work_item(
            supplier_ht=5000000,
            ht=1000000,
            mode="ht",
        )
        p.price_study_work.tva = tva20
        return WorkItemHtComputer(p, Config)

    def test_unit_ht(self, computer):
        assert computer.unit_ht() == 1000000

    def test_unit_ttc(self, computer):
        assert computer.unit_ttc() == 1200000


class TestProductSupplierHtMode:
    @pytest.fixture
    def computer(self, price_study, mk_price_study_product, tva20):
        price_study.general_overhead = 0.11
        p = mk_price_study_product(
            supplier_ht=1000000,
            margin_rate=0.12,
            tva=tva20,
            mode="supplier_ht",
        )
        return ProductSupplierHtComputer(p, Config)

    def test_flat_cost(self, computer):
        assert computer.flat_cost() == 1000000
        computer.product.supplier_ht = None
        assert computer.flat_cost() == 0

    def test_cost_price(self, computer, price_study):
        assert computer.cost_price() == 1110000
        price_study.general_overhead = 0
        assert computer.cost_price() == 1000000

    def test_intermediate_price(self, computer):
        assert int(computer.intermediate_price()) == 1261363
        computer.product.margin_rate = None
        assert int(computer.intermediate_price()) == 1110000

    def test_price_with_contribution(self, dbsession, computer, company):
        assert int(computer.price_with_contribution()) == 1261363
        company.contribution = 10
        dbsession.merge(company)
        dbsession.flush()
        assert int(computer.price_with_contribution()) == 1401515

    def test_price_with_insurance(
        self, dbsession, computer, company, mk_task_insurance_option, estimation
    ):
        assert int(computer.price_with_insurance()) == 1261363
        company.insurance = 10
        dbsession.merge(company)
        dbsession.flush()
        assert int(computer.price_with_insurance()) == 1401515
        company.contribution = 12
        dbsession.merge(company)
        dbsession.flush()
        assert int(computer.price_with_insurance()) == 1592630
        # L'assurance de la task a la priorité
        option = mk_task_insurance_option(rate=4)
        estimation.insurance = option
        dbsession.merge(estimation)
        dbsession.flush()
        assert int(computer.price_with_insurance()) == 1493091

    def test_unit_ht(self, dbsession, computer, company):
        assert int(computer.unit_ht()) == 1261363

        # Avec contribution :
        company.contribution = 10
        dbsession.merge(company)
        dbsession.flush()
        assert int(computer.unit_ht()) == 1401515
        company.insurance = 12
        dbsession.merge(company)
        dbsession.flush()
        assert int(computer.unit_ht()) == 1592630


class TestWorkItemSupplierHtMode:
    @pytest.fixture
    def computer(self, price_study, mk_price_study_work_item, tva20):
        price_study.general_overhead = 0.11
        p = mk_price_study_work_item(
            supplier_ht=1000000,
            mode="supplier_ht",
            work_unit_quantity=0.9,
            total_quantity=5.4,
        )
        p.price_study_work.tva = tva20
        p.price_study_work.margin_rate = 0.12
        return WorkItemSupplierHtComputer(p, Config)

    def test_flat_cost(self, computer):
        assert computer.flat_cost() == 1000000
        computer.product.supplier_ht = None
        assert computer.flat_cost() == 0

    def test_cost_price(self, computer, price_study):
        assert computer.cost_price() == 1110000
        price_study.general_overhead = 0
        assert computer.cost_price() == 1000000

    def test_intermediate_price(self, computer):
        assert int(computer.intermediate_price()) == 1261363
        computer.product.price_study_work.margin_rate = None
        assert int(computer.intermediate_price()) == 1110000

    def test_price_with_contribution(self, dbsession, computer, company):
        assert int(computer.price_with_contribution()) == 1261363
        company.contribution = 10
        dbsession.merge(company)
        dbsession.flush()
        assert int(computer.price_with_contribution()) == 1401515

    def test_price_with_insurance(self, dbsession, computer, company):
        assert int(computer.price_with_insurance()) == 1261363
        company.insurance = 10
        dbsession.merge(company)
        dbsession.flush()
        assert int(computer.price_with_insurance()) == 1401515
        company.contribution = 12
        dbsession.merge(company)
        dbsession.flush()
        assert int(computer.price_with_insurance()) == 1592630

    def test_unit_ht(self, computer, company):
        assert int(computer.unit_ht()) == 1261363

        # Avec contribution :
        company.contribution = 10
        assert int(computer.unit_ht()) == 1401515

    def test_unit_ttc(self, computer):
        assert int(computer.unit_ttc()) == 1513636

    def test_work_unit_flat_cost(self, computer):
        assert computer.work_unit_flat_cost() == 900000

    def test_full_flat_cost(self, computer):
        assert computer.full_flat_cost() == 5400000

    def test_full_cost_price(self, computer):
        assert computer.full_cost_price() == 5994000

    def test_full_intermediate_price(self, computer):
        assert int(computer.full_intermediate_price()) == 6811363

    def test_full_price_with_contribution(self, dbsession, computer, company):
        assert int(computer.full_price_with_contribution()) == 6811363
        company.contribution = 10
        dbsession.merge(company)
        dbsession.flush()
        assert int(computer.full_price_with_contribution()) == 7568181

    def test_full_price_with_insurance(self, dbsession, computer, company):
        assert int(computer.full_price_with_insurance()) == 6811363
        company.insurance = 10
        dbsession.merge(company)
        dbsession.flush()
        assert int(computer.full_price_with_insurance()) == 7568181
        company.contribution = 12
        dbsession.merge(company)
        dbsession.flush()
        assert int(computer.full_price_with_insurance()) == 8600206
