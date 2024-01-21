import pytest
import colander


def test_tva_value_validator(tva):
    from endi.forms.admin.sale.tva import get_tva_value_validator

    validator = get_tva_value_validator(None)
    with pytest.raises(colander.Invalid):
        validator(None, tva.value)

    validator = get_tva_value_validator(tva)
    validator(None, tva.value)


def test_has_default_tva_validator(mk_tva):
    from endi.forms.admin.sale.tva import has_tva_default_validator

    with pytest.raises(colander.Invalid):
        has_tva_default_validator(None, False)
    has_tva_default_validator(colander.SchemaNode, True)
    mk_tva(value=2000, default=True, name="2000")
    has_tva_default_validator(colander.SchemaNode, False)


def test_internal_product_validator(mk_tva, mk_product):
    from endi.forms.admin.sale.tva import deferred_internal_validator
    from endi.tests.tools import Dummy

    req = Dummy(context=None)

    validator = deferred_internal_validator(colander.SchemaNode, kw=dict(request=req))
    tva = mk_tva(value=2000, name="1000")
    mk_product(tva=tva, name="product", internal=True)
    mynode = colander.SchemaNode(typ=colander.String())
    with pytest.raises(colander.Invalid):
        validator(mynode, True)

    req = Dummy(context=tva)
    validator = deferred_internal_validator(colander.SchemaNode, kw=dict(request=req))
    mynode = colander.SchemaNode(typ=colander.String())
    validator(mynode, True)
