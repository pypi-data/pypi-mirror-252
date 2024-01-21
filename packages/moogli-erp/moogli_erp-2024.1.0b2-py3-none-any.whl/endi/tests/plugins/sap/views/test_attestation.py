from unittest import mock
from unittest.mock import (
    patch,
    MagicMock,
)

import colander
import pytest
from pyramid.httpexceptions import HTTPFound


pytestmark = [pytest.mark.plugin_sap]


@pytest.fixture
def sap_routes(config):
    from endi.plugins.sap.views.attestation import add_routes

    add_routes(config)


def test_sap_addpayment_view(config, get_csrf_request_with_db, user, full_invoice):
    from endi.plugins.sap.views.payment import SAPInvoicePaymentAddView

    request = get_csrf_request_with_db(context=full_invoice)
    view = SAPInvoicePaymentAddView(request)
    schema = view.get_schema().bind(request=request)
    assert schema["date"].default == colander.null

    # Assert no crash
    result = view.__call__()
    assert isinstance(result, dict)


@patch("endi.views.check_alive", return_value=(True, ""))
@patch(
    "endi.plugins.sap.views.attestation.generate_attestations",
    return_value=MagicMock(id=42),
)
def test_sap_generate_sap_attestations_view(
    get_csrf_request_with_db_and_user,
    config,
    sap_routes,
    fully_paid_invoice,
):
    from endi.plugins.sap.views.attestation import GenerateSapAttestationView

    config.add_route("job", "/jobs/{id:\d+}")
    appstruct = {"year": 2020}
    request = get_csrf_request_with_db_and_user(post=appstruct)
    result = GenerateSapAttestationView(request).submit_success(appstruct)

    assert isinstance(result, HTTPFound)
