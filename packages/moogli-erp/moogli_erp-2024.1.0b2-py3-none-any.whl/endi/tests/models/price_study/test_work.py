def test_work_compute(
    get_csrf_request_with_db, mk_price_study_work, mk_price_study_work_item
):
    work = mk_price_study_work(quantity=3.33, margin_rate=0.12)
    work.chapter.price_study.general_overhead = 0.11
    mk_price_study_work_item(
        supplier_ht=100000,
        work_unit_quantity=2,
        price_study_work=work,
        mode="supplier_ht",
    )

    mk_price_study_work_item(
        ht=100000, work_unit_quantity=2, price_study_work=work, mode="ht"
    )
    # work.items.append(workitem1)
    # work.items.append(workitem2)

    work.on_before_commit(get_csrf_request_with_db(), "add")

    assert work.flat_cost() == 666000
    assert int(work.unit_ht()) == 452272  # 452272.773
    assert int(work.compute_total_ht()) == 1506068  # 1506068,1818


def test_price_study_work_duplicate(mk_price_study_work, mk_price_study_work_item):
    work = mk_price_study_work(
        title="Titre",
        display_details=False,
    )
    mk_price_study_work_item(price_study_work=work, ht=1)
    mk_price_study_work_item(price_study_work=work, ht=1)
    mk_price_study_work_item(price_study_work=work, ht=1)
    mk_price_study_work_item(price_study_work=work, supplier_ht=1, mode="supplier_ht")
    dup = work.duplicate()
    assert dup.title == work.title
    assert len(dup.items) == 4

    assert dup.display_details is False

    dup = work.duplicate(force_ht=True)
    assert dup.items[-1].mode == "ht"
    assert dup.items[-1].supplier_ht == 0
