import pytest

from endi.models.sale_product.services import (
    SaleProductService,
)


class TestSaleProductService:
    @pytest.fixture
    def sale_product(self, mk_sale_product, tva, product):
        return mk_sale_product(
            ht=100000,
            mode="ht",
            tva=tva,
            product=product,
        )

    def test__ensure_tva(self, sale_product, tva, product, mk_product, tva10):
        SaleProductService._ensure_tva(sale_product)
        assert sale_product.product_id == product.id

    def test__ensure_tva_no_tva(self, sale_product):
        sale_product.tva_id = None
        SaleProductService._ensure_tva(sale_product)
        assert sale_product.product_id is None

    def test__ensure_tva_wrong_product(self, sale_product, mk_product, tva10):
        other_product = mk_product(name="other", tva=tva10)
        sale_product.product_id = other_product.id
        sale_product.product = other_product
        SaleProductService._ensure_tva(sale_product)
        assert sale_product.product_id is None

    def test_get_computer(self, sale_product):
        from endi.compute.sale_product import (
            SaleProductSupplierHtComputer,
            SaleProductTtcComputer,
            SaleProductHtComputer,
        )

        assert isinstance(
            SaleProductService._get_computer(sale_product), SaleProductHtComputer
        )
        sale_product.mode = "ttc"
        assert isinstance(
            SaleProductService._get_computer(sale_product), SaleProductTtcComputer
        )
        sale_product.mode = "supplier_ht"
        assert isinstance(
            SaleProductService._get_computer(sale_product),
            SaleProductSupplierHtComputer,
        )

    def test_on_before_commit_add(self, sale_product):
        assert sale_product.ttc == 0
        SaleProductService.on_before_commit(sale_product, "add")
        assert sale_product.ttc == 120000

    def test_on_before_commit_update(self, sale_product):
        SaleProductService.on_before_commit(sale_product, "update", {"other": "o"})
        assert sale_product.ttc == 0
        for key in (
            "supplier_ht",
            "ht",
            "ttc",
            "mode",
            "tva_id",
        ):
            sale_product.ttc = 0
            SaleProductService.on_before_commit(sale_product, "update", {key: "o"})
            assert sale_product.ttc == 120000
