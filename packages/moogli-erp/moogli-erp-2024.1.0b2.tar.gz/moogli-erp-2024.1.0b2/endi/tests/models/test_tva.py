import pytest
from endi.models.tva import Tva, Product


def test_tva_get_default(mk_tva):
    mk_tva(value=10000, name="tva")
    assert Tva.get_default() is None

    tva2 = mk_tva(value=2000, default=True, name="tva2")
    assert Tva.get_default() == tva2


def test_tva_unique_value(mk_tva):
    tva = mk_tva(value=1000, name="tva")
    assert not Tva.unique_value(1000)
    assert Tva.unique_value(3000)
    assert Tva.unique_value(1000, tva_id=tva.id)


def test_tva_get_internal(mk_tva, mk_product):
    tva = mk_tva(value=1000, name="tva")
    mk_tva(value=0, name="tva2")
    assert Tva.get_internal() is None

    mk_product(internal=True, name="test", tva=tva)
    assert Tva.get_internal() == tva


def test_tva_by_value(mk_tva):
    tva = mk_tva(value=1000, name="tva")
    with pytest.raises(Exception):
        Tva.by_value(15)
    assert Tva.by_value(1000) == tva


def test_product_get_internal(mk_tva, mk_product):
    assert Product.get_internal() == []
    tva = mk_tva(value=0, name="tva")
    mk_product(tva=tva, name="test")
    assert Product.get_internal() == []

    product2 = mk_product(tva=tva, internal=True, name="test2")
    assert Product.get_internal() == [product2]


def test_product_first_by_tva_value(mk_tva, mk_product):
    assert Product.first_by_tva_value(15) is None

    tva = mk_tva(value=10, name="tva")
    product = mk_product(tva=tva, name="test")

    assert Product.first_by_tva_value(10) == product.id

    internal_product = mk_product(tva=tva, name="test internal", internal=True)
    assert Product.first_by_tva_value(10) == product.id
    assert Product.first_by_tva_value(10, True) == internal_product.id
