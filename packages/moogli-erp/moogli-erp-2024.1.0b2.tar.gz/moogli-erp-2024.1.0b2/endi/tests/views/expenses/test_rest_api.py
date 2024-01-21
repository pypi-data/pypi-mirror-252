# NOTE : fixture can be found in the associated conftest.py file
import datetime
import pytest
from pyramid import testing
from endi.tests.tools import Dummy


def test_get_sheet(dbsession, get_csrf_request_with_db, full_expense_sheet):
    from endi.views.expenses.rest_api import RestExpenseSheetView

    request = get_csrf_request_with_db(context=full_expense_sheet)
    view = RestExpenseSheetView(request)
    result = view.get()
    assert len(result.lines) == 2
    assert len(result.kmlines) == 1


def test_add_sheet(dbsession, get_csrf_request_with_db, user, company):
    from endi.views.expenses.rest_api import RestExpenseSheetView

    request = get_csrf_request_with_db(
        post={
            "month": 10,
            "year": 2016,
            "title": "Titre NDD",
        },
        context=company,
        user=user,
    )
    request.matched_route = Dummy(
        name="/company/{company_id}/{user_id}/expenses",
        company_id=company.id,
        user_id=user.id,
    )
    view = RestExpenseSheetView(request)
    result = view.post()
    assert result.month == 10
    assert result.title == "Titre NDD"
    assert result.user_id == user.id
    assert result.company_id == company.id


def test_add_sheet_fail(
    dbsession, get_csrf_request_with_db, full_expense_sheet, company, user
):
    from endi.utils.rest import RestError
    from endi.views.expenses.rest_api import RestExpenseSheetView

    request = get_csrf_request_with_db(
        post={
            "month": -1,
            "year": 2015,
        },
        context=company,
        user=user,
    )
    request.matched_route = Dummy(
        name="/company/{company_id}/{user_id}/expenses",
        company_id=company.id,
        user_id=user.id,
    )
    view = RestExpenseSheetView(request)
    with pytest.raises(RestError) as invalid_exc:
        view.post()

    assert invalid_exc.value.code == 400


def test_edit_sheet(get_csrf_request_with_db, full_expense_sheet, company):
    from endi.views.expenses.rest_api import RestExpenseSheetView

    request = get_csrf_request_with_db(
        post={
            "month": 8,
            "year": 2005,
            "title": "Titre NDD 2",
        },
        context=full_expense_sheet,
    )
    request.matched_route = Dummy(
        name="/expenses/{id}",
        id=full_expense_sheet.id,
    )
    view = RestExpenseSheetView(request)
    result = view.put()
    assert result.year == 2005
    assert result.month == 8
    assert result.title == "Titre NDD 2"


def test_add_line(
    dbsession,
    get_csrf_request_with_db,
    full_expense_sheet,
    mk_expense_type,
):
    typ = mk_expense_type(label="test")
    from endi.views.expenses.rest_api import RestExpenseLineView

    request = get_csrf_request_with_db(
        post={
            "description": "Test",
            "category": "1",
            "ht": "50",
            "tva": "10",
            "manual_ttc": "0",
            "type_id": typ.id,
        },
        context=full_expense_sheet,
    )
    view = RestExpenseLineView(request)
    line = view.post()

    assert line.ht == 5000
    assert line.tva == 1000
    assert line.category == "1"
    assert line.description == "Test"
    assert line.expense_type == typ


def test_add_line_tva_on_margin(
    dbsession,
    get_csrf_request_with_db,
    full_expense_sheet,
    expense_type_tva_on_margin,
):
    from endi.views.expenses.rest_api import RestExpenseLineView

    request = get_csrf_request_with_db(
        post={
            "description": "Test",
            "category": "1",
            "ht": "42",  # should be overwritten
            "tva": "42",  # idem
            "manual_ttc": "100",
            "type_id": expense_type_tva_on_margin.id,
        },
        context=full_expense_sheet,
    )
    view = RestExpenseLineView(request)
    line = view.post()

    assert line.ht == 8333.3
    assert line.tva == 1666.7


def test_edit_line(
    dbsession,
    get_csrf_request_with_db,
    expense_sheet,
    expense_line,
    business,
):
    from endi.views.expenses.rest_api import RestExpenseLineView

    expense_line.sheet = expense_sheet
    request = get_csrf_request_with_db(
        post={
            "description": "Test Modify",
            "category": "2",
            "ht": "55",
            "tva": "11",
            "business_id": business.id,
            "project_id": business.project.id,
            "customer_id": business.project.customers[0].id,
        },
        context=expense_line,
    )

    view = RestExpenseLineView(request)
    view.put()

    assert expense_line.ht == 5500
    assert expense_line.tva == 1100
    assert expense_line.category == "2"
    assert expense_line.business == business
    assert expense_line.project == business.project
    assert expense_line.customer == business.project.customers[0]
    assert expense_line.description == "Test Modify"


def test_add_kmline(
    dbsession,
    get_csrf_request_with_db,
    full_expense_sheet,
    mk_expense_type,
):
    from endi.views.expenses.rest_api import RestExpenseKmLineView

    typ = mk_expense_type(amount=0.184, year=full_expense_sheet.year)
    request = get_csrf_request_with_db(
        post={
            "description": "Test",
            "category": "1",
            "start": "Start point",
            "end": "End point",
            "km": "50",
            "type_id": typ.id,
        },
        context=full_expense_sheet,
    )
    view = RestExpenseKmLineView(request)
    line = view.post()

    assert line.km == 5000
    assert line.category == "1"
    assert line.description == "Test"
    assert line.start == "Start point"
    assert line.end == "End point"
    assert line.expense_type == typ
    assert line.ht == 920


