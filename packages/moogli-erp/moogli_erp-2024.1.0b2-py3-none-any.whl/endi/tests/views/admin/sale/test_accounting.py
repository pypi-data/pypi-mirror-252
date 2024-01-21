import pytest

from endi.models.config import (
    get_config,
)

pytest.mark.usefixtures("config")


def test_config_cae_success(config, dbsession, get_csrf_request_with_db):
    from endi.views.admin.sale.accounting.invoice import (
        ConfigView,
        INDEX_URL,
    )

    ConfigView.back_link = INDEX_URL

    appstruct = {
        "compte_rrr": "000009558",
        "cae_general_customer_account": "00000556",
        "cae_third_party_customer_account": "00000665",
    }
    view = ConfigView(get_csrf_request_with_db())
    view.submit_success(appstruct)
    config = get_config()
    for key, value in list(appstruct.items()):
        assert config[key] == value
