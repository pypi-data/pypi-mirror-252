def test_duplicate(mk_price_study_discount, tva):
    attrs = dict(
        tva_id=tva.id,
        amount=10000,
        percentage=10,
        description="Description",
        type_="material",
        order=5,
    )
    discount = mk_price_study_discount(**attrs)
    dup = discount.duplicate()
    for key, value in attrs.items():
        assert getattr(dup, key) == value


def test_sync_with_task(
    get_csrf_request_with_db,
    estimation,
    mk_price_study,
    mk_price_study_discount,
    tva10,
    tva20,
):
    request = get_csrf_request_with_db()
    price_study = mk_price_study(task=estimation)
    price_study._amount_cache = {tva10: {"ht": 1000000}, tva20: {"ht": 2000000}}
    ps_discount = mk_price_study_discount(
        description="Test", percentage=5, type_="percentage", price_study=price_study
    )
    discounts = ps_discount.sync_with_task(request, price_study)
    assert len(discounts) == 2
    assert discounts[0].task_id == estimation.id
    assert sum(d.amount for d in discounts) == 150000
