import datetime
import pytest
from pyramid import testing
from endi.views.project.routes import PROJECT_ITEM_ESTIMATION_ROUTE
from endi.views.estimations.routes import API_ADD_ROUTE, ESTIMATION_ITEM_ROUTE
from endi.views.estimations.rest_api import EstimationAddRestView
from endi.models.task import Estimation


class TestEstimationAddRestView:
    @pytest.fixture
    def view_result(
        self,
        get_csrf_request_with_db,
        company,
        project,
        customer,
        default_business_type,
    ):
        def callview(params={}):
            props = {}
            props.update(
                {
                    "name": "Devis 1",
                    "company_id": str(company.id),
                    "customer_id": str(customer.id),
                    "project_id": str(project.id),
                    "business_type_id": str(default_business_type.id),
                }
            )
            props.update(params)
            project.__name__ = "project"
            request = get_csrf_request_with_db(
                post=props,
                current_route_path=API_ADD_ROUTE,
                context=company,
            )

            view = EstimationAddRestView(company, request)
            view.post()
            return Estimation.query().all()[-1]

        return callview

    def test_add(self, view_result, company, project, customer):
        estimation = view_result()
        assert isinstance(estimation, Estimation)
        assert len(estimation.payment_lines) == 1
        assert estimation.project == project
        assert estimation.company == company
        assert estimation.customer == customer
        assert not estimation.has_price_study()

    def test_add_restore_previous_true(self, plugin_active, view_result, mk_estimation):
        mk_estimation(display_ttc=1, display_units=1)
        estimation = view_result()
        if not plugin_active("sap"):
            assert estimation.display_ttc == 1
            assert estimation.display_units == 1

    def test_add_restore_previous_false(
        self, plugin_active, view_result, mk_estimation
    ):
        mk_estimation(display_ttc=0, display_units=0)
        estimation = view_result()
        if not plugin_active("sap"):
            assert estimation.display_ttc == 0
            assert estimation.display_units == 0
        else:
            assert estimation.display_ttc
            assert estimation.display_units

    def test_add_price_study(self, view_result, mk_project, mk_project_type):
        tp = mk_project_type(
            "test", include_price_study=True, price_study_mode="optionnal"
        )
        p = mk_project(project_type=tp)
        estimation = view_result(
            {
                "project_id": str(p.id),
            }
        )
        assert not estimation.has_price_study()
        tp.price_study_mode = "default"
        estimation = view_result({"project_id": str(p.id)})
        assert estimation.has_price_study()
        tp.price_study_mode = "mandatory"
        estimation = view_result({"project_id": str(p.id)})
        assert estimation.has_price_study()


def test_status_change_view_invalid_error(
    config, get_csrf_request_with_db, estimation, user
):
    config.add_route(PROJECT_ITEM_ESTIMATION_ROUTE, PROJECT_ITEM_ESTIMATION_ROUTE)
    from endi.utils.rest import RestError
    from endi.views.estimations.rest_api import EstimationStatusRestView

    request = get_csrf_request_with_db(post={"submit": "valid"})
    request.context = estimation
    config.set_security_policy(testing.DummySecurityPolicy(identity=user))
    request.is_xhr = True

    view = EstimationStatusRestView(request)

    with pytest.raises(RestError) as invalid_exc:
        view.__call__()
    assert invalid_exc.value.code == 400
    assert estimation.status == "draft"


def test_status_change_view_forbidden_error(
    config, get_csrf_request_with_db, full_estimation, user
):
    config.add_route(PROJECT_ITEM_ESTIMATION_ROUTE, PROJECT_ITEM_ESTIMATION_ROUTE)
    config.set_security_policy(
        testing.DummySecurityPolicy(
            userid=user.login.login, identity=user, permissive=False
        )
    )
    from endi.utils.rest import RestError
    from endi.views.estimations.rest_api import EstimationStatusRestView

    request = get_csrf_request_with_db(post={"submit": "valid"})
    request.context = full_estimation
    request.is_xhr = True

    view = EstimationStatusRestView(request)

    with pytest.raises(RestError) as forbidden_exc:
        view.__call__()
    assert forbidden_exc.value.code == 403
    assert full_estimation.status == "draft"


