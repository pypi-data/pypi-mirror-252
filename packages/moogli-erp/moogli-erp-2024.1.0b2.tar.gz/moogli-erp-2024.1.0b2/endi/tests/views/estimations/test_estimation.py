import pytest
from endi.views.estimations.estimation import (
    EstimationAddView,
    estimation_geninv_view,
    EstimationDuplicateView,
)
from endi.views.company.routes import (
    COMPANY_ESTIMATION_ADD_ROUTE,
    COMPANY_ESTIMATIONS_ROUTE,
)
from endi.views.estimations.routes import API_ADD_ROUTE
from endi.models.task import Estimation


def test_task_add_view(config, get_csrf_request_with_db, company, phase):
    route = COMPANY_ESTIMATIONS_ROUTE
    config.add_route(route, route, traverse="/companies/{id}")
    request = get_csrf_request_with_db(
        context=company,
        current_route_name=COMPANY_ESTIMATION_ADD_ROUTE,
        current_route_path=API_ADD_ROUTE.format(id=company.id),
    )
    view = EstimationAddView(request)
    result = view()
    assert result["title"] == EstimationAddView.title
    assert result["js_app_options"]["form_config_url"] == (
        f"/api/v1/companies/{company.id}/estimations/add?form_config=1"
        f"&company_id={company.id}"
    )
    request.GET["project_id"] = 2
    request.GET["phase_id"] = 2
    request.GET["customer_id"] = 2
    view = EstimationAddView(request)
    result = view()

    assert result["js_app_options"]["form_config_url"] == (
        f"/api/v1/companies/{company.id}/estimations/"
        f"add?form_config=1&company_id={company.id}&customer_id=2&project_id=2"
    )
    request.GET["project_id"] = 25555
    request.GET["phase_id"] = phase.id
    view = EstimationAddView(request)
    result = view()

    assert result["js_app_options"]["form_config_url"] == (
        f"/api/v1/companies/{company.id}/estimations/add?form_config=1"
        f"&company_id={company.id}"
        f"&customer_id=2&project_id={phase.project_id}&phase_id={phase.id}"
    )


def test_geninv_view(config, get_csrf_request_with_db, full_estimation):
    config.add_route("/invoices/{id}", "/invoices/{id}")
    estimation_geninv_view(full_estimation, get_csrf_request_with_db())
    assert full_estimation.geninv
    assert len(full_estimation.invoices) > 0
    for inv in full_estimation.invoices:
        assert inv.business_id == full_estimation.business_id


class TestEstimationDuplicate:
    def duplicate_one(self, config, request, customer, project, full_estimation):
        config.add_route("/estimations/{id}", "/")
        params = {
            "customer_id": customer.id,
            "project_id": project.id,
            "business_type_id": full_estimation.business_type_id,
        }
        request.context = full_estimation
        view = EstimationDuplicateView(request)
        view.submit_success(params)

    def get_one(self):
        return Estimation.query().order_by(Estimation.id.desc()).first()

    def test_duplicate(
        self,
        config,
        get_csrf_request_with_db_and_user,
        mk_customer,
        mk_project,
        full_estimation,
    ):
        new_customer = mk_customer(name="newcustomer")
        new_project = mk_project(name="newproject", customers=[new_customer])
        request = get_csrf_request_with_db_and_user()
        self.duplicate_one(config, request, new_customer, new_project, full_estimation)
        estimation = self.get_one()
        assert estimation.type_ == "estimation"
        assert estimation.customer_id == new_customer.id
        assert estimation.project_id == new_project.id

    def test_duplicate_internal(
        self,
        config,
        get_csrf_request_with_db_and_user,
        mk_customer,
        mk_project,
        full_estimation,
        mk_tva,
        mk_product,
    ):
        new_tva = mk_tva(value=0, name="O%")
        new_product = mk_product(tva=new_tva, name="interne", internal=True)

        new_customer = mk_customer(name="newcustomer", type="internal")
        new_project = mk_project(name="newproject", customers=[new_customer])
        request = get_csrf_request_with_db_and_user()

        self.duplicate_one(config, request, new_customer, new_project, full_estimation)
        estimation = self.get_one()
        assert estimation.type_ == "internalestimation"
        assert estimation.customer_id == new_customer.id
        assert estimation.project_id == new_project.id
        for line in estimation.all_lines:
            assert line.tva == new_tva.value
            assert line.product_id == new_product.id
