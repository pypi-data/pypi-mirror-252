import pytest
import os

from endi.tests.conftest import DATASDIR
from endi.views.admin.main.digital_signatures import (
    AdminDigitalSignaturesView,
    MAIN_ROUTE,
)

pytest.mark.usefixtures("config")


def test_digital_signatures_config_success(config, get_csrf_request_with_db, dbsession):
    config.add_route(MAIN_ROUTE, MAIN_ROUTE)
    from endi.models.config import ConfigFiles

    with open(os.path.join(DATASDIR, "digital_signature.jpg"), "rb") as image:
        datas = image.read()
        size = len(datas)
        image.seek(0)
        appstruct = {
            "cae_manager_digital_signature": {
                "fp": image,
                "mimetype": "image/jpeg",
                "uid": "1",
                "filename": "manager_signature.jpg",
                "size": size,
            }
        }
        view = AdminDigitalSignaturesView(get_csrf_request_with_db())
        view.submit_success(appstruct)
        dbsession.flush()
        assert (
            ConfigFiles.get("cae_manager_digital_signature.png").name
            == "manager_signature.jpg"
        )
        assert ConfigFiles.get("cae_manager_digital_signature.png").getvalue() == datas


def test_digital_signatures_config_delete_success(
    config, get_csrf_request_with_db, dbsession
):
    config.add_route(MAIN_ROUTE, MAIN_ROUTE)
    from endi.models.config import ConfigFiles

    with open(os.path.join(DATASDIR, "digital_signature.jpg"), "rb") as image:
        datas = image.read()
        size = len(datas)
        image.seek(0)
        appstruct = {
            "cae_manager_digital_signature": {
                "fp": image,
                "mimetype": "image/jpeg",
                "uid": "1",
                "filename": "manager_signature.jpg",
                "size": size,
            }
        }
        # Add image to local database
        view = AdminDigitalSignaturesView(get_csrf_request_with_db())
        view.submit_success(appstruct)
        dbsession.flush()
        assert (
            ConfigFiles.get("cae_manager_digital_signature.png").name
            == "manager_signature.jpg"
        )
        appstruct = {"cae_manager_digital_signature": {"delete": True}}
        # Delete image
        view = AdminDigitalSignaturesView(get_csrf_request_with_db())
        view.submit_success(appstruct)
        dbsession.flush()
        assert ConfigFiles.get("cae_manager_digital_signature.png") is None
