import pytest
import colander


@pytest.fixture
def income_measure_type_category(income_statement_measure_type_categories):
    return income_statement_measure_type_categories[0]  # "Produits"


@pytest.fixture
def income_measure_type(dbsession, income_measure_type_category):
    from endi.models.accounting.income_statement_measures import (
        IncomeStatementMeasureType,
    )

    typ = IncomeStatementMeasureType(
        label="Label 1",
        category_id=income_measure_type_category.id,
        account_prefix="701",
    )
    dbsession.add(typ)
    dbsession.flush()
    typ.category = income_measure_type_category
    return typ


def test_label_validator(pyramid_request, income_measure_type):
    from endi.forms.accounting import deferred_label_validator

    pyramid_request.context = None
    label_validator = deferred_label_validator(None, kw={"request": pyramid_request})

    with pytest.raises(colander.Invalid):
        label_validator(None, "Test : Test")

    with pytest.raises(colander.Invalid):
        label_validator(None, "Test ! Test")

    with pytest.raises(colander.Invalid):
        label_validator(None, "Label 1")

    with pytest.raises(colander.Invalid):
        label_validator(None, "Produits")

    assert label_validator(None, "Test") == None


def test_label_validator_with_context(
    pyramid_request, income_measure_type, income_measure_type_category
):
    from endi.forms.accounting import deferred_label_validator

    pyramid_request.context = income_measure_type
    label_validator = deferred_label_validator(None, kw={"request": pyramid_request})

    with pytest.raises(colander.Invalid):
        label_validator(None, "Test : Test")

    with pytest.raises(colander.Invalid):
        label_validator(None, "Test ! Test")
    with pytest.raises(colander.Invalid):
        assert label_validator(None, "Produits") is None

    assert label_validator(None, "Label 1") is None
    assert label_validator(None, "Test") == None


def test_complex_total_validator():
    from endi.forms.accounting import complex_total_validator

    for value in (
        "{Salaires]",
        "[Salaires}",
        "{Salaires : Tout}",
        "100 * {Test ! }",
    ):
        with pytest.raises(colander.Invalid):
            complex_total_validator(None, value)


def test_accounting_operation_schema():
    import datetime
    from endi.forms.accounting import get_add_edit_accounting_operation_schema

    schema = get_add_edit_accounting_operation_schema()

    values = {
        "analytical_account": "9HERNAN",
        "general_account": "411200",
        "date": "20210101",
        "label": (
            "HR RĂ\x84â\x80\x9aĂ\x82ÂŻĂ\x83â\x80\x9aĂ\x82ÂżĂ\x83â\x80\x9a"
            "Ă\x82Âœnovation de BĂ\x84â\x80\x9aĂ\x82ÂŻĂ\x83â\x80\x9a"
            "Ă\x82ÂżĂ\x83â\x80\x9aĂ\x82Âœtiment ancie"  # 83 chars
        ),
        "debit": "0",
        "credit": "5574.35",
        "balance": "-5574.35",
    }
    assert schema.deserialize(values) == {
        "analytical_account": "9HERNAN",
        "general_account": "411200",
        "date": datetime.date(2021, 1, 1),
        "label": (
            "HR RĂ\x84â\x80\x9aĂ\x82ÂŻĂ\x83â\x80\x9aĂ\x82ÂżĂ\x83â\x80\x9a"
            "Ă\x82Âœnovation de BĂ\x84â\x80\x9aĂ\x82ÂŻĂ\x83â\x80\x9a"
            "Ă\x82ÂżĂ\x83â\x80\x9aĂ\x82Âœtiment an"  # 80 chars
        ),
        "debit": 0,
        "credit": 5574.35,
        "balance": -5574.35,
    }
