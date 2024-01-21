from pytest import fixture
from endi.views.task.utils import (
    get_default_tva,
    get_default_product_id,
    get_tvas,
    get_products,
)


@fixture
def default_tva(mk_tva):
    return mk_tva(value=2000, default=True, name="tva20")


def test_get_tvas(
    pyramid_request,
    internalinvoice,
    internal_product,
    tva10,
    default_tva,
    invoice,
    mk_product,
):
    pyramid_request.context = internalinvoice
    assert get_tvas(pyramid_request) == [internal_product.tva]
    pyramid_request.context = invoice
    tvas = get_tvas(pyramid_request)
    assert tvas == []

    mk_product(tva=tva10)
    mk_product(tva=default_tva)
    tvas = get_tvas(pyramid_request)
    for tva in [tva10, default_tva]:
        assert tva in tvas
    assert internal_product.tva not in tvas
    mk_product(tva=internal_product.tva, internal=False)
    tvas = get_tvas(pyramid_request)
    assert internal_product.tva in tvas


def test_get_products(
    pyramid_request,
    internalinvoice,
    internal_product,
    tva10,
    default_tva,
    invoice,
    mk_product,
):
    mk_product(tva=tva10)
    mk_product(tva=tva10)
    mk_product(tva=default_tva)
    mk_product(tva=default_tva)

    pyramid_request.context = internalinvoice
    assert get_products(pyramid_request) == [internal_product]
    mk_product(tva=internal_product.tva, internal=False)
    assert get_products(pyramid_request) == [internal_product]

    pyramid_request.context = invoice
    products = get_products(pyramid_request)
    assert internal_product not in products


def test_get_default_tva(
    dbsession,
    pyramid_request,
    default_tva,
    tva10,
    mk_estimation,
    task_line_group,
    mk_task_line,
):
    tvas = [tva10, default_tva]
    estimation = mk_estimation()
    pyramid_request.context = estimation
    assert get_default_tva(pyramid_request, tvas) == default_tva

    line = mk_task_line(tva=tva10.value, description="line", group=task_line_group)
    estimation.line_groups.append(task_line_group)
    estimation.all_lines.append(line)

    assert get_default_tva(pyramid_request, [tva10, default_tva]) == tva10


def test_get_default_tva_internal(
    pyramid_request,
    internal_product,
    mk_internalestimation,
    default_tva,
    tva10,
):
    estimation = mk_internalestimation()
    pyramid_request.context = estimation
    assert (
        get_default_tva(pyramid_request, get_tvas(pyramid_request))
        == internal_product.tva
    )


def test_get_default_product_id(
    pyramid_request,
    internal_product,
    internalinvoice,
    invoice,
    default_tva,
    tva10,
    mk_product,
):
    pyramid_request.context = internalinvoice
    assert (
        get_default_product_id(
            pyramid_request, get_products(pyramid_request), internal_product.tva
        )
        == internal_product.id
    )

    pyramid_request.context = invoice
    p1 = mk_product(tva=tva10)
    assert (
        get_default_product_id(pyramid_request, get_products(pyramid_request), tva10)
        == p1.id
    )
    mk_product(tva=tva10)
    assert (
        get_default_product_id(pyramid_request, get_products(pyramid_request), tva10)
        == ""
    )
