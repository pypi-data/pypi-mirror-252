from datetime import date, datetime
from pyramid import testing
from endi.models import (
    workshop,
)

import pytest


@pytest.fixture
def workshop_action(dbsession):
    a = workshop.WorkshopAction(label="Info 1")
    dbsession.add(a)
    dbsession.flush()
    return a


@pytest.fixture
def mk_workshop(dbsession, workshop_action, company):
    def _mk_workshop(company_manager=company):
        appstruct = {
            "name": "Workshop",
            "description": "test desc",
            "company_manager": company_manager,
            "datetime": date.today(),
            "info1_id": workshop_action.id,
        }
        w = workshop.Workshop(**appstruct)

        start = datetime(2014, 0o6, 12, 8)
        stop = datetime(2014, 0o6, 12, 12)
        timeslot = workshop.Timeslot(
            name="matinée",
            start_time=start,
            end_time=stop,
        )
        w.timeslots.append(timeslot)
        dbsession.add(w)
        dbsession.flush()
        return w

    return _mk_workshop


@pytest.fixture
def workshop_model(mk_workshop):
    return mk_workshop()


def get_one():
    return workshop.Workshop.query().first()


def test_add_view(config, get_csrf_request_with_db_and_user, workshop_action):
    from endi.views.workshops.workshop import WorkshopAddView

    config.add_route("toto", "/toto")
    config.add_route("workshop", "/workshop/{id}")

    start = datetime(2014, 0o6, 12, 15)
    stop = datetime(2014, 0o6, 12, 18)

    appstruct = {
        "come_from": "/toto",
        "name": "test",
        "info1_id": workshop_action.id,
        "timeslots": [
            {
                "name": "timeslot",
                "start_time": start,
                "end_time": stop,
            }
        ],
    }
    view = WorkshopAddView(get_csrf_request_with_db_and_user())
    view.submit_success(appstruct)
    a = get_one()

    assert a.info1.label == "Info 1"
    assert a.timeslots[0].start_time == start
    assert a.timeslots[0].end_time == stop


def test_edit_view(workshop_model, config, get_csrf_request_with_db, workshop_action):
    from endi.views.workshops.workshop import WorkshopEditView

    req = get_csrf_request_with_db()
    req.context = workshop_model
    timeslot_id = req.context.timeslots[0].id
    start = datetime(2014, 0o6, 12, 15)
    stop = datetime(2014, 0o6, 12, 18)

    config.add_route("workshop", "/workshop/{id}")
    appstruct = {
        "come_from": "",
        "info2_id": workshop_action.id,
        "timeslots": [
            {
                "name": "Matinée",
                "id": timeslot_id,
                "start_time": req.context.timeslots[0].start_time,
                "end_time": req.context.timeslots[0].end_time,
            },
            {
                "id": None,
                "name": "timeslot",
                "start_time": start,
                "end_time": stop,
            },
        ],
    }
    view = WorkshopEditView(req)
    view.submit_success(appstruct)
    a = get_one()

    assert a.timeslots[0].name == "Matinée"
    assert a.timeslots[0].start_time == datetime(2014, 0o6, 12, 8)

    assert a.timeslots[1].name == "timeslot"
    assert a.info2.label == "Info 1"
    assert a.info1.label == "Info 1"


def test_workshop_view_only_view(
    user, workshop_model, config, get_csrf_request_with_db
):
    from endi.views.workshops.workshop import workshop_view

    config.add_route("workshop", "/workshop/{id}")
    request = get_csrf_request_with_db()
    config.set_security_policy(testing.DummySecurityPolicy(identity=user))
    result = workshop_view(workshop_model, request)
    assert result.status == "302 Found"
    assert result.location == "/workshop/{id}?action=edit".format(id=workshop_model.id)


def test_workshop_delete_view(workshop_model, config, get_csrf_request_with_db):
    from endi.views.workshops.workshop import workshop_delete_view

    config.add_route("workshops", "/workshops")
    request = get_csrf_request_with_db()
    request.referer = None
    result = workshop_delete_view(workshop_model, request)
    assert result.status == "302 Found"
    assert result.location == "/workshops"
    assert get_one() is None


def test_workshop_list_tools(
    config,
    get_csrf_request_with_db,
    internal_company,
    mk_workshop,
    company,
):
    from endi.views.workshops.lists import WorkshopListTools

    tools = WorkshopListTools()
    query = workshop.Workshop.query()

    # One workshop linked to regular company
    mk_workshop(company_manager=company)
    # One workshop linked to no company
    mk_workshop(company_manager=None)
    # One workshop linked to cae internal company
    mk_workshop(company_manager=internal_company)

    assert tools.filter_company_manager_or_cae(query, {}).count() == 3

    assert (
        tools.filter_company_manager_or_cae(
            query,
            {
                "company_manager": company.id,
            },
        ).count()
        == 1
    )

    assert (
        tools.filter_company_manager_or_cae(
            query,
            {
                "company_manager": -1,
            },
        ).count()
        == 2
    )


#    def test_timeslot_pdf_view(config, get_csrf_request_with_db):
#        config.add_subscriber(add_api, BeforeRender)
#        config.add_static_view("static", "endi:static")
#        context = self.addTimeslot()
#        request = get_csrf_request_with_db()
#        result = timeslot_pdf_view(context, request)
#        datestr = date.today().strftime("%e_%m_%Y")
#        assert ('Content-Disposition',
#                'attachment; filename="atelier_{0}_{1}.pdf"'.format(
#                    date, timeslot_id)
#               )