def test_edit_kmline(
    dbsession,
    get_csrf_request_with_db,
    expense_sheet,
    expense_kmline,
):
    from endi.views.expenses.rest_api import RestExpenseKmLineView

    request = get_csrf_request_with_db(
        post={
            "description": "Test Modify",
            "category": "2",
            "km": "55",
        },
        context=expense_kmline,
    )
    view = RestExpenseKmLineView(request)
    view.put()

    assert expense_kmline.km == 5500
    assert expense_kmline.category == "2"
    assert expense_kmline.description == "Test Modify"
    assert expense_kmline.start == "Dijon"
    assert expense_kmline.ht == 6897  # 1.254 * 5500


def test_line_type_required(
    dbsession,
    get_csrf_request_with_db,
    full_expense_sheet,
):
    from endi.views.expenses.rest_api import RestExpenseKmLineView
    from endi.utils.rest import RestError

    request = get_csrf_request_with_db(
        post={
            "description": "Test",
            "category": "1",
            "start": "Start point",
            "end": "End point",
            "km": "50",
            "type_id": -1,
        },
        context=full_expense_sheet,
    )
    view = RestExpenseKmLineView(request)
    with pytest.raises(RestError) as exc:
        view.post()
    assert exc.value.code == 400


def test_bookmark_view(dbsession, get_csrf_request_with_db, mk_expense_type, user):
    from endi.models.services.user import UserPrefsService
    from endi.views.expenses.rest_api import RestBookMarkView

    typ = mk_expense_type(label="base")
    request = get_csrf_request_with_db(
        post={"type_id": typ.id, "tva": "20", "ht": "100", "description": "Bookmark"},
        user=user,
    )
    view = RestBookMarkView(request)
    view.post()
    bookmarks = UserPrefsService.get(request, "expense")["bookmarks"]
    bookmark = bookmarks[1]
    assert bookmark["ht"] == 100
    assert bookmark["tva"] == 20
    assert bookmark["description"] == "Bookmark"
    assert bookmark["type_id"] == typ.id
    assert bookmark["id"] == 1


def test_forbidden_sheet_status(
    config,
    user,
    dbsession,
    get_csrf_request_with_db,
    full_expense_sheet,
):
    from endi.utils.rest import RestError
    from endi.views.expenses.rest_api import RestExpenseSheetStatusView

    config.add_route("/expenses/{id}", "/{id}")
    config.set_security_policy(
        testing.DummySecurityPolicy(
            userid=user.login.login,
            identity=user,
            permissive=False,
        )
    )
    request = get_csrf_request_with_db(
        post={
            "submit": "valid",
            "comment": "Test status comment",
        },
        context=full_expense_sheet,
    )

    request.is_xhr = True

    view = RestExpenseSheetStatusView(request)
    with pytest.raises(RestError) as forbidden_exc:
        view.__call__()
    assert forbidden_exc.value.code == 403


def test_sheet_status_valid(
    config,
    dbsession,
    get_csrf_request_with_db,
    full_expense_sheet,
    user,
):

    from endi.models.config import Config
    from endi.models.expense.sheet import ExpenseSheet

    from endi.views.expenses.rest_api import RestExpenseSheetStatusView

    config.add_route("/expenses/{id}", "/{id}")

    request = get_csrf_request_with_db(
        post={
            "submit": "valid",
            "comment": "Test status comment",
        },
        context=full_expense_sheet,
        user=user,
    )
    request.is_xhr = True

    view = RestExpenseSheetStatusView(request)
    result = view.__call__()
    assert result == {"redirect": "/{0}".format(full_expense_sheet.id)}

    sheet = ExpenseSheet.get(full_expense_sheet.id)
    assert sheet.status == "valid"
    assert sheet.statuses[0].comment == "Test status comment"
    assert sheet.statuses[0].status == "valid"
    assert sheet.statuses[0].user_id == user.id
    assert sheet.statuses[0].datetime.date() == datetime.date.today()
    assert sheet.status_date.date() == datetime.date.today()


def test_sheet_justified(
    config,
    dbsession,
    get_csrf_request_with_db,
    full_expense_sheet,
    user,
):
    from endi.views.expenses.rest_api import (
        RestExpenseSheetJustifiedStatusView,
    )

    request = get_csrf_request_with_db(
        post={
            "submit": True,
            "comment": "Test status comment",
        },
        context=full_expense_sheet,
        user=user,
    )
    request.is_xhr = True

    view = RestExpenseSheetJustifiedStatusView(request)
    result = view.__call__()
    assert result["status"] == "success"
    assert result["datas"]["justified"] == True
    assert full_expense_sheet.justified
    assert full_expense_sheet.statuses[0].comment == "Test status comment"
    assert full_expense_sheet.statuses[0].user_id == user.id
    assert full_expense_sheet.statuses[0].status == "justified"
    assert full_expense_sheet.statuses[0].datetime.date() == datetime.date.today()

    request = get_csrf_request_with_db(
        post={
            "submit": False,
            "comment": "2nd Test status comment",
        },
        context=full_expense_sheet,
        user=user,
    )

    result = view.__call__()
    assert result["status"] == "success"
    assert result["datas"]["justified"] == False
    assert not full_expense_sheet.justified
    assert full_expense_sheet.statuses[1].comment == "2nd Test status comment"
    assert full_expense_sheet.statuses[1].user_id == user.id
    assert full_expense_sheet.statuses[0].status == "justified"
