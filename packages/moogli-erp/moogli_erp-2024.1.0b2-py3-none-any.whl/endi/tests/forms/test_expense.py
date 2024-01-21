import pytest
from pyramid import testing
from endi.tests.tools import Dummy


@pytest.fixture
def expensetype(dbsession):
    from endi.models.expense.types import ExpenseType

    type_ = ExpenseType(label="Restauration", code="CODE")

    dbsession.add(type_)
    dbsession.flush()
    return type_


@pytest.fixture
def expenseteltype(dbsession):
    from endi.models.expense.types import ExpenseTelType

    type_ = ExpenseTelType(label="Téléphone", code="TELE", percentage=50)

    dbsession.add(type_)
    dbsession.flush()
    return type_


@pytest.fixture
def expensekmtype(dbsession):
    from endi.models.expense.types import ExpenseKmType

    type_ = ExpenseKmType(
        label="voiture",
        year=2017,
        amount=1.55,
        code="CODEKM",
    )

    dbsession.add(type_)
    dbsession.flush()
    return type_


@pytest.fixture
def expense_sheet(dbsession, user, company):
    from endi.models.expense.sheet import ExpenseSheet

    sheet = ExpenseSheet(
        month=1, year=2017, title="Titre NDD", user_id=user.id, company_id=company.id
    )
    dbsession.add(sheet)
    dbsession.flush()
    return sheet


def test_add_edit_sheet_schema(
    dbsession, config, pyramid_request, expense_sheet, user, company
):
    import colander
    from endi.forms.expense import get_add_edit_sheet_schema

    schema = get_add_edit_sheet_schema()
    config.set_security_policy(testing.DummySecurityPolicy(identity=user))

    pyramid_request.context = company
    pyramid_request.matched_route = Dummy(
        name="/company/{company_id}/{user_id}/expenses",
        company_id=company.id,
        user_id=user.id,
    )
    schema1 = schema.bind(request=pyramid_request)
    pyramid_request.context = expense_sheet
    pyramid_request.matched_route = Dummy(
        name="/expenses/{id}/duplicate",
        id=expense_sheet.id,
    )
    schema2 = schema.bind(request=pyramid_request)
    pyramid_request.matched_route = Dummy(
        name="/expenses/{id}/edit",
        id=expense_sheet.id,
    )
    schema3 = schema.bind(request=pyramid_request)

    for s in (schema1, schema2, schema3):
        result = s.deserialize({"month": 2, "year": 2016, "title": "Titre NDD"})
        assert "month" in result
        assert result["title"] == "Titre NDD"
        with pytest.raises(colander.Invalid):
            s.deserialize({"month": 2, "title": "Titre NDD"})
        with pytest.raises(colander.Invalid):
            s.deserialize({"month": 22, "year": 2017})
        with pytest.raises(colander.Invalid):
            s.deserialize({"month": 2, "year": -1})
        with pytest.raises(colander.Invalid):
            s.deserialize({"month": -1, "year": 2017})


def test_add_edit_line_schema(dbsession, pyramid_request, expensetype, expense_sheet):
    import colander
    from endi.models.expense.sheet import (
        ExpenseLine,
    )
    from endi.forms.expense import get_add_edit_line_schema

    schema = get_add_edit_line_schema(ExpenseLine, expense_sheet)
    schema = schema.bind(request=pyramid_request)

    result = schema.deserialize(
        {
            "manual_ttc": "0",
            "ht": "15.52",
            "tva": "1.55",
            "type_id": expensetype.id,
        }
    )

    assert result["ht"] == 1552

    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                "manual_ttc": "0",
                "ht": "ab",
                "tva": "1.55",
                "type_id": expensetype.id,
            }
        )

    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                "manual_ttc": "0",
                "tva": "1.55",
                "type_id": expensetype.id,
            }
        )

    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                "manual_ttc": "0",
                "ht": "15.52",
                "type_id": expensetype.id,
            }
        )

    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                "manual_ttc": "0",
                "ht": "15.52",
                "tva": "1.55",
            }
        )


def test_add_edit_line_schema_bug_1025(
    dbsession,
    pyramid_request,
    expensetype,
    expenseteltype,
    expensekmtype,
    expense_sheet,
):
    import colander
    from endi.models.expense.sheet import (
        ExpenseLine,
    )
    from endi.forms.expense import get_add_edit_line_schema

    schema = get_add_edit_line_schema(ExpenseLine, expense_sheet)
    schema = schema.bind(request=pyramid_request)

    # Should not raise : cf https://framagit.org/endi/endi/issues/1025
    schema.deserialize(
        {
            "manual_ttc": "0",
            "ht": "15.52",
            "tva": "1.55",
            "type_id": expenseteltype.id,
        }
    )

    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                "manual_ttc": "0",
                "ht": "1",
                "tva": "1",
                "type_id": expensekmtype.id,
            }
        )


def test_add_edit_kmline_schema(
    dbsession,
    pyramid_request,
    expensetype,
    expensekmtype,
    expense_sheet,
):
    import colander
    from endi.models.expense.sheet import (
        ExpenseKmLine,
    )
    from endi.forms.expense import get_add_edit_line_schema

    pyramid_request.context = expense_sheet
    schema = get_add_edit_line_schema(ExpenseKmLine, expense_sheet)
    schema = schema.bind(request=pyramid_request)

    result = schema.deserialize(
        {
            "km": "2",
            "type_id": expensekmtype.id,
        }
    )

    assert result["km"] == 200

    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                "km": "2",
                "type_id": expensetype.id,
            }
        )

    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                "type_id": expensekmtype.id,
            }
        )

    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                "km": "2",
            }
        )

    expensekmtype.year = 1980
    dbsession.merge(expensekmtype)
    dbsession.flush()
    schema = get_add_edit_line_schema(ExpenseKmLine, expense_sheet)
    schema = schema.bind(request=pyramid_request)

    with pytest.raises(colander.Invalid):
        result = schema.deserialize(
            {
                "km": "2",
                "type_id": expensekmtype.id,
            }
        )
