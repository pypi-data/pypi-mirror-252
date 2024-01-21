from pytest import fixture

from endi.views.price_study.rest_api import (
    RestPriceStudyView,
    RestPriceStudyChapterView,
    RestPriceStudyProductView,
    RestWorkItemView,
    RestPriceStudyDiscountView,
)

from endi.utils.renderer import get_json_dict_repr


@fixture
def full_price_study(
    get_csrf_request_with_db,
    price_study,
    price_study_chapter,
    mk_price_study_product,
    mk_price_study_work,
    mk_price_study_work_item,
    tva,
):
    request = get_csrf_request_with_db()
    ps_product = mk_price_study_product(
        description="Description",
        ht=100000,
        quantity=5,
        chapter=price_study_chapter,
        tva=tva,
    )
    price_study_work = mk_price_study_work(
        title="Title",
        description="Description",
        chapter=price_study_chapter,
        quantity=5,
        tva=tva,
    )
    work_item = mk_price_study_work_item(
        ht=100000,
        work_unit_quantity=2,
        price_study_work=price_study_work,
    )
    work_item.on_before_commit(request, "add")
    ps_product.on_before_commit(request, "add")
    price_study.sync_amounts()
    return price_study


class TestRestPriceStudyView:
    def test_margin_rate_reset_view(
        self,
        get_csrf_request_with_db,
        price_study,
        price_study_work,
        mk_price_study_work_item,
        mk_price_study_product,
        company,
    ):
        company.margin_rate = 0.4
        product = mk_price_study_product()
        request = get_csrf_request_with_db(context=price_study)

        view = RestPriceStudyView(price_study, request)
        view.margin_rate_reset_view()
        assert price_study_work.margin_rate == 0.4
        assert product.margin_rate == 0.4


class TestRestPriceStudyChapterView:
    def test_add(self, get_csrf_request_with_db, price_study):
        request = get_csrf_request_with_db(
            post={"title": "Chapter", "description": "Chapitre 1"}
        )

        view = RestPriceStudyChapterView(price_study, request)
        result = view.post()
        result = get_json_dict_repr(result, request)

        assert result["title"] == "Chapter"
        assert result["description"] == "Chapitre 1"
        assert "id" in result
        assert result["task_line_group_id"] is not None

    def test_edit(self, get_csrf_request_with_db, price_study_chapter):
        request = get_csrf_request_with_db(post={"description": "Chapitre 2"})
        view = RestPriceStudyChapterView(price_study_chapter, request)
        result = view.put()
        result = get_json_dict_repr(result, request)
        assert result["title"] == price_study_chapter.title
        assert result["description"] == "Chapitre 2"
        assert result["id"] == price_study_chapter.id

        request = get_csrf_request_with_db(post={"title": "New title"})
        view = RestPriceStudyChapterView(price_study_chapter, request)
        result = view.put()
        result = get_json_dict_repr(result, request)
        assert result["title"] == "New title"
        assert result["description"] == "Chapitre 2"
        assert result["id"] == price_study_chapter.id

    def test_delete(
        self,
        get_csrf_request_with_db,
        price_study,
        price_study_chapter,
        mk_price_study_product,
        tva,
    ):
        request = get_csrf_request_with_db()
        price_study_product = mk_price_study_product(ht=2000000, mode="ht", tva=tva)
        price_study_product.on_before_commit(request, "add")
        assert price_study.ht == 2000000
        view = RestPriceStudyChapterView(price_study_chapter, request)
        view.delete()
        assert price_study.ht == 0


