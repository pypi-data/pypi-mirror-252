def test_global_expense_list(
    config,
    pyramid_request,
    user,
    dbsession,
    full_expense_sheet,
    get_csrf_request_with_db,
):
    """
    Fix #1989
    """
    from endi.views.expenses.lists import ExpenseList
    from endi.tests.tools import Dummy

    config.add_route(
        "/expenses/{id}/addpayment",
        "/expenses/{id:\d+}/addpayment",
        traverse="/expenses/{id}",
    )
    request = get_csrf_request_with_db(
        current_route_name="expenses",
        current_route_path="/expenses",
    )
    request.popups = {}
    request.context = Dummy

    view = ExpenseList(request)
    result = view.__call__()

    # Just to check we have something, and it did not crash…
    assert isinstance(result, dict)