def test_status_change_view(config, get_csrf_request_with_db, full_estimation, user):
    config.add_route(ESTIMATION_ITEM_ROUTE, ESTIMATION_ITEM_ROUTE)

    from endi.views.estimations.rest_api import EstimationStatusRestView

    request = get_csrf_request_with_db(
        post={"submit": "valid", "comment": "Test comment"},
        context=full_estimation,
        user=user,
    )
    from pyramid_layout.layout import LayoutManager

    request.is_xhr = True

    view = EstimationStatusRestView(request)
    result = view.__call__()
    assert result == {"redirect": ESTIMATION_ITEM_ROUTE.format(id=full_estimation.id)}
    assert full_estimation.status == "valid"
    assert full_estimation.statuses[-1].comment == "Test comment"
    assert full_estimation.statuses[-1].status == "valid"


def test_signed_status_change_wrong(
    config, get_csrf_request_with_db, full_estimation, user
):
    from endi.utils.rest import RestError
    from endi.views.estimations.rest_api import (
        EstimationSignedStatusRestView,
    )

    request = get_csrf_request_with_db(post={"submit": "wrong"}, user=user)
    request.context = full_estimation
    request.is_xhr = True

    view = EstimationSignedStatusRestView(request)
    with pytest.raises(RestError) as invalid_exc:
        view.__call__()
    assert invalid_exc.value.code == 400


def test_signed_status_change_forbidden(
    config, get_csrf_request_with_db, full_estimation, user
):
    config.set_security_policy(
        testing.DummySecurityPolicy(
            userid=user.login.login, identity=user, permissive=False
        )
    )
    from endi.utils.rest import RestError
    from endi.views.estimations.rest_api import (
        EstimationSignedStatusRestView,
    )

    request = get_csrf_request_with_db(post={"submit": "signed"})
    request.context = full_estimation
    request.is_xhr = True

    view = EstimationSignedStatusRestView(request)
    with pytest.raises(RestError) as forbidden_exc:
        view.__call__()
    assert forbidden_exc.value.code == 403


def test_signed_status_change(get_csrf_request_with_db, full_estimation, user):
    from endi.views.estimations.rest_api import (
        EstimationSignedStatusRestView,
    )

    request = get_csrf_request_with_db(
        post={"submit": "aborted"}, user=user, context=full_estimation
    )

    request.is_xhr = True

    view = EstimationSignedStatusRestView(request)
    result = view.__call__()
    assert result["datas"] == {"signed_status": "aborted"}


def test_add_task_group(get_csrf_request_with_db, full_estimation, user):
    from endi.views.estimations.rest_api import TaskLineGroupRestView

    request = get_csrf_request_with_db(
        post={"title": "Title", "description": "Description"},
        user=user,
        context=full_estimation,
    )

    view = TaskLineGroupRestView(request)
    result = view.post()
    assert result.task_id == full_estimation.id
    assert result.title == "Title"
    assert result.description == "Description"


def test_edit_task_group(
    get_csrf_request_with_db, user, full_estimation, task_line_group
):
    from endi.views.estimations.rest_api import TaskLineGroupRestView

    task_line_group.task = full_estimation
    request = get_csrf_request_with_db(
        post={"title": "New Title"}, user=user, context=task_line_group
    )

    view = TaskLineGroupRestView(request)
    result = view.put()
    assert result.title == "New Title"
    assert result.description == "Group description"


def test_add_task_line(
    get_csrf_request_with_db,
    task_line_group,
    user,
    unity,
    tva,
    product,
    full_estimation,
):
    from endi.views.estimations.rest_api import TaskLineRestView

    request = get_csrf_request_with_db(
        post={
            "description": "Description",
            "cost": "150.12345",
            "tva": str(tva.value / 100),
            "quantity": 2,
            "unity": unity.label,
        },
        user=user,
        context=task_line_group,
    )

    view = TaskLineRestView(request)
    result = view.post()
    assert result.group_id == task_line_group.id
    assert result.description == "Description"
    assert result.cost == 15012345
    assert result.tva == tva.value
    assert result.quantity == 2
    assert result.unity == unity.label
    assert result.product_id == product.id

    # test invalid entry
    from endi.utils.rest import RestError

    request = get_csrf_request_with_db(
        post={
            "description": "Description",
            "tva": str(tva.value / 100),
            "quantity": 2,
        },
        user=user,
        context=task_line_group,
    )

    view = TaskLineRestView(request)

    with pytest.raises(RestError):
        view.post()


