import pytest
import os

from endi.tests.conftest import DATASDIR
from endi.models.config import (
    get_config,
)

pytest.mark.usefixtures("config")


def test_site_config_success(config, get_csrf_request_with_db, dbsession):
    from endi.views.admin.main.site import (
        AdminSiteView,
        MAIN_ROUTE,
    )

    config.add_route(MAIN_ROUTE, MAIN_ROUTE)
    from endi.models.config import ConfigFiles

    with open(os.path.join(DATASDIR, "entete5_1.png"), "rb") as image:
        datas = image.read()
        size = len(datas)
        image.seek(0)
        appstruct = {
            "welcome": "testvalue",
            "logo": {
                "fp": image,
                "mimetype": "image/png",
                "uid": "1",
                "filename": "F.png",
                "size": size,
            },
            "login_backgrounds": [],
        }
        view = AdminSiteView(get_csrf_request_with_db())
        view.submit_success(appstruct)
        dbsession.flush()
        assert get_config()["welcome"] == "testvalue"
        assert ConfigFiles.get("logo.png").name == "F.png"
        assert ConfigFiles.get("logo.png").getvalue() == datas