class TestRestPriceStudyProductView:
    def test_add_product(
        self, get_csrf_request_with_db, price_study_chapter, tva, product
    ):
        request = get_csrf_request_with_db(
            post={
                "type_": "price_study_product",
                "description": "Description",
                "quantity": 5,
                "tva_id": tva.id,
                "product_id": product.id,
                "supplier_ht": 1,
                "margin_rate": 0.12,
                "mode": "supplier_ht",
            }
        )
        price_study_chapter.price_study.general_overhead = 0.11
        view = RestPriceStudyProductView(price_study_chapter, request)
        result_obj = view.post()
        result = get_json_dict_repr(result_obj, request)
        assert result["type_"] == "price_study_product"
        assert result["id"] is not None
        assert result["description"] == "Description"
        assert result["quantity"] == 5
        assert result["product_id"] == product.id
        assert result["tva_id"] == tva.id
        # Check amounts where synced
        assert result["ht"] == 1.26136
        assert result["total_ht"] == 6.30682
        # Check parent amounts were synced
        assert int(price_study_chapter.price_study.ht) == 631000

    def test_add_work(
        self, price_study_chapter, get_csrf_request_with_db, product, tva
    ):
        from endi.views.price_study.rest_api import RestPriceStudyProductView

        request = get_csrf_request_with_db(
            post={
                "type_": "price_study_work",
                "title": "Title",
                "description": "Description",
                "product_id": product.id,
                "tva_id": tva.id,
            }
        )
        view = RestPriceStudyProductView(price_study_chapter, request)

        result = view.post()
        result = get_json_dict_repr(result, request)

        assert result["type_"] == "price_study_work"
        assert result["id"] is not None
        assert result["description"] == "Description"
        assert result["title"] == "Title"
        assert result["product_id"] == product.id
        assert result["tva_id"] == tva.id

    def test_edit_product(
        self,
        price_study,
        price_study_chapter,
        mk_price_study_product,
        get_csrf_request_with_db,
        tva,
        product,
        company,
    ):
        price_study.general_overhead = 0.11
        price_study_product = mk_price_study_product(
            description="Description",
            quantity=5,
            tva_id=tva.id,
            product_id=product.id,
            supplier_ht=1,
            margin_rate=0.12,
            chapter=price_study_chapter,
            mode="supplier_ht",
        )
        request = get_csrf_request_with_db(
            post={
                "description": "New description",
                "quantity": 10,
                "supplier_ht": 2,
                "margin_rate": 0.12,
            }
        )

        view = RestPriceStudyProductView(price_study_product, request)
        result = view.put()
        result = get_json_dict_repr(result, request)

        assert result["type_"] == "price_study_product"
        assert result["id"] == price_study_product.id
        assert result["description"] == "New description"
        assert result["quantity"] == 10
        assert result["tva_id"] == tva.id
        # Check amounts where synced
        assert result["ht"] == 2.52273
        assert result["total_ht"] == 25.22727

    def test_edit_work(
        self,
        price_study,
        price_study_chapter,
        mk_price_study_work,
        mk_price_study_work_item,
        get_csrf_request_with_db,
        mk_tva,
    ):
        price_study.general_overhead = 0.11
        price_study_work = mk_price_study_work(
            title="Title",
            description="Description",
            chapter=price_study_chapter,
        )
        mk_price_study_work_item(
            supplier_ht=100000,
            work_unit_quantity=2,
            total_quantity=6.66,
            price_study_work=price_study_work,
            mode="supplier_ht",
        )
        request = get_csrf_request_with_db(
            post={
                "title": "New title",
                "description": "New description",
                "quantity": 10,
                "supplier_ht": 2,
                "margin_rate": 0.12,
            }
        )

        view = RestPriceStudyProductView(price_study_work, request)
        result = view.put()
        result = get_json_dict_repr(result, request)

        assert result["type_"] == "price_study_work"
        assert result["id"] == price_study_work.id
        assert result["description"] == "New description"
        assert result["title"] == "New title"
        assert result["quantity"] == 10

        # Test encure_tva
        assert result["margin_rate"] == 0.12
        # Check amounts where synced
        assert result["ht"] == 2.52273
        assert result["total_ht"] == 25.22727

    def test_product_load_from_catalog(
        self,
        price_study,
        price_study_chapter,
        get_csrf_request_with_db,
        mk_sale_product,
        tva,
        product,
        company,
    ):
        price_study.general_overhead = 0.11
        company.margin_rate = 0.15
        sale_product = mk_sale_product(
            supplier_ht=100000,
            unity="unity",
            mode="supplier_ht",
            company=company,
        )

        request = get_csrf_request_with_db(post={"sale_product_ids": [sale_product.id]})

        view = RestPriceStudyProductView(price_study_chapter, request)
        result = view.load_from_catalog_view()
        result = get_json_dict_repr(result[0], request)

        assert result["type_"] == "price_study_product"
        assert result["supplier_ht"] == 1
        assert result["quantity"] == 1
        assert result["unity"] == "unity"
        assert result["ht"] == 1.30588
        assert result["total_ht"] == 1.30588

    def test_work_load_from_catalog(
        self,
        price_study,
        price_study_chapter,
        get_csrf_request_with_db,
        mk_sale_product_work,
        mk_sale_product_work_item,
        tva,
        product,
        tva10,
        mk_product,
        company,
    ):
        product10 = mk_product(tva=tva10)
        price_study.general_overhead = 0.11
        company.margin_rate = 0.15
        sale_product_work = mk_sale_product_work(
            title="Title",
            description="Description",
            tva_id=tva10.id,
            product_id=product10.id,
            company=company,
        )

        mk_sale_product_work_item(
            sale_product_work=sale_product_work,
            _supplier_ht=100000,
            _mode="supplier_ht",
            locked=False,
        )
        request = get_csrf_request_with_db(
            post={"sale_product_ids": [sale_product_work.id]}
        )

        view = RestPriceStudyProductView(price_study_chapter, request)
        result = view.load_from_catalog_view()
        result = get_json_dict_repr(result[0], request)

        assert result["type_"] == "price_study_work"

        # La tva et le produit sont settés avec les valeurs par défaut
        assert result["tva_id"] == tva.id
        assert result["product_id"] == product.id
        # Computed values
        assert result["ht"] == 1.30588
        assert result["total_ht"] == 1.30588

    def test_product_delete(
        self,
        price_study,
        price_study_chapter,
        get_csrf_request_with_db,
        mk_price_study_product,
        tva,
    ):
        price_study.general_overhead = 0.11

        price_study_product = mk_price_study_product(
            description="Description",
            quantity=5,
            supplier_ht=100000,
            margin_rate=0.12,
            chapter=price_study_chapter,
            tva_id=tva.id,
            mode="supplier_ht",
        )
        request = get_csrf_request_with_db()
        price_study_product.on_before_commit(get_csrf_request_with_db(), "add")

        # Check total is set
        assert price_study.ht == 631000

        request.context = price_study_product
        view = RestPriceStudyProductView(price_study_product, request)
        view.delete()
        # Check it's set to 0
        assert price_study.ht == 0

    def test_work_delete(
        self,
        get_csrf_request_with_db,
        price_study,
        price_study_work,
        mk_price_study_work_item,
    ):
        request = get_csrf_request_with_db()
        price_study_work.quantity = 5
        item = mk_price_study_work_item(ht=100000, price_study_work=price_study_work)
        item.on_before_commit(request, "add")
        item = mk_price_study_work_item(ht=100000, price_study_work=price_study_work)
        item.on_before_commit(request, "add")
        item = mk_price_study_work_item(ht=100000, price_study_work=price_study_work)
        item.on_before_commit(request, "add")
        assert price_study.ht == 1500000

        view = RestPriceStudyProductView(price_study_work, request)
        view.delete()
        # Check it's set to 0
        assert price_study.ht == 0

    def test_percent_discount_refresh(
        self,
        full_price_study,
        get_csrf_request_with_db,
        mk_price_study_discount,
        tva,
    ):
        discount = mk_price_study_discount(
            description="Description",
            type_="percentage",
            percentage=5,
            tva=tva,
            price_study=full_price_study,
        )
        discount.on_before_commit(get_csrf_request_with_db(), "add")

        request = get_csrf_request_with_db(
            post={
                "ht": 2,
            }
        )
        # On édite le premier produit
        view = RestPriceStudyProductView(full_price_study.products[0], request)
        view.put()

        # On vérifie que la remise et les totaux de l’étude sont justes
        assert full_price_study.ht == 1425000


