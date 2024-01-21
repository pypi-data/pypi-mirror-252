from pyramid.httpexceptions import HTTPFound


def test_task_metadata_view(
    dbsession, full_estimation, config, get_csrf_request_with_db
):
    from endi.views.task.views import TaskSetMetadatasView

    original_customer_id = full_estimation.customer_id
    appstruct = {
        "name": "new task name",
        "customer_id": original_customer_id + 1,
        "project_id": full_estimation.project_id,
        "phase_id": full_estimation.phase_id,
    }
    request = get_csrf_request_with_db(post=appstruct, context=full_estimation)
    config.add_route("/estimations/{id}", "/estimations/{id}")
    view = TaskSetMetadatasView(full_estimation, request)
    result = view.submit_success(appstruct)
    assert isinstance(result, HTTPFound)
    assert full_estimation.name == "new task name"
    assert full_estimation.customer_id == original_customer_id


def test_task_metadata_view_fix_1873(
    dbsession, full_estimation, config, get_csrf_request_with_db, business
):
    from endi.tests.tools import Dummy
    from endi.views.task.views import TaskSetMetadatasView

    full_estimation.business = business
    business.is_void = lambda: False
    appstruct = {"name": "new task name"}

    request = get_csrf_request_with_db(post=appstruct, context=full_estimation)
    config.add_route("/estimations/{id}", "/estimations/{id}")

    view = TaskSetMetadatasView(full_estimation, request)
    result = view.submit_success(appstruct)
    assert isinstance(result, HTTPFound)
    assert full_estimation.name == "new task name"


def test_task_metadata_set_estimatinon_project_id_view(
    dbsession,
    full_estimation,
    config,
    get_csrf_request_with_db,
    mk_project,
    full_invoice,
    business,
):
    new_project = mk_project(name="project 2")
    full_estimation.business = business
    business.invoices.append(full_invoice)

    from endi.views.task.views import TaskSetMetadatasView

    appstruct = {
        "name": "new task name",
        "customer_id": full_estimation.customer_id,
        "project_id": new_project.id,
    }
    request = get_csrf_request_with_db(post=appstruct, context=full_estimation)
    config.add_route("/estimations/{id}", "/estimations/{id}")
    view = TaskSetMetadatasView(full_estimation, request)
    result = view.submit_success(appstruct)
    assert isinstance(result, HTTPFound)
    assert full_estimation.project_id == new_project.id
    assert business.project_id == new_project.id
    assert full_invoice.project_id == new_project.id


def test_task_metadata_set_invoice_project_id_view(
    dbsession,
    full_estimation,
    config,
    get_csrf_request_with_db,
    mk_project,
    full_invoice,
    business,
):
    new_project = mk_project(name="project 2")
    full_invoice.business = business
    business.estimations.append(full_estimation)

    from endi.views.task.views import TaskSetMetadatasView

    appstruct = {
        "name": "new task name",
        "customer_id": full_invoice.customer_id,
        "project_id": new_project.id,
    }
    request = get_csrf_request_with_db(post=appstruct, context=full_invoice)
    config.add_route("/invoices/{id}", "/invoices/{id}")
    view = TaskSetMetadatasView(full_invoice, request)
    result = view.submit_success(appstruct)
    assert isinstance(result, HTTPFound)
    assert full_estimation.project_id == new_project.id
    assert business.project_id == new_project.id
    assert full_invoice.project_id == new_project.id
