import pytest
from endi.models.price_study.product import PriceStudyProduct
from endi.models.price_study.price_study import PriceStudy
from endi.models.price_study.services import (
    BasePriceStudyProductService,
    PriceStudyService,
    PriceStudyProductService,
    PriceStudyWorkService,
)
from endi.tests.tools import Dummy
from endi.compute.math_utils import amount


@pytest.fixture
def price_study_product(mk_price_study_product):
    return mk_price_study_product(
        supplier_ht=10000000,
        margin_rate=0.1,
        mode="supplier_ht",
    )


class TestPriceStudyService:
    def test_is_editable(self, price_study):
        for status in ("draft", "invalid"):
            price_study.task.status = status
            assert PriceStudyService.is_editable(price_study)
        for status in ("wait", "valid"):
            price_study.task.status = status
            assert not PriceStudyService.is_editable(price_study)

    def test_is_admin_editable(self, price_study):
        for status in ("draft", "invalid", "wait"):
            price_study.task.status = status
            assert PriceStudyService.is_admin_editable(price_study)
        for status in ("valid",):
            price_study.task.status = status
            assert not PriceStudyService.is_admin_editable(price_study)

    def test_json_totals_product_material(
        self,
        csrf_request,
        price_study,
        mk_price_study_product,
    ):
        price_study.general_overhead = 0.1

        p = mk_price_study_product(
            supplier_ht=10000000,
            margin_rate=0.1,
            mode="supplier_ht",
            quantity=4,
            unity="m2",
        )
        p.sync_amounts()
        totals = price_study.json_totals(csrf_request)
        assert "labor" in totals
        assert "material" in totals
        for key in ("flat_cost", "general_overhead", "margin", "hours", "total_ht"):
            assert totals["labor"][key] == 0

        assert totals["material"]["flat_cost"] == 400
        assert totals["material"]["general_overhead"] == 40
        assert totals["material"]["margin"] == 48.88889
        assert totals["material"]["total_ht"] == 488.88889

    def test_json_totals_product_ht(
        self,
        csrf_request,
        price_study,
        mk_price_study_product,
    ):
        p = mk_price_study_product(ht=10000000, mode="ht", quantity=4, unity="m2")
        p.sync_amounts()
        price_study.general_overhead = 0.1
        totals = price_study.json_totals(csrf_request)
        assert "labor" in totals
        assert "material" in totals
        for key in ("flat_cost", "general_overhead", "margin", "hours"):
            assert totals["labor"][key] == 0

        assert totals["material"]["flat_cost"] == 0
        assert totals["material"]["general_overhead"] == 0
        assert totals["material"]["margin"] == 0
        assert totals["material"]["total_ht"] == 400

    def test_json_totals_product_labor(
        self, csrf_request, price_study, mk_price_study_product, company
    ):
        price_study.general_overhead = 0.1
        p = mk_price_study_product(ht=10000000, mode="ht", quantity=4, unity="heures")
        p.sync_amounts()
        p = mk_price_study_product(
            supplier_ht=10000000,
            margin_rate=0.1,
            mode="supplier_ht",
            quantity=4,
            unity="forfait main d'oeuvre",
        )
        p.sync_amounts()

        totals = price_study.json_totals(csrf_request)
        assert "labor" in totals
        assert "material" in totals
        for key in ("flat_cost", "general_overhead", "margin", "total_ht"):
            assert totals["material"][key] == 0

        assert totals["labor"]["flat_cost"] == 400
        assert totals["labor"]["general_overhead"] == 40
        assert totals["labor"]["margin"] == 48.88889
        assert totals["labor"]["total_ht"] == 888.88889

    def test_json_totals_workitem_material(
        self,
        csrf_request,
        price_study,
        price_study_work,
        mk_price_study_work_item,
    ):
        price_study_work.margin_rate = 0.1
        price_study.general_overhead = 0.1
        price_study_work.quantity = 3
        p = mk_price_study_work_item(
            supplier_ht=10000000,
            mode="supplier_ht",
            work_unit_quantity=4,
            unity="m2",
            price_study_work=price_study_work,
        )
        p.sync_quantities()
        p.sync_amounts()

        totals = price_study.json_totals(csrf_request)
        assert "labor" in totals
        assert "material" in totals
        for key in ("flat_cost", "general_overhead", "margin", "hours", "total_ht"):
            assert totals["labor"][key] == 0

        assert totals["material"]["flat_cost"] == 1200
        assert totals["material"]["general_overhead"] == 120
        assert totals["material"]["margin"] == 146.66667
        assert totals["material"]["total_ht"] == 1466.66667

    def test_json_totals_workitem_ht(
        self,
        csrf_request,
        price_study,
        price_study_work,
        mk_price_study_work_item,
    ):
        price_study_work.margin_rate = 0.1
        price_study.general_overhead = 0.1
        price_study_work.quantity = 3
        p = mk_price_study_work_item(
            ht=10000000,
            mode="ht",
            work_unit_quantity=4,
            unity="m2",
            price_study_work=price_study_work,
        )
        p.sync_quantities()
        p.sync_amounts()
        totals = price_study.json_totals(csrf_request)
        assert "labor" in totals
        assert "material" in totals
        for key in ("flat_cost", "general_overhead", "margin", "hours"):
            assert totals["labor"][key] == 0

        assert totals["material"]["flat_cost"] == 0
        assert totals["material"]["general_overhead"] == 0
        assert totals["material"]["margin"] == 0
        assert totals["material"]["total_ht"] == 1200

    def test_json_totals_workitem_labor(
        self,
        csrf_request,
        price_study,
        price_study_work,
        mk_price_study_work_item,
    ):
        price_study_work.margin_rate = 0.1
        price_study.general_overhead = 0.1
        price_study_work.quantity = 3
        mk_price_study_work_item(
            ht=10000000, mode="ht", work_unit_quantity=4, unity="heures"
        )
        mk_price_study_work_item(
            supplier_ht=10000000,
            mode="supplier_ht",
            work_unit_quantity=4,
            unity="forfait main d'oeuvre",
        )
        price_study.sync_amounts(sync_down=True)
        totals = price_study.json_totals(csrf_request)
        assert "labor" in totals
        assert "material" in totals
        for key in ("flat_cost", "general_overhead", "margin", "total_ht"):
            assert totals["material"][key] == 0

        assert totals["labor"]["flat_cost"] == 1200
        assert totals["labor"]["general_overhead"] == 120
        assert totals["labor"]["margin"] == 146.66667
        assert totals["labor"]["total_ht"] == 2666.66667

    def test_amounts_by_tva(
        self,
        price_study,
        price_study_chapter,
        mk_price_study_product,
        tva20,
        tva10,
        mk_tva,
    ):
        negative_tva = mk_tva(value=-100)
        mk_price_study_product(tva=tva20, ht=10000000, chapter=price_study_chapter)
        mk_price_study_product(tva=tva10, ht=10000000, chapter=price_study_chapter)
        mk_price_study_product(tva=tva10, ht=10000000, chapter=price_study_chapter)
        mk_price_study_product(
            tva=negative_tva, ht=10000000, chapter=price_study_chapter
        )
        price_study.sync_amounts(sync_down=True)
        result = PriceStudyService.amounts_by_tva(price_study)
        assert result[tva10] == {"ht": 20000000, "tva": 2000000}
        assert result[tva20] == {"ht": 10000000, "tva": 2000000}
        assert result[negative_tva] == {"ht": 10000000, "tva": 0}

    def test_discounts_by_tva_amount_mode(
        self,
        price_study,
        mk_price_study_discount,
        tva20,
        tva10,
        mk_tva,
    ):
        negative_tva = mk_tva(value=-100)
        mk_price_study_discount(tva=tva20, amount=1000000, price_study=price_study)
        mk_price_study_discount(tva=tva10, amount=1000000, price_study=price_study)
        mk_price_study_discount(tva=tva10, amount=1000000, price_study=price_study)
        mk_price_study_discount(
            tva=negative_tva, amount=1000000, price_study=price_study
        )
        result = PriceStudyService.discounts_by_tva(price_study)
        assert result[tva10] == {"ht": -2000000, "tva": -200000}
        assert result[tva20] == {"ht": -1000000, "tva": -200000}
        assert result[negative_tva] == {"ht": -1000000, "tva": 0}

    def test_discounts_by_tva_percentage_mode(
        self,
        price_study,
        price_study_chapter,
        mk_price_study_product,
        mk_price_study_discount,
        tva20,
        tva10,
        mk_tva,
    ):
        negative_tva = mk_tva(value=-100)
        mk_price_study_product(tva=tva20, ht=10000000, chapter=price_study_chapter)
        mk_price_study_product(tva=tva10, ht=10000000, chapter=price_study_chapter)
        mk_price_study_product(tva=tva10, ht=10000000, chapter=price_study_chapter)
        mk_price_study_product(
            tva=negative_tva, ht=10000000, chapter=price_study_chapter
        )
        mk_price_study_discount(
            percentage=10, type_="percentage", price_study=price_study
        )
        price_study.sync_amounts(sync_down=True)
        result = PriceStudyService.discounts_by_tva(price_study)
        assert result[tva10] == {"ht": -2000000, "tva": -200000}
        assert result[tva20] == {"ht": -1000000, "tva": -200000}
        assert result[negative_tva] == {"ht": -1000000, "tva": 0}

    def test_totals(
        self,
        price_study,
        price_study_chapter,
        mk_price_study_product,
        mk_price_study_discount,
        tva20,
        tva10,
        mk_tva,
    ):
        negative_tva = mk_tva(value=-100)
        mk_price_study_product(tva=tva20, ht=10000000, chapter=price_study_chapter)
        mk_price_study_product(tva=tva10, ht=10000000, chapter=price_study_chapter)
        mk_price_study_product(tva=tva10, ht=10000000, chapter=price_study_chapter)
        mk_price_study_product(
            tva=negative_tva, ht=10000000, chapter=price_study_chapter
        )
        mk_price_study_discount(
            percentage=10, type_="percentage", price_study=price_study
        )
        price_study.sync_amounts(sync_down=True)
        before_discount = PriceStudyService.total_ht_before_discount(price_study)
        assert before_discount == 20000000 + 10000000 + 10000000
        discount = PriceStudyService.discount_ht(price_study)
        assert discount == -2000000 - 1000000 - 1000000
        total_ht = PriceStudyService.total_ht(price_study)
        assert total_ht == before_discount + discount
        total_tva_before_discount = PriceStudyService.total_tva_before_discount(
            price_study
        )
        assert total_tva_before_discount == 2000000 + 2000000
        discount_tva = PriceStudyService.discount_tva(price_study)
        assert discount_tva == -200000 - 200000
        total_tva = PriceStudyService.total_tva(price_study)
        assert total_tva == total_tva_before_discount + discount_tva
        total_ttc = PriceStudyService.total_ttc(price_study)
        assert total_ttc == total_tva + total_ht
        assert price_study.ht == total_ht

    def test_sync_with_task(
        self,
        estimation,
        mk_price_study_chapter,
        get_csrf_request_with_db,
        mk_price_study,
        mk_price_study_product,
        tva,
        product,
    ):
        request = get_csrf_request_with_db()
        estimation.line_groups = []
        request.dbsession.merge(estimation)
        request.dbsession.flush()
        study = mk_price_study(task=estimation)
        chapter = mk_price_study_chapter(
            description="Desc", title="Tit", order=1, price_study=study
        )
        mk_price_study_product(
            description="Price study product",
            mode="ht",
            ht=15000000,
            tva=tva,
            product=product,
            chapter=chapter,
            quantity=4,
        )
        study.sync_amounts(sync_down=True)
        PriceStudyService.sync_with_task(request, study)
        assert len(estimation.line_groups) == 1
        assert estimation.line_groups[0].description == "Desc"
        assert estimation.line_groups[0].title == "Tit"
        assert len(estimation.line_groups[0].lines) == 1
        line = estimation.line_groups[0].lines[0]
        assert line.description == "Price study product"
        assert line.tva == tva.value
        assert line.product == product
        assert line.quantity == 4
        assert line.cost == 15000000
        assert estimation.ht == PriceStudyService.total_ht(study)


