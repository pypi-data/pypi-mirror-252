import datetime

import colander

from endi.export.sale_product import (
    BaseSaleProductSchema,
    SaleProductTrainingSchema,
    SaleProductWorkSchema,
)
from endi.import_.sale_product import CatalogInstancesAdapter


def test_base_product_import(company, dbsession, sale_product, sale_product_appstruct):
    # Create one sale product and zero categories
    adapter = CatalogInstancesAdapter(company)
    new = adapter.adapt(BaseSaleProductSchema().objectify(sale_product_appstruct))
    dbsession.add(new)

    assert len(dbsession.dirty) == 0
    assert len(dbsession.deleted) == 0
    assert len(dbsession.new) == 1
    assert new in dbsession.new

    dbsession.flush()

    dbsession.refresh(new)
    dbsession.refresh(sale_product)
    new_json = new.__json__(None)
    old_json = sale_product.__json__(None)

    # Remove keys that are not supposed to be similar
    for k in ("id", "updated_at"):
        del new_json[k]
        del old_json[k]

    assert new_json == old_json
    assert len(adapter.warnings) == 0


def test_base_product_import_creates_category_on_the_fly(
    company,
    dbsession,
    sale_product,
    mk_sale_product_appstruct,
    sale_product_category,
):
    """On-the-fly category creation"""
    appstruct = mk_sale_product_appstruct(
        category={
            "id": 44444,
            "title": "My cat",
            "description": "cd",
        }
    )
    adapter = CatalogInstancesAdapter(company)
    new = adapter.adapt(BaseSaleProductSchema().objectify(appstruct))
    new_cat = list(adapter.pending_cache.categories.values())[0]
    dbsession.add(new)
    assert len(dbsession.dirty) == 0
    assert len(dbsession.deleted) == 0
    assert len(dbsession.new) == 2
    assert new in dbsession.new
    assert new.category in dbsession.new

    dbsession.flush()

    dbsession.refresh(new_cat)
    assert new_cat.company == company
    assert new_cat.id != 44444
    assert new_cat.id != sale_product_category.id
    assert new_cat.title == "My cat"
    assert new_cat.description == "cd"

    dbsession.refresh(new)
    assert new.category == new_cat


def test_base_product_import_reuse_existing_category(
    company,
    dbsession,
    sale_product,
    mk_sale_product_appstruct,
    sale_product_category,
):
    """Case 2 : re-use a category existing in DB )"""

    appstruct = mk_sale_product_appstruct(
        category={
            "id": 1234,
            "title": "My Cat Title",  # Same as fixture
            "description": "cd",
        }
    )

    adapter = CatalogInstancesAdapter(company)
    new = adapter.adapt(BaseSaleProductSchema().objectify(appstruct))

    dbsession.add(new)

    # Check that we did not trigger any change to existing objects
    assert len(dbsession.dirty) == 0
    assert len(dbsession.deleted) == 0
    assert len(dbsession.new) == 1
    assert new in dbsession.new

    dbsession.flush()

    # We re-used the previously created category
    assert new.category_id == sale_product_category.id


def test_base_product_import_new_category_deduplication(
    company,
    dbsession,
    sale_product,
    mk_sale_product_appstruct,
    sale_product_category,
):
    """
    Two products on the same category, only one category is created
    (pending cache is used to avoid duplication.
    """
    category_appstruct = {
        "id": 55555,
        "title": "My non-existing cat",
        "description": "cd",
    }
    appstruct1 = mk_sale_product_appstruct(
        description="Ga", category=category_appstruct
    )
    appstruct2 = mk_sale_product_appstruct(
        description="Bu", category=category_appstruct
    )
    adapter = CatalogInstancesAdapter(company)
    new = adapter.adapt(BaseSaleProductSchema().objectify(appstruct1))
    new2 = adapter.adapt(BaseSaleProductSchema().objectify(appstruct2))
    dbsession.add_all([new, new2])

    assert len(dbsession.dirty) == 0
    assert len(dbsession.deleted) == 0
    assert len(dbsession.new) == 3
    assert new in dbsession.new
    assert new2 in dbsession.new
    assert new.category in dbsession.new

    dbsession.flush()
    dbsession.refresh(new)
    dbsession.refresh(new2)

    assert new.category.id is not None


def test_base_product_import_typing(company, dbsession, sale_product_appstruct):
    from endi.models.sale_product import SaleProductMaterial
    from endi.models.sale_product import BaseSaleProduct

    input_instances = [BaseSaleProductSchema().objectify(sale_product_appstruct)]
    adapter = CatalogInstancesAdapter(company)
    dbsession.add_all(adapter.adapt(i) for i in input_instances)
    dbsession.flush()

    assert (
        dbsession.query(BaseSaleProduct).with_polymorphic([SaleProductMaterial]).count()
        == 1
    )
    assert SaleProductMaterial.query().count() == 1


def test_base_product_import_nulled_fields(
    company, dbsession, mk_sale_product_appstruct
):
    """Checks that if no match is found on relationships, they are nulled, and a warning is issued"""
    from endi.models.expense.types import ExpenseType
    from endi.models.sale_product import BaseSaleProduct
    from endi.models.task import WorkUnit
    from endi.models.third_party import Supplier
    from endi.models.tva import Product, Tva

    appstruct = mk_sale_product_appstruct(
        unit="kg",
        supplier={"label": "Fournisseur Test"},
        purchase_type={"label": "Fournitures diverses"},
    )
    adapter = CatalogInstancesAdapter(company)
    dbsession.add(adapter.adapt(BaseSaleProductSchema().objectify(appstruct)))
    dbsession.flush()
    assert Tva.query().count() == 0
    assert Product.query().count() == 0
    assert WorkUnit.query().count() == 0
    assert Supplier.query().count() == 0
    assert ExpenseType.query().count() == 0

    assert BaseSaleProduct.query().one().label == "Label"

    assert len(adapter.warnings) == 4