class TestRestWorkItemView:
    def test_load_from_catalog_view(
        self,
        price_study,
        price_study_chapter,
        get_csrf_request_with_db,
        mk_sale_product,
        mk_price_study_work,
    ):
        price_study.general_overhead = 0.11
        price_study_work = mk_price_study_work(
            title="Title",
            description="Description",
            chapter=price_study_chapter,
            quantity=5,
            margin_rate=0.15,
        )
        sale_product = mk_sale_product(
            supplier_ht=100000, unity="unity", mode="supplier_ht"
        )
        request = get_csrf_request_with_db(post={"sale_product_ids": [sale_product.id]})
        view = RestWorkItemView(price_study_work, request)
        result = view.load_from_catalog_view()
        result = get_json_dict_repr(result[0], request)
        assert len(price_study_work.items) == 1
        assert result["unity"] == "unity"
        assert result["mode"] == "supplier_ht"
        assert result["supplier_ht"] == 1
        assert result["work_unit_quantity"] == 1
        assert result["quantity_inherited"] is True
        assert result["work_unit_ht"] == 1.30588

    def test_add(
        self,
        get_csrf_request_with_db,
        price_study,
        price_study_work,
        mk_price_study_work_item,
        tva,
    ):
        request = get_csrf_request_with_db(context=price_study_work)
        price_study_work.quantity = 5
        request = get_csrf_request_with_db(
            post={
                "description": "test",
                "unity": "h",
                "ht": 120,
                "mode": "ht",
                "work_unit_quantity": 2,
            }
        )
        view = RestWorkItemView(price_study_work, request)
        result = view.post()
        result = get_json_dict_repr(result, request)
        assert result["ht"] == 120
        assert result["mode"] == "ht"
        assert result["work_unit_ht"] == 240
        assert result["unity"] == "h"
        assert result["total_ht"] == 1200

    def test_edit(
        self,
        get_csrf_request_with_db,
        price_study,
        price_study_work,
        mk_price_study_work_item,
        tva,
        company,
    ):
        price_study.general_overhead = 0.12
        price_study_work.quantity = 5
        price_study_work.margin_rate = 0.11
        work_item = mk_price_study_work_item(
            ht=12000000, work_unit_quantity=2, unity="heure(s)", mode="ht"
        )
        request = get_csrf_request_with_db(
            post={
                "unity": "h",
                "mode": "supplier_ht",
                "supplier_ht": 100,
                "work_unit_quantity": 2,
            },
            context=work_item,
        )
        view = RestWorkItemView(work_item, request)
        result = view.put()

        result = get_json_dict_repr(result, request)
        assert result["mode"] == "supplier_ht"
        assert result["supplier_ht"] == 100
        assert result["ht"] == 125.84270
        assert result["work_unit_ht"] == 251.68539
        assert result["unity"] == "h"
        assert result["total_ht"] == 1258.42697

        assert result["work_unit_quantity"] == 2
        assert result["total_quantity"] == 10

        assert price_study.ht == 125843000

    def test_work_item_delete(
        self,
        price_study,
        get_csrf_request_with_db,
        price_study_work,
        mk_price_study_work_item,
    ):
        request = get_csrf_request_with_db()
        price_study_work.quantity = 5
        item = mk_price_study_work_item(ht=100000, price_study_work=price_study_work)
        item.on_before_commit(request, "add")
        item = mk_price_study_work_item(ht=100000, price_study_work=price_study_work)
        item.on_before_commit(request, "add")
        item = mk_price_study_work_item(ht=100000, price_study_work=price_study_work)
        item.on_before_commit(request, "add")
        assert price_study.ht == 1500000

        view = RestWorkItemView(item, request)
        view.delete()
        assert price_study_work.ht == 200000
        assert price_study_work.total_ht == 1000000
        assert price_study.ht == 1000000


