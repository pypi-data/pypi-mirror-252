import pytest
from endi.tests.tools import Dummy


@pytest.fixture
def settings():
    return {}


@pytest.fixture
def request_(settings):
    # request is a reserved py.test name
    registry = Dummy(settings=settings)
    req = Dummy(registry=registry, headers={})
    return req


def test_settings_has_value(request_, settings):
    from endi.utils.predicates import SettingHasValuePredicate

    predicate = SettingHasValuePredicate(("key", True), None)
    assert predicate(None, request_) is False
    predicate = SettingHasValuePredicate(("key", False), None)
    assert predicate(None, request_) is True

    settings["key"] = "Test value"
    predicate = SettingHasValuePredicate(("key", True), None)
    assert predicate(None, request_) is True
    predicate = SettingHasValuePredicate(("key", False), None)
    assert predicate(None, request_) is False