def test_import_stock_variations(
    company,
    dbsession,
    mk_sale_product_appstruct,
):

    sp_as = mk_sale_product_appstruct(
        stock_operations=[
            {
                "date": "2023-11-01T17:38:37.124425",
                "stock_variation": "10",
            },
            {
                "date": "2023-11-01T17:38:37.124425",
                "stock_variation": "-1",
            },
        ]
    )
    adapter = CatalogInstancesAdapter(company)
    instance = adapter.adapt(BaseSaleProductSchema().objectify(sp_as))
    dbsession.add(instance)

    assert len(dbsession.new) == 3  # 2x SaleProductStockOperation, 1x BaseSaleProduct
    dbsession.flush()
    dbsession.refresh(instance)

    assert len(instance.stock_operations) == 2
    assert instance.get_current_stock() == 9
    assert instance.stock_operations[0].date == datetime.date(2023, 11, 1)


def test_work_product_import(
    company,
    dbsession,
    mk_sale_product_appstruct,
    work_sale_product_appstruct,
):
    # Those are the two IDs Referenced in the WorkItem
    p42000_appstruct = mk_sale_product_appstruct(id=42000, label="Peinture")
    p43000_appstruct = mk_sale_product_appstruct(id=43000, label="Solvant")

    adapter = CatalogInstancesAdapter(company)

    p42000 = adapter.adapt(BaseSaleProductSchema().objectify(p42000_appstruct))
    p43000 = adapter.adapt(BaseSaleProductSchema().objectify(p43000_appstruct))
    p55 = adapter.adapt(SaleProductWorkSchema().objectify(work_sale_product_appstruct))

    dbsession.add_all([p42000, p43000, p55])

    # 2 BaseSaleProduct, 1 WorkProduct, 2 WorkItem
    assert len(dbsession.new) == 5

    dbsession.flush()
    dbsession.refresh(p55)
    dbsession.refresh(p42000)
    dbsession.refresh(p43000)

    # 42000 and 430000 are the IDs from remote export
    # No reason we get the same here, the DB picked the ID in its own sequence
    assert p42000.id != 42000
    assert p43000.id != 43000

    assert len(p55.items) == 2

    assert p55.items[0].description == "B"
    assert p55.items[0].base_sale_product.label == "Peinture"
    assert p55.items[0]._unity is None
    assert p55.items[0].base_sale_product.id == p42000.id

    assert p55.items[1].description == "C"
    assert p55.items[1].base_sale_product.label == "Solvant"
    assert p55.items[1]._unity is None
    assert p55.items[1].base_sale_product.id == p43000.id


def test_work_product_import_unit_handling(
    company,
    dbsession,
    mk_sale_product_appstruct,
    mk_work_unit,
):
    wp_appstruct = mk_sale_product_appstruct(
        type_="sale_product_work",
        items=[
            {
                "base_sale_product_id": 42000,
                "description": "B",
                "_ht": None,
                "locked": True,
                "_mode": "ht",
                "quantity": 1,
                "_supplier_ht": None,
                "total_ht": 0,
                "type_": "material",
                "_unity": "litre",
            },
        ],
        product=colander.null,
        tva=colander.null,
    )
    del wp_appstruct["product"]
    del wp_appstruct["tva"]
    p42000_appstruct = mk_sale_product_appstruct(
        id=42000,
        label="Peinture",
        product=colander.null,
        tva=colander.null,
    )
    del p42000_appstruct["product"]
    del p42000_appstruct["tva"]

    adapter = CatalogInstancesAdapter(company)

    adapter.adapt(BaseSaleProductSchema().objectify(p42000_appstruct))
    wp = adapter.adapt(SaleProductWorkSchema().objectify(wp_appstruct))
    assert wp.items[0]._unity is None
    assert len(adapter.warnings) == 1

    # Pre-existing unit
    mk_work_unit(label="litre")
    adapter = CatalogInstancesAdapter(company)

    p = adapter.adapt(BaseSaleProductSchema().objectify(p42000_appstruct))
    wp = adapter.adapt(SaleProductWorkSchema().objectify(wp_appstruct))
    assert wp.items[0]._unity == "litre"
    assert len(adapter.warnings) == 0

    dbsession.add_all([wp, p])
    dbsession.flush()


def test_training_sale_product_import(
    company,
    dbsession,
    mk_sale_product_appstruct,
    mk_training_type_option,
):
    mk_training_type_option(label="existant")

    training_appstruct = mk_sale_product_appstruct(
        type_="sale_product_training",
        types=[
            {"label": "existant"},
            {"label": "TT non existant"},
        ],
    )
    adapter = CatalogInstancesAdapter(company)

    training_p = adapter.adapt(
        SaleProductTrainingSchema().objectify(training_appstruct)
    )

    dbsession.add(training_p)

    assert len(dbsession.new) == 1
    assert len(dbsession.dirty) == 0
    assert len(dbsession.deleted) == 0
    dbsession.flush()
    dbsession.refresh(training_p)

    # 1 existant -> kept
    assert len(training_p.types) == 1
    #  the other non-existant -> warning
    assert len([i for i in adapter.warnings if "TT non existant" in i]) == 1