class TestRestPriceStudyDiscountView:
    def test_add_discount(
        self,
        full_price_study,
        get_csrf_request_with_db,
        tva,
    ):
        assert full_price_study.ht == 1500000

        request = get_csrf_request_with_db(
            post={
                "type_": "amount",
                "description": "Description",
                "amount": 1,
                "tva_id": tva.id,
            }
        )
        view = RestPriceStudyDiscountView(full_price_study, request)
        result = view.post()

        assert result.amount == 100000
        assert full_price_study.ht == 1400000

    def test_edit_discount(
        self,
        full_price_study,
        get_csrf_request_with_db,
        mk_price_study_discount,
        tva,
    ):
        discount = mk_price_study_discount(
            description="Description",
            type_="amount",
            amount=100000,
            tva=tva,
            price_study=full_price_study,
        )
        discount.on_before_commit(get_csrf_request_with_db(), "add")

        request = get_csrf_request_with_db(
            post={
                "description": "New description",
                "percentage": 5,
                "type_": "percentage",
                "tva_id": tva.id,
            }
        )
        view = RestPriceStudyDiscountView(discount, request)
        result = view.put()

        assert result.percentage == 5
        assert result.total_ht() == 75000

        assert full_price_study.ht == 1425000

    def test_delete(
        self,
        full_price_study,
        get_csrf_request_with_db,
        mk_price_study_discount,
        tva,
    ):
        discount = mk_price_study_discount(
            description="Description",
            type_="amount",
            amount=100000,
            tva=tva,
            price_study=full_price_study,
        )
        discount.on_before_commit(get_csrf_request_with_db(), "add")
        request = get_csrf_request_with_db()
        view = RestPriceStudyDiscountView(discount, request)
        view.delete()
        assert len(full_price_study.discounts) == 0
        assert full_price_study.ht == 1500000
