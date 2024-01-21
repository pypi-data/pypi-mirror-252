def test_duplicate_base_price_study_product(
    mk_price_study_product, product, tva, company
):
    attrs = {
        "margin_rate": 0.12,
        "ht": 10000,
        "description": "Description",
        "product_id": product.id,
        "tva_id": tva.id,
        "unity": "mètre",
        "quantity": 5,
        "total_ht": 10000,
    }
    p = mk_price_study_product(**attrs)
    dup = p.duplicate()
    for key, val in attrs.items():
        assert getattr(dup, key) == val

    dup = p.duplicate(force_ht=True)
    assert getattr(dup, "margin_rate") == None

    company.margin_rate = 0.11
    dup = p.duplicate()
    assert dup.margin_rate == 0.11
    dup = p.duplicate(force_ht=True)
    assert dup.margin_rate == None


def test_sync_with_task_product(
    estimation,
    mk_price_study_chapter,
    get_csrf_request_with_db,
    mk_price_study_product,
    tva,
    product,
):
    request = get_csrf_request_with_db()
    estimation.line_groups = []
    request.dbsession.merge(estimation)
    chapter = mk_price_study_chapter(description="Desc", title="Tit", order=1)
    ps_product = mk_price_study_product(
        description="Price study product",
        mode="ht",
        ht=15000000,
        quantity=2,
        tva=tva,
        product=product,
        chapter=chapter,
    )
    ps_product.sync_amounts(propagate=False)
    line = ps_product.sync_with_task(request)
    assert line.cost == 15000000
    assert line.tva == tva.value
    assert line.product == product
    assert line.quantity == 2

    assert line.description == "Price study product"
    line2 = ps_product.sync_with_task(request)
    assert line == line2
