def test_json_repr(mk_price_study):
    study = mk_price_study(general_overhead=0.2)
    dict_repr = study.__json__(None)
    assert dict_repr["general_overhead"] == 0.2


def test_duplicate(
    mk_price_study, mk_price_study_chapter, mk_price_study_discount, company
):
    study = mk_price_study(general_overhead=0.2)
    mk_price_study_chapter(price_study=study)
    mk_price_study_discount(price_study=study)
    mk_price_study_chapter(price_study=study)
    mk_price_study_discount(price_study=study)
    dup = study.duplicate()
    assert dup.general_overhead == 0.2

    company.general_overhead = 0.3
    dup = study.duplicate()
    assert len(dup.chapters) == 2
    assert len(dup.discounts) == 2
    assert dup.general_overhead == 0.3
