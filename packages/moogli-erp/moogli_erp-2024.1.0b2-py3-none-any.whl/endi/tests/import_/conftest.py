import pytest


@pytest.fixture
def mk_sale_product_appstruct():
    def _mk_sale_product_appstruct(**kwargs):
        d = {
            "archived": False,
            # "category": None,
            "description": "",
            "ht": 0,
            "id": 42,
            "label": "Label",
            "margin_rate": 0.0,
            "mode": "ht",
            "notes": None,
            "product": {
                "compte_cg": "122",
                "label": "product",
                "name": "product",
                "tva": {
                    "default": True,
                    "label": "tva 20%",
                    "name": "tva 20%",
                    "value": 2000,
                },
            },
            "ref": None,
            "stock_operations": [],
            # "supplier": None,
            "supplier_ht": 100000,
            "supplier_ref": None,
            "supplier_unity_amount": None,
            "ttc": 0,
            "tva": {
                "default": True,
                "label": "tva 20%",
                "name": "tva 20%",
                "value": 2000,
            },
            "type_": "sale_product_material",
            "unity": "",
        }
        d.update(kwargs)
        return d

    return _mk_sale_product_appstruct


@pytest.fixture
def sale_product_appstruct(mk_sale_product_appstruct):
    return mk_sale_product_appstruct()


@pytest.fixture
def work_sale_product_appstruct(mk_sale_product_appstruct):
    return mk_sale_product_appstruct(
        type_="sale_product_work",
        id=55,
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
                "_unity": None,
            },
            {
                "base_sale_product_id": 43000,
                "description": "C",
                "_ht": None,
                "locked": True,
                "_mode": "ht",
                "quantity": 1,
                "_supplier_ht": None,
                "total_ht": "0",
                "type_": "material",
                "_unity": None,
            },
        ],
    )
