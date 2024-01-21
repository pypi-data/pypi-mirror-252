import pytest

from endi.views.project.routes import (
    PROJECT_ITEM_ROUTE,
    PROJECT_ITEM_PHASE_ROUTE,
    PROJECT_ITEM_ESTIMATION_ROUTE,
    PROJECT_ITEM_INVOICE_ROUTE,
    PROJECT_ITEM_BUSINESS_ROUTE,
)


@pytest.fixture
def customer2(dbsession, company):
    from endi.models.third_party.customer import Customer

    customer = Customer(
        name="customer2",
        code="CUST",
        lastname="Lastname",
        firstname="Firstname",
        address="1th street",
        zip_code="01234",
        city="City",
    )
    customer.company = company
    dbsession.add(customer)
    dbsession.flush()
    return customer


def getone():
    from endi.models.project import Project

    return Project.query().first()


def test_entry_point_view(login, user, project, get_csrf_request_with_db, config):
    from endi.views.project.project import (
        ProjectEntryPointView,
        ProjectPhaseListView,
    )
    from endi.views.project.estimation import (
        ProjectEstimationListView,
    )
    from endi.views.project.invoice import (
        ProjectInvoiceListView,
    )
    from endi.views.project.business import (
        ProjectBusinessListView,
    )

    for route in (
        PROJECT_ITEM_ROUTE,
        PROJECT_ITEM_PHASE_ROUTE,
        PROJECT_ITEM_ESTIMATION_ROUTE,
        PROJECT_ITEM_INVOICE_ROUTE,
        PROJECT_ITEM_BUSINESS_ROUTE,
    ):
        config.add_route(route, route)

    req = get_csrf_request_with_db(user=user)
    res = ProjectEntryPointView(project, req)()
    assert res.location == PROJECT_ITEM_PHASE_ROUTE.format(id=project.id)

    for view, route in (
        (ProjectPhaseListView, PROJECT_ITEM_PHASE_ROUTE),
        (ProjectEstimationListView, PROJECT_ITEM_ESTIMATION_ROUTE),
        (ProjectInvoiceListView, PROJECT_ITEM_INVOICE_ROUTE),
        (ProjectBusinessListView, PROJECT_ITEM_BUSINESS_ROUTE),
    ):
        url = route.format(id=project.id)
        req = get_csrf_request_with_db(current_route_path=url)
        req.context = project
        req.user = user
        view(project, req).__call__()
        res = ProjectEntryPointView(project, req)()
        assert res.location == url


def test_project_add(company, get_csrf_request_with_db, config, customer, project_type):
    from endi.views.project.project import ProjectAddView

    config.add_route(PROJECT_ITEM_ROUTE, PROJECT_ITEM_ROUTE)
    req = get_csrf_request_with_db()
    req.context = company
    view = ProjectAddView(req)

    appstruct = {
        "name": "Projéct&$",
        "customers": [customer.id],
        "project_type_id": project_type.id,
    }
    result = view.submit_success(appstruct)

    project = getone()
    assert result.status == "302 Found"
    assert result.location == "/projects/{id}?action=addstep2".format(id=project.id)

    assert project.name == "Projéct&$"
    assert project.company_id == company.id
    assert len(project.customers) == 1


def test_project_add_step2(
    project,
    get_csrf_request_with_db,
    config,
    mk_business_type,
    default_business_type,
):
    other_business_type = mk_business_type(name="other")
    from endi.views.project.project import ProjectAddStep2View

    config.add_route(PROJECT_ITEM_ROUTE, PROJECT_ITEM_ROUTE)
    req = get_csrf_request_with_db()
    req.context = project
    view = ProjectAddStep2View(req)
    appstruct = {
        "code": "CODE",
        "description": "Description",
        "business_types": [other_business_type.id],
    }

    result = view.submit_success(appstruct)

    assert result.status == "302 Found"
    assert result.location == "/projects/{id}".format(id=project.id)

    assert project.code == "CODE"
    assert project.description == "Description"
    assert project.business_types == [other_business_type]


def test_edit(config, get_csrf_request_with_db, project, customer2):
    from endi.views.project.project import ProjectEditView

    config.add_route(PROJECT_ITEM_ROUTE, PROJECT_ITEM_ROUTE)

    req = get_csrf_request_with_db()
    req.context = project
    definition = "Super project, should e ^dmeù*"
    appstruct = {
        "name": "Projéct&$",
        "code": "ABDC",
        "customers": [customer2.id],
        "definition": definition,
        "business_types": [],
    }
    view = ProjectEditView(req)
    view.submit_success(appstruct)

    project = getone()
    assert project.definition == definition
    assert project.business_types == []
    assert project.customers == [customer2]


def test_archive(project, get_csrf_request_with_db):
    from endi.views.project.project import project_archive

    req = get_csrf_request_with_db()
    req.referer = "test"
    req.context = project
    project_archive(req)
    assert getone().archived


def test_delete(project, get_csrf_request_with_db):
    from endi.views.project.project import project_delete

    req = get_csrf_request_with_db()
    req.referer = "test"
    project = getone()
    req.context = project
    project_delete(req)
    assert getone() is None
