import pytest

from endi.models.config import (
    get_config,
)

pytest.mark.usefixtures("config")


def test_admin_cae_success(config, get_csrf_request_with_db, dbsession):
    from endi.views.admin.main.cae import (
        AdminCaeView,
        MAIN_ROUTE,
    )

    config.add_route(MAIN_ROUTE, MAIN_ROUTE)
    appstruct = {
        "cae_business_name": "MA CAE",
        "cae_legal_status": "SARL",
        "cae_address": "2 rue girard\n",
        "cae_zipcode": "21000",
        "cae_city": "Dijon",
        "cae_tel": "000000000",
        "cae_contact_email": "contact@macae.fr",
        "cae_business_identification": "XXXXX",
        "cae_intercommunity_vat": "TVA XXX",
        "cae_vat_collect_mode": "debit",
    }
    view = AdminCaeView(get_csrf_request_with_db())
    view.submit_success(appstruct)
    for key, value in list(appstruct.items()):
        assert get_config()[key] == value