class TestBasePriceStudyProductService:
    def test__ensure_tva(
        self,
        csrf_request_with_db_and_user,
        estimation,
        price_study,
        price_study_chapter,
        price_study_product,
        mk_price_study_product,
        mk_tva,
        mk_product,
    ):
        t = mk_tva(value=1950)
        mk_product(tva=t, internal=False)
        mk_price_study_product(tva=t, chapter=price_study_chapter)
        request = csrf_request_with_db_and_user
        estimation.line_groups = []
        request.dbsession.merge(estimation)
        request.dbsession.flush()
        price_study.sync_with_task(request)
        # On s'assure qu'on tste bien quelque chose
        assert price_study_product.tva_id is None
        BasePriceStudyProductService._ensure_tva(price_study_product)
        assert price_study_product.tva == t

    def test__ensure_tva_internal(
        self,
        csrf_request_with_db_and_user,
        estimation,
        price_study,
        price_study_chapter,
        price_study_product,
        mk_price_study_product,
        mk_tva,
        mk_product,
    ):
        t = mk_tva(value=1950)
        mk_product(tva=t, internal=True)
        t2 = mk_tva(value=1960, default=True)
        mk_product(tva=t2, internal=False)

        mk_price_study_product(tva=t, chapter=price_study_chapter)
        request = csrf_request_with_db_and_user
        estimation.line_groups = []
        estimation.internal = True
        request.dbsession.merge(estimation)
        request.dbsession.flush()
        price_study.sync_with_task(request)
        # On s'assure qu'on tste bien quelque chose
        assert price_study_product.tva_id is None
        BasePriceStudyProductService._ensure_tva(price_study_product)
        assert price_study_product.tva == t

    def test_sync_with_task(
        self,
        csrf_request_with_db_and_user,
        estimation,
        price_study,
        price_study_chapter,
        mk_price_study_product,
        tva,
        product,
        tva10,
    ):
        price_study_product = mk_price_study_product(
            description="descr",
            tva=tva,
            chapter=price_study_chapter,
            ht=100000000,
            mode="ht",
            quantity=5,
            unity="unity",
            product=product,
            order=6,
        )
        price_study_product.sync_amounts(propagate=False)
        taskline = BasePriceStudyProductService.sync_with_task(
            csrf_request_with_db_and_user, price_study_product, price_study_chapter
        )
        assert taskline.description == "descr"
        assert taskline.cost == 100000000
        assert taskline.tva == tva.value
        assert taskline.quantity == 5
        assert taskline.unity == "unity"
        assert taskline.product == product
        assert taskline.order == 6

        price_study_product.description = "new"
        price_study_product.tva = tva10

        taskline2 = BasePriceStudyProductService.sync_with_task(
            csrf_request_with_db_and_user, price_study_product, price_study_chapter
        )
        assert taskline2 is taskline
        assert taskline2.description == "new"
        assert taskline2.tva == tva10.value


