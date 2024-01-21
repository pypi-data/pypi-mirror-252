# Compute
def test_work_item_compute(
    get_csrf_request_with_db, mk_price_study_work_item, mk_price_study_work, tva, mk_tva
):
    work = mk_price_study_work(quantity=3.33, tva=tva, margin_rate=0.12)
    work.chapter.price_study.general_overhead = 0.11

    work_item = mk_price_study_work_item(
        supplier_ht=100000,
        work_unit_quantity=2,
        total_quantity=6.66,
        price_study_work=work,
        mode="supplier_ht",
    )

    work_item.on_before_commit(get_csrf_request_with_db(), "add")
    assert work_item.flat_cost(unitary=True, work_level=False) == 100000
    assert work_item.flat_cost(unitary=True, work_level=True) == 200000
    assert work_item.flat_cost(unitary=False) == 666000

    assert int(work_item.cost_price(unitary=True)) == 111000
    assert int(work_item.cost_price(unitary=False)) == 739260

    assert int(work_item.intermediate_price(unitary=True)) == 126136
    assert int(work_item.intermediate_price(unitary=False)) == 840068

    assert int(work_item.unit_ht()) == 126136
    assert int(work_item.compute_work_unit_ht()) == 252272
    assert int(work_item.compute_total_ht()) == 840068

    # tva à 20% (fixture tva par défaut)
    assert int(work_item.compute_total_tva()) == 168013
    # Valeur imprécise, les arrondis se font au niveau de la facture
    assert int(work_item.ttc()) == 1008081

    new_tva = mk_tva(name="tva 2", value="1000")
    work.tva = new_tva

    # La tva est héritée
    assert int(work_item.compute_total_tva()) == 84006
    # Valeur imprécise, les arrondis se font au niveau de la facture
    assert int(work_item.ttc()) == 924075


def test_work_item_sync_quantities(mk_price_study_work_item, mk_price_study_work):
    work = mk_price_study_work(quantity=3.33)

    work_item = mk_price_study_work_item(work_unit_quantity=2, price_study_work=work)

    work_item.quantity_inherited = False
    work_item.sync_quantities()
    assert work_item.total_quantity == 2

    work_item.quantity_inherited = True
    work_item.sync_quantities()
    assert work_item.total_quantity == 6.66


# Duplicate
def test_work_item_duplicate(mk_price_study_work_item):
    attrs = {
        "description": "description",
        "total_ht": 10000,
        "supplier_ht": 1000,
        "ht": 100000,
        "unity": "mètre",
        "work_unit_quantity": 5,
        "total_quantity": 15,
        "quantity_inherited": True,
        "work_unit_ht": 1000,
        "mode": "supplier_ht",
    }
    item = mk_price_study_work_item(**attrs)

    dup = item.duplicate()
    for key, value in attrs.items():
        assert getattr(dup, key) == value

    dup = item.duplicate(force_ht=True)
    assert dup.supplier_ht == 0
    assert dup.mode == "ht"


def test_json_repr(mk_price_study_work_item):
    attrs = {
        "supplier_ht": 15000000,
        "ht": 40000000,
        "work_unit_ht": 20000000,
        "unity": "mètre",
        "work_unit_quantity": 2,
        "total_quantity": 10,
        "description": "Description",
        "mode": "supplier_ht",
    }
    work_item = mk_price_study_work_item(**attrs)
    json_dict = work_item.__json__(None)
    expected_attrs = attrs.copy()
    expected_attrs["supplier_ht"] = 150
    expected_attrs["ht"] = 400
    expected_attrs["work_unit_ht"] = 200

    for key, value in expected_attrs.items():
        assert json_dict[key] == value
