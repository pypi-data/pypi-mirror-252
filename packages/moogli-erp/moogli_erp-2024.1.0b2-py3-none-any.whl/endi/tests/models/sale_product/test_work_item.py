def test_work_item_get_company(
    mk_sale_product_work, mk_sale_product_work_item, company
):
    item = mk_sale_product_work_item(
        _ht=1000, _mode="ht", sale_product_work=mk_sale_product_work(company=company)
    )
    assert item.get_company() == company


def test_work_item_get_tva(mk_sale_product_work, mk_sale_product_work_item, tva):
    item = mk_sale_product_work_item(
        _ht=1000, _mode="ht", sale_product_work=mk_sale_product_work(tva=tva)
    )
    assert item.get_tva() == tva


def test_work_item_locked(
    dbsession,
    mk_sale_product_work,
    mk_sale_product_work_item,
    mk_sale_product,
    mk_product,
    mk_tva,
):
    sale_product_work = mk_sale_product_work()
    base_product = mk_sale_product(
        supplier_ht=1,
        ht=10,
        unity="mot",
        mode="supplier_ht",
    )
    tva = mk_tva(name="test", value=1000)
    mk_product(name="test1", tva=tva)
    item = mk_sale_product_work_item(
        locked=True,
        _supplier_ht=2,
        _ht=20,
        _unity="feuille",
        base_sale_product_id=base_product.id,
        sale_product_work_id=sale_product_work.id,
        _mode="ht",
    )
    assert item.supplier_ht == 1
    assert item.ht == 10
    assert item.unity == "mot"
    assert item.mode == "supplier_ht"

    # If not locked, we use the _ prefixed attributes
    item.locked = False
    assert item.supplier_ht == 2
    assert item.ht == 20
    assert item.unity == "feuille"
    assert item.mode == "ht"


def test_work_item_compute(
    dbsession,
    company,
    mk_sale_product_work,
    mk_sale_product_work_item,
    mk_sale_product,
    tva,
    product,
):
    company.general_overhead = 0.11
    company.margin_rate = 0.12
    sale_product_work = mk_sale_product_work(tva=tva, product=product)

    base_product = mk_sale_product(
        supplier_ht=100000,
        mode="supplier_ht",
        unity="mot",
    )
    assert base_product.ht == 0
    base_product.sync_amounts()
    assert int(base_product.ht) == 126136

    item = mk_sale_product_work_item(
        locked=True,
        quantity=2,
        base_sale_product_id=base_product.id,
        sale_product_work_id=sale_product_work.id,
        _mode="supplier_ht",
    )

    assert int(item.flat_cost()) == 200000
    assert int(item.flat_cost(unitary=True)) == 100000
    assert int(item.cost_price()) == 222000
    assert int(item.cost_price(unitary=True)) == 111000
    assert int(item.intermediate_price()) == 252272
    assert int(item.intermediate_price(unitary=True)) == 126136
    assert int(item.unit_ht()) == 126136
    assert int(item.compute_total_ht()) == 252272

    company.contribution = 10
    dbsession.merge(company)
    dbsession.flush()
    assert int(item.unit_ht()) == 140151
    company.contribution = 10.0
    dbsession.merge(company)
    dbsession.flush()
    # Ref #1877
    assert int(item.unit_ht()) == 140151

    item.sync_amounts()
    assert int(item.total_ht) == 280303
    assert int(item._ht) == 140151

    assert int(sale_product_work.flat_cost()) == 200000
    assert int(sale_product_work.ht) == 280303
    assert int(sale_product_work.ttc) == 336363
