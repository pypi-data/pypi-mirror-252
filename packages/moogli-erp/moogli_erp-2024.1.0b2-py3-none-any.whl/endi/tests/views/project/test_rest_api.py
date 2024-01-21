from endi.views.project.rest_api import ProjectRestView


def test_get_projects(
    company,
    dbsession,
    get_csrf_request_with_db,
    project,
):
    request = get_csrf_request_with_db()
    request.context = company
    view = ProjectRestView(request)
    result = view.collection_get()
    assert len(result) == 1
    assert result[0]["name"] == project.name


def test_get_projects_filters(
    company,
    customer,
    customer2,
    dbsession,
    get_csrf_request_with_db,
    project,
):
    request = get_csrf_request_with_db()
    request.context = company
    view = ProjectRestView(request)

    request.GET = {"customer_id": customer.id}
    assert len(view.collection_get()) == 1

    request.GET = {"customer_id": customer2.id}
    assert len(view.collection_get()) == 0

    request.GET = {"search": "PROJECT"}
    assert len(view.collection_get()) == 1

    request.GET = {"search": "NOEXIST"}
    assert len(view.collection_get()) == 0


def test_get_projects_other_company(
    company2,
    dbsession,
    get_csrf_request_with_db,
    project,
):
    request = get_csrf_request_with_db()
    request.context = company2
    view = ProjectRestView(request)
    result = view.collection_get()
    assert len(result) == 0
