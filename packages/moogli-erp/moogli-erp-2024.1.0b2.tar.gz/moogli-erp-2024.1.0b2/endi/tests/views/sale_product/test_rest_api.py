import pytest
from endi.utils.renderer import get_json_dict_repr
from endi.views.sale_product.rest_api import (
    RestSaleProductView,
    RestWorkItemView,
)
from endi.models.sale_product import WorkItem


class TestRestSaleProductView:
    @pytest.fixture
    def callview(self, company, get_csrf_request_with_db):
        def call_it(params, ctx=company, method="post"):
            request = get_csrf_request_with_db(context=ctx, post=params)
            view = RestSaleProductView(ctx, request)
            result = getattr(view, method)()
            return get_json_dict_repr(result, None)

        return call_it

    def test_product_add(self, callview, company):
        json_result = callview({"type_": "sale_product_material", "label": "label"})

        assert json_result["label"] == "label"
        assert json_result["type_"] == "sale_product_material"
        assert json_result["company_id"] == company.id

    def test_work_add(self, callview, company):
        json_result = callview({"type_": "sale_product_work", "label": "label"})

        assert json_result["label"] == "label"
        assert json_result["type_"] == "sale_product_work"
        assert json_result["company_id"] == company.id
        assert json_result["archived"] is False

    def test_edit_product(self, callview, mk_sale_product, tva, product, company):

        company.general_overhead = 0.11
        company.margin_rate = 0.12
        sale_product = mk_sale_product(
            label="label",
            type_="sale_product_material",
            tva_id=tva.id,
            product_id=product.id,
            supplier_ht=100000,
            mode="supplier_ht",
        )
        sale_product.on_before_commit("add")
        assert int(sale_product.ht) == 126136

        json_result = callview(
            {
                "label": "New label",
                "description": "Description",
                "supplier_ht": "",
                "ht": 1,
                "tva_id": "",
                "archived": True,
            },
            ctx=sale_product,
            method="put",
        )

        assert json_result["ht"] == 1
        assert sale_product.ht == 100000
        assert json_result["label"] == "New label"
        assert json_result["description"] == "Description"
        assert json_result["tva_id"] == None
        assert json_result["product_id"] == None
        assert json_result["archived"] is True

    def test_edit_work(self, callview, mk_sale_product_work, tva, product, company):
        company.general_overhead = 0.11
        company.margin_rate = (0.12,)
        sale_product_work = mk_sale_product_work(
            label="label",
            tva_id=tva.id,
            product_id=product.id,
        )
        sale_product_work.on_before_commit("add")

        json_result = callview(
            {
                "label": "New label",
                "description": "Description",
                "ht": 1,
                "tva_id": "",
            },
            ctx=sale_product_work,
            method="put",
        )

        assert json_result["ht"] == 0
        assert json_result["label"] == "New label"
        assert json_result["description"] == "Description"
        assert json_result["tva_id"] == None
        assert json_result["product_id"] == None


class TestRestWorkItemView:
    @pytest.fixture
    def callview(self, get_csrf_request_with_db):
        def call_it(params, ctx, method="post"):
            request = get_csrf_request_with_db(post=params, context=ctx)
            view = RestWorkItemView(ctx, request)
            result = getattr(view, method)()
            return get_json_dict_repr(result, None)

        return call_it

    def test_add_work_item(self, callview, mk_sale_product_work, tva, product, company):
        company.general_overhead = 0.11
        company.margin_rate = 0.12
        sale_product_work = mk_sale_product_work(
            label="label",
            tva_id=tva.id,
        )

        json_result = callview(
            {
                "label": "Label",
                "description": "Description",
                "supplier_ht": 1,
                "quantity": 2,
                "type_": "sale_product_material",
                "mode": "supplier_ht",
            },
            sale_product_work,
        )

        assert json_result["description"] == "Description"
        assert json_result["locked"] is True

        # Computing
        assert json_result["ht"] == 1.26136
        assert json_result["total_ht"] == 2.52273

        assert int(sale_product_work.ht) == 252272

        result = WorkItem.query().first()
        assert result.base_sale_product is not None
        assert result.base_sale_product.label == "Label"
        assert result.base_sale_product.supplier_ht == 100000

    def test_edit_work_item(
        self,
        callview,
        mk_sale_product_work,
        mk_sale_product_work_item,
        mk_sale_product,
        tva,
        product,
        company,
        mk_work_unit,
    ):
        mk_work_unit(label="Kg")
        company.general_overhead = 0.11
        company.margin_rate = 0.12
        sale_product_work = mk_sale_product_work(
            label="label",
            tva_id=tva.id,
        )
        sale_product = mk_sale_product(
            supplier_ht=100000,
            mode="supplier_ht",
            description="Description",
            unity="Ml",
        )
        sale_product.sync_amounts()
        work_item = mk_sale_product_work_item(
            description="Description",
            sale_product_work=sale_product_work,
            _supplier_ht=200000,
            quantity=2,
            base_sale_product=sale_product,
            _mode="supplier_ht",
        )

        work_item.on_before_commit("add")
        # This value is inherited from the base_sale_product
        assert int(work_item.ht) == 126136

        json_result = callview(
            {
                "label": "Label",
                "description": "Description",
                "supplier_ht": "",
                "unity": "Kg",
                "ht": 20,
                "quantity": 5,
                "mode": "ht",
            },
            work_item,
            method="put",
        )

        # Still locked
        assert sale_product.ht == 2000000
        assert sale_product.unity == "Kg"
        assert sale_product.mode == "ht"
        assert json_result["locked"] is True
        assert json_result["ht"] == 20
        assert json_result["total_ht"] == 100.0
        assert sale_product_work.ht == 10000000

    def test_delete_work_item(
        self,
        callview,
        mk_sale_product_work,
        mk_sale_product_work_item,
        mk_sale_product,
        tva,
        product,
        company,
    ):
        company.general_overhead = 0.11
        company.margin_rate = 0.12
        sale_product_work = mk_sale_product_work(
            label="label",
            tva_id=tva.id,
        )
        sale_product = mk_sale_product(
            supplier_ht=100000,
            mode="supplier_ht",
            description="Description",
        )
        sale_product.sync_amounts()
        work_item1 = mk_sale_product_work_item(
            description="Description",
            sale_product_work=sale_product_work,
            _supplier_ht=200000,
            quantity=2,
            _mode="supplier_ht",
            base_sale_product=sale_product,
        )
        work_item2 = mk_sale_product_work_item(
            description="Description 2",
            sale_product_work=sale_product_work,
            _supplier_ht=200000,
            quantity=2,
            _mode="supplier_ht",
            base_sale_product=sale_product,
            locked=False,
        )

        work_item1.on_before_commit("add")
        work_item2.on_before_commit("add")
        # This value is inherited from the base_sale_product
        assert int(work_item1.ht) == 126136
        # This value is not inherited (locked is False)
        assert int(work_item2.ht) == 252272

        assert int(sale_product_work.ht) == 756818

        callview({}, work_item1, method="delete")

        assert int(sale_product_work.ht) == 504545
