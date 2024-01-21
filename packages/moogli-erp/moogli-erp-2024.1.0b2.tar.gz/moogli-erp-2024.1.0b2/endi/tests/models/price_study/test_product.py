def test_product_compute(get_csrf_request_with_db, mk_price_study_product):
    req = get_csrf_request_with_db()
    product = mk_price_study_product(
        supplier_ht=100000,
        margin_rate=0.12,
        quantity=3.33,
        mode="supplier_ht",
    )
    product.chapter.price_study.general_overhead = 0.11

    assert product.flat_cost() == 100000
    assert int(product.cost_price()) == 111000
    assert int(product.intermediate_price()) == 126136
    assert int(product.unit_ht()) == 126136
    # In int computing : assert int(product.compute_total_ht()) == 420032
    assert int(product.compute_total_ht()) == 420034

    product.on_before_commit(req, "add")
    assert int(product.ht) == 126136
    assert int(product.total_ht) == 420034


def test_product_duplicate(mk_price_study_product):
    product = mk_price_study_product(
        supplier_ht=10000,
        mode="supplier_ht",
    )
    dup = product.duplicate()
    assert dup.supplier_ht == 10000
    assert dup.mode == "supplier_ht"
    dup = product.duplicate(force_ht=True)
    assert dup.supplier_ht == 0
    assert dup.mode == "ht"


def test_product_json_repr(mk_price_study_product):
    attrs = dict(
        (
            ("type_", "material"),
            ("margin_rate", 0.1),
            ("description", "Description"),
            ("unity", "mètre"),
            ("quantity", "5"),
            ("supplier_ht", 1500000),
            ("mode", "supplier_ht"),
        )
    )
    product = mk_price_study_product(**attrs)
    json_dict = product.__json__(None)
    attrs["supplier_ht"] = 15
    for key, value in attrs.items():
        assert json_dict[key] == value
