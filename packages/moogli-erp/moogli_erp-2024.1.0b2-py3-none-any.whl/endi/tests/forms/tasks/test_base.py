import pytest
from endi.tests.tools import Dummy


@pytest.fixture
def company2(dbsession, user):
    from endi.models.company import Company

    company = Company(
        name="Company 2",
        email="company2@c.fr",
    )
    company.employees = [user]
    dbsession.add(company)
    dbsession.flush()
    user.companies = [company]
    user = dbsession.merge(user)
    dbsession.flush()
    return company


@pytest.fixture
def customer2(dbsession, company2):
    from endi.models.third_party.customer import Customer

    customer = Customer(
        name="customer 2",
        code="CUS2",
        lastname="Lastname2",
        firstname="Firstname2",
        address="1th street",
        zip_code="01234",
        city="City",
    )
    customer.company = company2
    dbsession.add(customer)
    dbsession.flush()
    return customer


@pytest.fixture
def project2(dbsession, company2, customer2, project_type):
    from endi.models.project import Project

    project = Project(name="Project 2", project_type=project_type)
    project.company = company2
    project.customers = [customer2]
    dbsession.add(project)
    dbsession.flush()
    return project


@pytest.fixture
def phase2(dbsession, project2):
    from endi.models.project import Phase

    phase = Phase(name="Phase")
    phase.project = project2
    phase.project_id = project2.id
    project2.phases.append(phase)
    dbsession.add(phase)
    dbsession.flush()
    return phase


def test_duplicate_task_schema(
    invoice, project, customer, phase, company, phase2, project2, default_business_type
):
    import colander
    from pyramid.testing import DummyRequest
    from endi.forms.tasks.base import get_duplicate_schema

    schema = get_duplicate_schema()
    req = DummyRequest(
        context=invoice,
        current_company=company,
    )
    schema = schema.bind(request=req)

    assert (
        schema["phase_id"].widget.values[0][1] == "Ne pas ranger dans un sous-dossier"
    )
    assert schema["name"].default == f"{invoice.name} (Copie)"

    result = schema.deserialize(
        {
            "name": "Facture",
            "customer_id": str(customer.id),
            "project_id": str(project.id),
            "phase_id": str(phase.id),
            "business_type_id": str(default_business_type.id),
        }
    )

    assert result == {
        "name": "Facture",
        "customer_id": customer.id,
        "project_id": project.id,
        "phase_id": phase.id,
        "business_type_id": default_business_type.id,
    }
    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                "name": "Facture",
                "customer_id": str(customer.id),
                "project_id": str(project.id),
                "phase_id": str(phase2.id),
                "business_type_id": str(default_business_type.id),
            }
        )

    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                "name": "Facture",
                "customer_id": str(customer.id),
                "project_id": str(project2.id),
                "phase_id": str(phase2.id),
                "business_type_id": str(default_business_type.id),
            }
        )

    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                "name": "Facture",
                "customer_id": str(customer.id),
                "project_id": str(project2.id),
                "phase_id": str(phase2.id),
            }
        )


def test_get_business_types_from_request_1065(
    project,
    project_type,
    mk_business_type,
    pyramid_request,
):
    from endi.forms.tasks.base import get_business_types_from_request
    from unittest.mock import MagicMock

    # contexte avec business_type qui n'est pas dans project_type.business_types
    context = MagicMock()

    context.business_type = mk_business_type("test")
    context.project = project

    pyramid_request.context = context

    assert context.business_type in get_business_types_from_request(pyramid_request)


def test_get_task_metadatas_edit_schema(
    dbsession,
    pyramid_request,
    invoice,
    mk_business,
):
    from endi.models.config import Config
    from endi.forms.tasks.base import get_task_metadatas_edit_schema

    pyramid_request.context = invoice
    invoice.business = mk_business()
    pyramid_request.matched_route = Dummy(name="invoice")
    schema = get_task_metadatas_edit_schema()

    Config.set("invoice_number_template", "${SEQGLOBAL}")
    dbsession.flush()

    bound_schema = schema.bind(request=pyramid_request)
    date_node = bound_schema.get("date")
    assert date_node is not None
    assert date_node.validator is None

    Config.set("invoice_number_template", "${SEQYEAR}")
    dbsession.flush()

    bound_schema = schema.bind(request=pyramid_request)
    date_node = bound_schema.get("date")
    assert date_node is not None
    assert date_node.validator is not None

    schema = get_task_metadatas_edit_schema()
    invoice.invoicing_mode = invoice.PROGRESS_MODE
    bound_schema = schema.bind(request=pyramid_request)
    for key in ("customer_id", "project_id", "phase_id"):
        node = bound_schema.get(key)
        assert node is None