def test_edit_task_line(
    get_csrf_request_with_db,
    user,
    task_line,
    unity,
    product,
    full_estimation,
):
    from endi.views.estimations.rest_api import TaskLineRestView

    request = get_csrf_request_with_db(
        post={"cost": "160"},
        user=user,
        context=task_line,
    )

    view = TaskLineRestView(request)
    result = view.put()
    assert result.cost == 16000000
    assert result.description == "Default description"
    assert result.quantity == 1
    assert result.unity == unity.label
    assert result.product_id == product.id


def test_add_discount_line(get_csrf_request_with_db, full_estimation, user, unity, tva):
    from endi.views.estimations.rest_api import DiscountLineRestView

    request = get_csrf_request_with_db(
        post={
            "description": "Description",
            "amount": "150.12345",
            "tva": str(tva.value / 100),
        },
        user=user,
        context=full_estimation,
    )

    view = DiscountLineRestView(request)
    result = view.post()
    assert result.task_id == full_estimation.id
    assert result.description == "Description"
    assert result.amount == 15012345
    assert result.tva == tva.value


def test_add_discount_percent_line(
    get_csrf_request_with_db, full_estimation, user, unity, tva
):
    from endi.views.estimations.rest_api import DiscountLineRestView

    request = get_csrf_request_with_db(
        post={
            "description": "Description",
            "percentage": 10,
        },
        user=user,
        context=full_estimation,
    )

    parts = full_estimation.tva_ht_parts()
    tva, ht = next(iter(parts.items()))
    view = DiscountLineRestView(request)
    result = view.post_percent_discount_view()
    assert len(result) == 1
    assert result[0].task_id == full_estimation.id
    assert result[0].description == "Description"
    assert result[0].amount == int(ht / 10)
    assert result[0].tva == tva


def test_add_discount_percent_line_ttc_issue_2070(
    get_csrf_request_with_db, full_estimation, user, unity, tva
):
    from endi.views.estimations.rest_api import DiscountLineRestView

    request = get_csrf_request_with_db(
        post={
            "description": "Description",
            "percentage": 10,
        },
        user=user,
        context=full_estimation,
    )
    full_estimation.mode = "ttc"

    parts = full_estimation.tva_ttc_parts()
    tva, ttc = next(iter(parts.items()))
    view = DiscountLineRestView(request)
    result = view.post_percent_discount_view()
    assert len(result) == 1
    assert result[0].task_id == full_estimation.id
    assert result[0].description == "Description"
    assert result[0].amount == int(ttc / 10)
    assert result[0].tva == tva


def test_edit_discount_line(
    get_csrf_request_with_db,
    user,
    discount_line,
    unity,
    product,
    full_estimation,
):
    from endi.views.estimations.rest_api import DiscountLineRestView

    request = get_csrf_request_with_db(
        post={"amount": "160"}, user=user, context=discount_line
    )

    view = DiscountLineRestView(request)
    result = view.put()
    assert result.amount == 16000000
    assert result.description == "Discount"


def test_add_payment_line(dbsession, get_csrf_request_with_db, full_estimation, user):
    from endi.views.estimations.rest_api import PaymentLineRestView

    full_estimation.manualDeliverables = 1
    dbsession.merge(full_estimation)
    dbsession.flush()

    request = get_csrf_request_with_db(
        post={
            "description": "Description",
            "amount": "150.12345",
            "date": "2017-06-01",
        },
        user=user,
        context=full_estimation,
    )

    view = PaymentLineRestView(request)
    result = view.post()
    assert result.task_id == full_estimation.id
    assert result.description == "Description"
    assert result.amount == 15012345
    assert result.date == datetime.date(2017, 6, 1)


def test_edit_payment_line_amount(
    dbsession,
    get_csrf_request_with_db,
    user,
    payment_line,
    full_estimation,
    unity,
    product,
):
    from endi.views.estimations.rest_api import PaymentLineRestView

    full_estimation.manualDeliverables = 1
    dbsession.merge(full_estimation)
    dbsession.flush()

    request = get_csrf_request_with_db(
        post={"amount": "160"}, user=user, context=payment_line
    )

    view = PaymentLineRestView(request)
    result = view.put()
    assert result.amount == 16000000
    assert result.description == "Paiement"
