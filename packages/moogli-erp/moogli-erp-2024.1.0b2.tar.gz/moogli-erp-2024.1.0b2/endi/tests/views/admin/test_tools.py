from endi.models.config import Config


def test_base_config_view(config, dbsession, get_csrf_request_with_db):
    from endi.views.admin.tools import BaseConfigView
    from endi.forms.admin import get_config_schema

    class TestView(BaseConfigView):
        title = ("Test",)
        keys = ("test_key1", "test_key2")
        schema = get_config_schema(keys)
        validation_msg = "Ok"
        back_link = "/"

    config.add_route("/", "/")

    appstruct = {"test_key1": "test1", "test_wrong_key": "test error"}

    view = TestView(get_csrf_request_with_db())
    view.submit_success(appstruct)

    assert Config.get("test_key1").value == "test1"
    assert Config.get("test_wrong_key") == None
