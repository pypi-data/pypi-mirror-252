from endi.models.payments import PaymentMode
from endi.models.task import WorkUnit


def test_payment_mode_success(config, dbsession, get_csrf_request_with_db):
    from endi.views.admin.sale.forms.main import (
        PaymentModeAdminView,
        FORMS_URL,
    )

    config.add_route(FORMS_URL, "/")
    appstruct = {
        "datas": [
            {"label": "Chèque"},
            {"label": "Expèce"},
        ]
    }
    view = PaymentModeAdminView(get_csrf_request_with_db())
    view.submit_success(appstruct)
    assert dbsession.query(PaymentMode).count() == 2
    appstruct = {
        "datas": [
            {"label": "Chèque"},
        ]
    }
    view.submit_success(appstruct)
    assert dbsession.query(PaymentMode).count() == 1


def test_workunit_success(config, dbsession, get_csrf_request_with_db):
    from endi.views.admin.sale.forms.main import (
        WorkUnitAdminView,
        FORMS_URL,
    )

    config.add_route(FORMS_URL, "/")
    appstruct = {"datas": [{"label": "Semaines"}, {"label": "Jours"}]}
    view = WorkUnitAdminView(get_csrf_request_with_db())
    view.submit_success(appstruct)
    assert dbsession.query(WorkUnit).count() == 2
    appstruct = {
        "datas": [
            {"label": "Semaines"},
        ]
    }
    view.submit_success(appstruct)
    assert dbsession.query(WorkUnit).count() == 1
