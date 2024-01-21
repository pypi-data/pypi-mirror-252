"""
    tests endi.views.expense
"""
from endi.tests.tools import Dummy


def test_add_expense(
    config,
    dbsession,
    get_csrf_request_with_db,
    company,
    user,
):
    from endi.views.expenses.expense import ExpenseSheetAddView

    config.add_route("/expenses/{id}", "/{id}")
    request = get_csrf_request_with_db(
        post={"month": "10", "year": "2017", "title": "Titre NDD", "submit": "submit"}
    )
    request.context = company
    request.matchdict = {"uid": user.id}
    request.matched_route = Dummy(
        name="/company/{company_id}/{user_id}/expenses",
        company_id=company.id,
        user_id=user.id,
    )
    view = ExpenseSheetAddView(request)
    result = view.__call__()
    assert result.code == 302


def test_duplicate(
    config,
    dbsession,
    get_csrf_request_with_db,
    company,
    user,
    full_expense_sheet,
    mk_expense_type,
):
    from endi.views.expenses.expense import ExpenseSheetDuplicateView

    config.add_route("/expenses/{id}", "/{id}")
    request = get_csrf_request_with_db(
        post={
            "month": "10",
            "year": "2017",
            "title": "Copie de Titre NDD",
            "submit": "submit",
        }
    )
    # https://framagit.org/endi/endi/issues/774
    mk_expense_type(label="KM", code="KM", amount=0.184, year=2017)

    request.context = full_expense_sheet
    request.matched_route = Dummy(
        name="/expenses/{id}/duplicate",
        id=full_expense_sheet.id,
    )
    view = ExpenseSheetDuplicateView(request)
    result = view.__call__()
    assert result.location != "/{id}".format(id=full_expense_sheet.id)

    from endi.models.expense.sheet import ExpenseSheet

    id = int(result.location[1:])
    new_sheet = ExpenseSheet.get(id)
    assert new_sheet.month == 10
    assert new_sheet.year == 2017
    assert new_sheet.title == "Copie de Titre NDD"
    assert new_sheet.company_id == company.id
    assert new_sheet.user_id == user.id
    assert len(new_sheet.lines) == len(full_expense_sheet.lines)
    assert len(new_sheet.kmlines) == len(full_expense_sheet.kmlines)


def test_edit_sheet_infos(
    config,
    dbsession,
    get_csrf_request_with_db,
    company,
    user,
    full_expense_sheet,
):
    from endi.views.expenses.expense import ExpenseSheetEditInfosView

    SHEET_APPSTRUCT = {"month": 10, "year": 2017, "title": "Titre NDD"}

    config.add_route("/expenses/{id}", "/{id}")
    request = get_csrf_request_with_db(
        post=SHEET_APPSTRUCT.update({"submit": "submit"})
    )

    request.context = full_expense_sheet
    request.matched_route = Dummy(
        name="/expenses/{id}/edit",
        id=full_expense_sheet.id,
    )
    view = ExpenseSheetEditInfosView(request)
    appstruct = SHEET_APPSTRUCT.copy()
    appstruct["month"] = 5
    appstruct["title"] = "Nouveau titre NDD"
    view.submit_success(appstruct)
    assert request.context.month == 5
    assert request.context.year == 2017
    assert request.context.title == "Nouveau titre NDD"
    assert request.context.company_id == company.id
    assert request.context.user_id == user.id
