import pytest
import colander
import datetime


@pytest.fixture
def other_project_type(dbsession, mk_business_type):
    other_business_type = mk_business_type(name="other")
    from endi.models.project.types import ProjectType

    result = ProjectType(name="other", label="other")
    result.default_business_type = other_business_type
    dbsession.add(result)
    dbsession.flush()
    return result


def test_full_add_project_schema(
    dbsession,
    customer,
    pyramid_request,
    company,
    mk_project_type,
    mk_business_type,
):
    from endi.forms.project import get_full_add_project_schema

    business_type = mk_business_type(name="default")
    other_business_type = mk_business_type(name="other")
    project_type = mk_project_type(
        name="ptype",
        default_btype=business_type,
        other_business_types=[other_business_type],
        with_business=True,
    )
    schema = get_full_add_project_schema()
    pyramid_request.context = company
    schema = schema.bind(request=pyramid_request)
    args = {
        "name": "Test project",
        "project_type_id": str(project_type.id),
        "business_types": [str(other_business_type.id)],
        "mode": "ht",
    }
    result = schema.deserialize(args)
    assert result["name"] == "Test project"
    assert result["project_type_id"] == project_type.id
    assert result["mode"] == "ht"
    assert result["business_types"] == [other_business_type.id]

    wrong = args.copy()
    wrong["mode"] = "ttc"
    with pytest.raises(colander.Invalid):
        schema.deserialize(wrong)

    project_type.ttc_compute_mode_allowed = True
    dbsession.merge(project_type)
    result = schema.deserialize(wrong)
    assert result["mode"] == "ttc"

    wrong_btype = mk_business_type(name="wrong")
    wrong = args.copy()
    wrong["business_types"] = [str(wrong_btype.id)]
    with pytest.raises(colander.Invalid):
        schema.deserialize(wrong)


def test_add_project_schema(customer, project_type, pyramid_request, company):
    from endi.forms.project import get_add_project_schema

    schema = get_add_project_schema()
    pyramid_request.context = company
    schema = schema.bind(request=pyramid_request)

    args = {
        "name": "Test project",
        "project_type_id": str(project_type.id),
        "customers": [str(customer.id)],
    }
    result = schema.deserialize(args)
    assert result["name"] == "Test project"
    assert result["project_type_id"] == project_type.id
    assert result["customers"] == [customer.id]

    for field in "name", "customers", "project_type_id":
        wrong = args.copy()
        wrong.pop(field)
        with pytest.raises(colander.Invalid):
            schema.deserialize(wrong)

    # Ref #2351 : https://framagit.org/endi/endi/-/issues/2351
    args = {
        "name": "Test project",
        "project_type_id": str(project_type.id),
        "customers": [str(customer.id), ""],
    }
    result = schema.deserialize(args)
    assert result["customers"] == [customer.id]

    args["customers"].pop(0)
    with pytest.raises(colander.Invalid):
        schema.deserialize(wrong)


def test_add_step2_project_schema():
    from endi.forms.project import get_add_step2_project_schema

    schema = get_add_step2_project_schema()

    args = {
        "description": "Descr",
        "code": "PROJ",
        "starting_date": "2016-02-01",
        "ending_date": "2016-02-02",
    }

    result = schema.deserialize(args)
    assert result["description"] == "Descr"
    assert result["code"] == "PROJ"
    assert result["starting_date"] == datetime.date(2016, 2, 1)

    args["starting_date"] = "2016-02-03"
    with pytest.raises(colander.Invalid):
        schema.deserialize(args)


def test_edit_project_schema(
    customer,
    get_csrf_request_with_db,
    project_type,
    company,
    project,
    customer2,
    mk_estimation,
):
    from endi.forms.project import get_edit_project_schema

    pyramid_request = get_csrf_request_with_db(context=project)

    schema = get_edit_project_schema()
    schema = schema.bind(request=pyramid_request)

    args = {
        "name": "Other name",
        "customers": [str(customer.id)],
        "project_type_id": str(project_type.id),
    }
    result = schema.deserialize(args)

    assert result["name"] == "Other name"
    assert result["customers"] == [customer.id]

    mk_estimation(project=project, customer=customer2)
    schema = get_edit_project_schema()
    schema = schema.bind(request=pyramid_request)
    result = schema.deserialize(args)
    # Assure que le client qui a un devis est toujours dans le projet
    assert customer2.id in result["customers"]


def test_is_compatible_project_type(
    dbsession,
    project,
    customer,
    user,
    company,
    other_project_type,
    default_business_type,
    mk_business_type,
):
    from endi.models.task.estimation import Estimation

    estimation = Estimation(
        company=company,
        project=project,
        customer=customer,
        user=user,
        business_type=other_project_type.default_business_type,
    )
    dbsession.add(estimation)
    dbsession.flush()

    from endi.forms.project import _is_compatible_project_type

    assert _is_compatible_project_type(project, other_project_type)

    new_estimation = Estimation(
        company=company,
        project=project,
        customer=customer,
        user=user,
        business_type=default_business_type,
    )
    dbsession.add(new_estimation)
    dbsession.flush()
    assert not _is_compatible_project_type(project, other_project_type)
