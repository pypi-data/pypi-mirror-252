import pytest


@pytest.fixture
def supplier(mk_supplier):
    return mk_supplier(company_name="Fournisseur1")


@pytest.fixture
def supplier2(mk_supplier, company2):
    return mk_supplier(company_name="Fournisseur2", company=company2)


@pytest.fixture
def purchase_type(mk_expense_type):
    return mk_expense_type(
        "Achat",
        code="Compte cg",
    )


@pytest.fixture
def sale_product_category(dbsession):
    from endi.models.sale_product.category import SaleProductCategory

    category = SaleProductCategory(title="Catégorie")
    dbsession.add(category)
    dbsession.flush()
    return category


@pytest.fixture
def sale_product(
    dbsession,
    tva,
    product,
    company,
    sale_product_category,
):
    from endi.models.sale_product.sale_product import SaleProductMaterial

    product = SaleProductMaterial(
        label="Parpaing",
        ht="50",
        tva=tva,
        product=product,
        company=company,
        category=sale_product_category,
    )
    dbsession.add(product)
    dbsession.flush()
    return product


def test_get_sale_product_add_edit_schema(
    supplier,
    supplier2,
    purchase_type,
    sale_product_category,
    sale_product,
    pyramid_request,
    company,
    tva,
):
    import colander
    from endi.forms.sale_product.sale_product import (
        get_sale_product_add_edit_schema,
    )
    from endi.models.sale_product.base import BaseSaleProduct

    req = pyramid_request
    req.context = company

    schema = get_sale_product_add_edit_schema(BaseSaleProduct)
    schema = schema.bind(request=req)

    result = schema.deserialize(
        {
            "label": "Test label",
            "tva_id": tva.id,
            "ht": "15.52",
            "supplier_id": supplier.id,
            "type_": "sale_product_material",
            "supplier_ht": "12",
        }
    )

    assert result["ht"] == 1552000
    assert result["supplier_ht"] == 1200000

    # type_
    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                "label": "Test label",
                "tva_id": tva.id,
                "ht": "15.52",
                "supplier_id": supplier.id,
                "type_": "wrong_type",
            }
        )
    # tva_
    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                "label": "Test label",
                "ht": "15.52",
                "supplier_id": supplier.id,
                "type_": "sale_product_material",
                "tva_id": 175,
            }
        )

    # company supplier
    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                "label": "Test label",
                "tva_id": tva.id,
                "ht": "15.52",
                "type_": "sale_product_material",
                "supplier_id": supplier2.id,
            }
        )
