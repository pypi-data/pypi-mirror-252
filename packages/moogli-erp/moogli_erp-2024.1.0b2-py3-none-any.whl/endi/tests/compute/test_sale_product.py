import pytest

from endi.compute.sale_product import (
    SaleProductHtComputer,
    SaleProductWorkItemHtComputer,
    SaleProductTtcComputer,
    SaleProductSupplierHtComputer,
    SaleProductWorkItemSupplierHtComputer,
)
from endi.models.config import Config


class TestHtMode:
    @pytest.fixture
    def computer(self, mk_sale_product, tva20):
        p = mk_sale_product(
            supplier_ht=5000000,
            ht=1000000,
            mode="ht",
            tva=tva20,
        )
        return SaleProductHtComputer(p, Config)

    def test_unit_ht(self, computer):
        assert computer.unit_ht() == 1000000
        computer.product.ht = None
        assert computer.unit_ht() == 0

    def test_unit_ttc(self, computer):
        assert computer.unit_ttc() == 1200000


class TestWorkItemHtMode:
    @pytest.fixture
    def computer(self, mk_sale_product_work_item, sale_product_work, tva20):
        sale_product_work.tva = tva20
        p = mk_sale_product_work_item(
            _supplier_ht=5000000,
            _ht=1000000,
            _mode="ht",
            locked=False,
            sale_product_work=sale_product_work,
        )
        return SaleProductWorkItemHtComputer(p, Config)

    def test_unit_ht(self, computer):
        assert computer.unit_ht() == 1000000

    def test_unit_ttc(self, computer):
        assert computer.unit_ttc() == 1200000

    def test_flat_cost(self, computer):
        assert computer.flat_cost() == 0

    def test_full_flat_cost(self, computer):
        assert computer.full_flat_cost() == 0


class TestTtcMode:
    @pytest.fixture
    def computer(self, mk_sale_product, tva20):
        p = mk_sale_product(
            supplier_ht=5000000,
            ttc=1000000,
            mode="ttc",
            tva=tva20,
        )
        return SaleProductTtcComputer(p, Config)

    def test_unit_ht(self, computer):
        assert int(computer.unit_ht()) == 833330

    def test_unit_ttc(self, computer):
        assert computer.unit_ttc() == 1000000
        computer.product.ttc = None
        assert computer.unit_ttc() == 0


class TestSupplierHtMode:
    @pytest.fixture
    def computer(self, mk_sale_product, tva20, company):
        company.general_overhead = 0.11
        company.margin_rate = 0.12

        p = mk_sale_product(
            supplier_ht=1000000,
            tva=tva20,
            mode="supplier_ht",
        )
        # assert int(base_product.ht) == 126136
        return SaleProductSupplierHtComputer(p, Config)

    def test_flat_cost(self, computer):
        assert computer.flat_cost() == 1000000
        computer.product.supplier_ht = None
        assert computer.flat_cost() == 0

    def test_cost_price(self, computer, company):
        assert computer.cost_price() == 1110000
        company.general_overhead = 0
        assert computer.cost_price() == 1000000

    def test_intermediate_price(self, computer, company):
        assert int(computer.intermediate_price()) == 1261363
        company.margin_rate = None
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

    def test_unit_ht(self, dbsession, computer, company):
        assert int(computer.unit_ht()) == 1261363

        # Avec contribution :
        company.contribution = 10
        dbsession.merge(company)
        dbsession.flush()
        assert int(computer.unit_ht()) == 1401515
        # Avec assurance
        company.insurance = 12
        dbsession.merge(company)
        dbsession.flush()
        assert int(computer.unit_ht()) == 1592630

    def test_unit_ttc(self, computer):
        assert int(computer.unit_ttc()) == 1513636


class TestWorkItemSupplierHtMode:
    @pytest.fixture
    def computer(self, mk_sale_product_work_item, sale_product_work, tva20, company):
        company.general_overhead = 0.11
        company.margin_rate = 0.12
        p = mk_sale_product_work_item(
            _supplier_ht=1000000,
            _mode="supplier_ht",
            locked=False,
            sale_product_work=sale_product_work,
            quantity=5.4,
        )
        return SaleProductWorkItemSupplierHtComputer(p, Config)

    def test_flat_cost(self, computer):
        assert computer.flat_cost() == 1000000
        computer.product._supplier_ht = None
        assert computer.flat_cost() == 0

    def test_cost_price(self, computer, company):
        assert computer.cost_price() == 1110000
        company.general_overhead = 0
        assert computer.cost_price() == 1000000

    def test_intermediate_price(self, computer, company):
        assert int(computer.intermediate_price()) == 1261363
        company.margin_rate = None
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

    def test_unit_ht(self, dbsession, computer, company):
        assert int(computer.unit_ht()) == 1261363
        # Avec contribution :
        company.contribution = 10
        dbsession.merge(company)
        dbsession.flush()
        assert int(computer.unit_ht()) == 1401515

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