class TestPriceStudyProductService:
    def test_flat_cost(self, price_study_product, mk_price_study_product):
        assert (
            amount(PriceStudyProductService.flat_cost(price_study_product), 2)
            == 1000000000
        )
        assert (
            PriceStudyProductService.flat_cost(
                mk_price_study_product(supplier_ht=None, mode="ht")
            )
            == 0
        )

    def test_cost_price(self, price_study_product, price_study):
        price_study.general_overhead = 0.1
        assert (
            amount(PriceStudyProductService.cost_price(price_study_product), 2)
            == 1100000000
        )

    def test_intermediate_price(self, price_study_product, price_study):
        price_study.general_overhead = 0.1
        assert (
            amount(PriceStudyProductService.intermediate_price(price_study_product), 2)
            == 1222222222
        )

    def test_unit_ht(self, dbsession, price_study_product, price_study, company):
        company.contribution = 10
        dbsession.merge(company)
        dbsession.flush()
        price_study.general_overhead = 0.1
        assert (
            amount(
                PriceStudyProductService.unit_ht(price_study_product),
                2,
            )
            == 1358024691
        )
        # Ref #1877
        company.contribution = 10.0
        dbsession.merge(company)
        dbsession.flush()
        assert (
            amount(
                PriceStudyProductService.unit_ht(price_study_product),
                2,
            )
            == 1358024691
        )


