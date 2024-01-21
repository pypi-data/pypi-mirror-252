import pytest

from endi.models.config import (
    get_config,
)

pytest.mark.usefixtures("config")


def test_admin_contact_success(config, get_csrf_request_with_db, dbsession):
    from endi.views.admin.main.contact import (
        AdminContactView,
        MAIN_ROUTE,
    )

    config.add_route(MAIN_ROUTE, MAIN_ROUTE)
    appstruct = {"cae_admin_mail": "admin@cae.fr"}
    view = AdminContactView(get_csrf_request_with_db())
    view.submit_success(appstruct)
    assert get_config()["cae_admin_mail"] == "admin@cae.fr"
