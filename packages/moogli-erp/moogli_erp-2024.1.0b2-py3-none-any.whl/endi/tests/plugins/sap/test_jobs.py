from unittest.mock import (
    patch,
    MagicMock,
)
import pytest

from endi.plugins.sap.celery_jobs import (
    _generate_attestations,
    EmptyResult,
)
from endi.plugins.sap.models.sap import SAPAttestation


pytestmark = [pytest.mark.plugin_sap]


@pytest.fixture(autouse=True)
def _routes(config):
    from endi.views.files.routes import PUBLIC_ITEM

    config.add_route(PUBLIC_ITEM, PUBLIC_ITEM)


@patch("endi.views.check_alive", return_value=(True, ""))
@patch(
    "endi.plugins.sap.views.attestation.generate_attestations",
    return_value=MagicMock(id=42),
)
def test_generate_attestations_wrong_year(
    dbsession,
    csrf_request,
    fully_paid_invoice,
):
    job_errors, job_messages = [], []
    # request = get_csrf_request_with_db_and_user()
    with pytest.raises(EmptyResult):
        _generate_attestations(
            [],
            [],
            job_errors,
            job_messages,
            True,
            csrf_request,
            year=2020,
        )


def test_generate_attestations_view(
    dbsession,
    csrf_request,
    fully_paid_invoice,
):
    job_errors, job_messages = [], []
    _generate_attestations(
        [],
        [],
        job_errors,
        job_messages,
        True,
        csrf_request,
        year=2019,  # 1 invoice with 1 line in 2019
    )

    assert SAPAttestation.query().count() == 1
    assert SAPAttestation.query().first().amount == 12000000  # 120€ TTC


def test_generate_attestations_partial_payments(
    dbsession,
    csrf_request,
    partly_paid_invoice,
):
    """
    We have in partly_paid_invoice:
    2 lines
      jardinage, 12€TTC
      bricolage, 24€TTC
    2 payments:
      5€
      7€
    -> paid : 12€
    -> unpaid : 24€
    """
    job_errors, job_messages = [], []

    _generate_attestations(
        [],
        [],
        job_errors,
        job_messages,
        True,
        csrf_request,
        year=2019,  # 1 invoice with 1 line in 2019
    )
    assert SAPAttestation.query().count() == 1
    assert SAPAttestation.query().first().amount == 1200000  # 12€ TTC


def test_generate_attestations_discount(
    dbsession,
    csrf_request,
    fully_paid_invoice_with_discount,
):
    """
    In theory, discount changes nothing here

    We have in fully_paid_invoice:
    1 lines 120€ TTC
    1 discount 12€TTC
    -> paid : 108€TTC
    -> unpaid : 0€TTC
    """
    job_errors, job_messages = [], []
    _generate_attestations(
        [],
        [],
        job_errors,
        job_messages,
        True,
        csrf_request,
        year=2019,  # 1 invoice with 1 line in 2019
    )
    assert SAPAttestation.query().count() == 1
    assert SAPAttestation.query().first().amount == 10800000  # 108€ TTC


def test_generate_attestations_multi(
    dbsession,
    csrf_request,
    # Group 1 :
    fully_paid_invoice,
    fully_paid_invoice_2,  # = company, = customer
    # Group 2
    fully_paid_invoice_customer_2,  # = company, ≠ customer
    # Group 3
    fully_paid_invoice_company_2,  # ≠ company, ≠ customer
):
    job_errors, job_messages = [], []
    _generate_attestations(
        [],
        [],
        job_errors,
        job_messages,
        True,
        csrf_request,
        year=2019,  # 1 invoice with 1 line in 2019
    )
    assert SAPAttestation.query().count() == 3


def test_sap_generate_sap_attestations_view_filtering(
    dbsession,
    csrf_request,
    company,
    customer_1,
    customer_2,
    company_2,
    fully_paid_invoice,
    fully_paid_invoice_2,  # = company, = customer
    fully_paid_invoice_customer_2,  # = company, ≠ customer
    fully_paid_invoice_company_2,  # ≠ company, ≠ customer
):
    expectlist = [
        (dict(customers_ids={customer_1.id}), 1),
        (dict(customers_ids={customer_2.id, customer_1.id}), 2),
        (dict(companies_ids={company_2.id}), 1),
    ]
    for _filter, expected_count in expectlist:
        job_errors, job_messages = [], []

        kwargs = dict(
            companies_ids=[],
            customers_ids=[],
            job_errors=job_errors,
            job_messages=job_messages,
            regenerate_existing=True,
            request=csrf_request,
            year=2019,
        )
        kwargs.update(_filter)
        _generate_attestations(**kwargs)
        job_errors, job_messages = [], []

        assert SAPAttestation.query().count() == expected_count
        SAPAttestation.query().delete()


def test_generate_attestations_regenerate(
    dbsession,
    csrf_request,
    fully_paid_invoice,
):
    job_errors, job_messages = [], []
    kwargs = dict(
        companies_ids=[],
        customers_ids=[],
        job_errors=job_errors,
        job_messages=job_messages,
        regenerate_existing=False,
        request=csrf_request,
        year=2019,
    )
    _generate_attestations(**kwargs)
    updated_at = SAPAttestation.query().first().updated_at

    # Did not change
    with pytest.raises(EmptyResult):
        _generate_attestations(**kwargs)
    assert SAPAttestation.query().first().updated_at == updated_at

    # Did change
    kwargs.update(dict(regenerate_existing=True))
    _generate_attestations(**kwargs)
    assert SAPAttestation.query().first().updated_at != updated_at