class TestPriceStudyWorkService:
    @pytest.fixture
    def my_price_study_work(
        self, company, price_study, mk_price_study_work_item, price_study_work, tva10
    ):
        price_study.general_overhead = 0.1
        price_study_work.margin_rate = 0.2
        price_study_work.tva = tva10
        price_study_work.quantity = 5
        company.contribution = 10

        mk_price_study_work_item(
            mode="supplier_ht",
            supplier_ht=10000000,
            work_unit_quantity=5,
        )
        mk_price_study_work_item(
            mode="supplier_ht",
            supplier_ht=10000000,
            work_unit_quantity=5,
        )
        mk_price_study_work_item(mode="ht", ht=10000000, work_unit_quantity=5)
        price_study_work.sync_amounts(propagate=False)
        return price_study_work

    @pytest.fixture
    def item_no_heritance(self, my_price_study_work, mk_price_study_work_item):
        item = mk_price_study_work_item(
            mode="ht",
            ht=10000000,
            work_unit_quantity=2,
            quantity_inherited=False,
            price_study_work=my_price_study_work,
        )
        my_price_study_work.sync_amounts(propagate=False)
        return item

    def test_flat_cost(self, my_price_study_work):
        assert PriceStudyWorkService.flat_cost(my_price_study_work) == 500000000

    def test_cost_price(self, my_price_study_work):
        assert PriceStudyWorkService.cost_price(my_price_study_work) == 550000000

    def test_intermediate_price(self, my_price_study_work):
        assert (
            PriceStudyWorkService.intermediate_price(my_price_study_work) == 687500000
        )

    def test_unit_ht(self, my_price_study_work):
        assert (
            int(PriceStudyWorkService.unit_ht(my_price_study_work)) == 202777777
        )  # 10000000 * 5 + 137500000 / 0.9

    def test_unit_ht_3348(self, my_price_study_work, item_no_heritance):
        # Ref #3348 : item avec une quantité non héritée n'est pas inclue
        # dans le unit_ht
        assert (
            int(PriceStudyWorkService.unit_ht(my_price_study_work)) == 206777777
        )  # 10000000 * 5 + 137500000 / 0.9  + 2*10000000 / 5

    def test_compute_total_ht(self, my_price_study_work, mk_price_study_work_item):
        assert (
            int(PriceStudyWorkService.compute_total_ht(my_price_study_work))
            == 1013888888
        )  # 202777777.7777778 * 5 -> 1013888888.888889

    def test_compute_total_ht_ref3348(self, my_price_study_work, item_no_heritance):
        # Ref #3348 : item avec une quantité non héritée est inclue dans le total_ht
        assert (
            int(PriceStudyWorkService.compute_total_ht(my_price_study_work))
            == 1033888888
        )  # 202777777.7777778 * 5 + 2*10000000 -> 1033888888.888889

    def test_ttc(self, my_price_study_work):
        assert (
            int(PriceStudyWorkService.ttc(my_price_study_work)) == 1115277777
        )  # 1013888888.88889 * 1.1 -> 1115277777.777778

    def test_ht_by_tva(self, my_price_study_work, tva10):
        assert (
            int(PriceStudyWorkService.ht_by_tva(my_price_study_work)[tva10])
            == 1013888888
        )

    def test_sync_amounts(
        self, my_price_study_work, price_study, mk_price_study_work_item
    ):
        PriceStudyWorkService.sync_amounts(my_price_study_work)
        assert int(price_study.ht) == 1013889000

        new_item = mk_price_study_work_item(
            mode="ht",
            ht=10000000,
            work_unit_quantity=12,
            price_study_work=my_price_study_work,
        )
        # Still default ones
        assert new_item.total_quantity == 1
        assert new_item.total_ht == 0
        assert new_item.work_unit_ht == 0
        # Syncing down
        my_price_study_work.sync_amounts(propagate=False)
        assert new_item.total_quantity == 60
        assert new_item.total_ht == 600000000
        assert new_item.work_unit_ht == 120000000

    def test_sync_with_task(
        self,
        csrf_request_with_db_and_user,
        estimation,
        price_study,
        item_no_heritance,
        price_study_chapter,
        my_price_study_work,
        product,
        tva10,
    ):
        my_price_study_work.product = product
        taskline = PriceStudyWorkService.sync_with_task(
            csrf_request_with_db_and_user, my_price_study_work, price_study_chapter
        )
        # ref https://framagit.org/endi/endi/-/issues/3491
        # ref https://framagit.org/endi/endi/-/issues/3348
        assert int(taskline.cost) == 1033888888
        assert taskline.tva == tva10.value
        assert taskline.quantity == 1
        assert taskline.product == product
