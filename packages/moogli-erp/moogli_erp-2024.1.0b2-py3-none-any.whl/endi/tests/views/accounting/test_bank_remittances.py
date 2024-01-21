import pytest
import colander
from endi.views.accounting.routes import (
    BANK_REMITTANCE_ROUTE,
    BANK_REMITTANCE_ITEM_ROUTE,
)


def test_bank_remittances_view(config, get_csrf_request_with_db, user):
    from endi.views.accounting.bank_remittances import BankRemittanceListView

    config.add_route(BANK_REMITTANCE_ROUTE, BANK_REMITTANCE_ROUTE)
    request = get_csrf_request_with_db()
    request.matchdict = {"uid": user.id}
    view = BankRemittanceListView(request)
    result = view.__call__()
    assert isinstance(result, dict)


def test_bank_remittance_views(
    config,
    get_csrf_request_with_db,
    bank_remittance,
    user,
):
    from pyramid.httpexceptions import HTTPFound
    from endi.views.accounting.bank_remittances import (
        BankRemittanceView,
        BankRemittanceCloseView,
        BankRemittanceOpenView,
        BankRemittancePdfView,
    )

    config.add_route(
        BANK_REMITTANCE_ITEM_ROUTE,
        BANK_REMITTANCE_ITEM_ROUTE,
        traverse="/bank_remittances/{id}",
    )
    request = get_csrf_request_with_db()
    request.context = bank_remittance
    request.matchdict = {"uid": user.id}
    # Item view
    view = BankRemittanceView(request)
    result = view.__call__()
    assert isinstance(result, dict)
    # Close view (without POST['remittance_date'])
    view = BankRemittanceCloseView(request)
    with pytest.raises(colander.Invalid):
        result = view.__call__()
    # Close view (with POST['remittance_date'])
    request = get_csrf_request_with_db(post={"remittance_date": "2019-10-01"})
    request.referrer = "/bank_remittances/{}".format(bank_remittance.id)
    view = BankRemittanceCloseView(request)
    result = view.__call__()
    assert isinstance(result, HTTPFound)
    # Open view
    view = BankRemittanceOpenView(request)
    result = view.__call__()
    assert isinstance(result, HTTPFound)
    # PDF view
    result = BankRemittancePdfView(bank_remittance, request)
    assert result.status_code == 200
