def test_payment_add_view(
    config,
    get_csrf_request_with_db,
    user,
    full_expense_sheet,
    bank,
    mode,
):
    from endi.views.payment.expense import ExpensePaymentAddView
    from collections import OrderedDict

    config.add_route("/expenses/{id}", "/{id}")
    request = get_csrf_request_with_db(
        post=OrderedDict(
            [
                ("amount", str(125.4 + 120 + 36 / 2)),
                ("mode", mode.label),
                ("__start__", "date:mapping"),
                ("date", "2017-05-02"),
                ("__end__", "date:mapping"),
                ("bank_id", str(bank.id)),
                ("submit", "submit"),
            ]
        ),
        context=full_expense_sheet,
        user=user,
    )
    view = ExpensePaymentAddView(request)
    result = view.__call__()
    assert result.location == "/{id}".format(id=full_expense_sheet.id)
    assert full_expense_sheet.topay() == 0
    assert full_expense_sheet.paid_status == "resulted"
